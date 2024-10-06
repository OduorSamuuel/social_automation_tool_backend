from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from .models import User

@api_view(['GET'])
def get_stats(request):
    # Dummy data to simulate stats coming from the database
    data = {
        "active_users": 10500,
        "uptime_percentage": 99.9,
        "support_hours": 24
    }
    return Response(data)

@api_view(['POST'])
def signup_user(request):
    try:
        data = request.data
        # Create the user object and hash the password
        user = User.objects.create(
            name=data['name'],
            email=data['email'],
            phone_number=data['phoneNumber'],
            password=make_password(data['password']),  # Hash the password before saving
        )
        user.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    try:
        data = request.data
        email = data.get('email')
        password = data.get('password')

        # Retrieve the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the provided password matches the hashed password
        if check_password(password, user.password):
            return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)