# Django imports
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string

# Rest framework imports
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

# Token imports
from rest_framework_simplejwt.tokens import RefreshToken

# Local imports
from .serializers import (
    UserSerializer, LoginSerializer, UpdateUserSerializer, 
    PasswordResetRequestSerializer, SetNewPasswordSerializer
)

# Get custom User model
User = get_user_model()


# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


# User Login View
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Logout View
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")  # Get the refresh token from the request
            token = RefreshToken(refresh_token)  # Create a RefreshToken object from the token
            token.blacklist()  # Blacklist the token
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# User Profile View (Get and Update)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

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
                # Generate token and UID
                token = PasswordResetTokenGenerator().make_token(user)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

                # Create password reset link
                domain = get_current_site(request).domain
                relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})  # Ensure this matches the URL pattern
                reset_url = f'http://{domain}{relative_link}'

                # Email content
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
            # Decode UID to get user ID
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            # Check if the token is valid
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                # Set new password and save user
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
