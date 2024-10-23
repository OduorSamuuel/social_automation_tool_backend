# Django imports
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.conf import settings


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

# Rest framework imports
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

# Google Auth
from google.oauth2 import id_token
from google.auth.transport import requests

# Local imports
from .serializers import (
    UserSerializer, LoginSerializer, UpdateUserSerializer,
    PasswordResetRequestSerializer, SetNewPasswordSerializer, UserProfileSerializer
)

# Get custom User model
User = get_user_model()

# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

# User Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log the user in (this sets the session cookie)
            login(request, user)

            # Send a success response with user data
            response = Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)

            # Explicitly include the session ID cookie in the response headers (optional)
            response.set_cookie(
                key='sessionid',
                value=request.session.session_key,
                httponly=True,  # Ensures that the cookie cannot be accessed via JavaScript
                secure=True,  # Only send cookie over HTTPS
                samesite='Lax'  # Adjust if needed, e.g., 'None' for cross-site requests
            )

            return response

        else:
            # Send a failure response if authentication fails
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Google Auth View
# Google Auth View
class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Introducing a clock skew allowance of 10 seconds
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID, clock_skew_in_seconds=10)

            # Validate the issuer to ensure it comes from Google
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            email = idinfo['email']

            # Check if the user exists, if not, create a new user
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.set_unusable_password()  # Prevent direct login with password
                user.save()

            # Log the user in using the default authentication backend
            login(request, user)  # No backend specified here

            # Explicitly save the session if necessary
            request.session.save()

            # Get the session key saved to the database
            session_key = request.session.session_key

            return Response({
                'message': 'Google authentication successful',
                'user': {
                    'id': user.id,
                    'email': user.email,
                },
                'session_key': session_key  # Include the session key in the response
            }, status=status.HTTP_200_OK)

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            email = idinfo['email']

            # Check if the user exists, if not, create a new user
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.set_unusable_password()
                user.save()

            # Log the user in with the correct backend
            login(request, user, backend='social_core.backends.google.GoogleOAuth2')

            return Response({
                'message': 'Google login successful',
                'user': {
                    'id': user.id,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

# User Logout View
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logout(request)
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# User Profile View (Get and Update)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]  # Set permission to allow any authenticated user

    def get_object(self):
        return self.request.user

# Password Reset Request View
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            user = User.objects.filter(email=email).first()

            if user:
                token = PasswordResetTokenGenerator().make_token(user)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

                domain = get_current_site(request).domain
                relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
                reset_url = f'http://{domain}{relative_link}'

                subject = 'Password Reset Request'
                message = f'Hello,\nUse the link below to reset your password:\n{reset_url}'
                send_mail(subject, message, 'from@example.com', [user.email])

                return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Confirm Password Reset View (Set new password)
class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def patch(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                user.set_password(serializer.data['new_password'])
                user.save()
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckLoginStatusView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            return Response({
                'id': user.id,
                'email': user.email,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)