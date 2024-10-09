from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# User Registration Serializer
# Django imports
from django.contrib.auth import get_user_model

# DRF imports
from rest_framework import serializers

# Password reset imports
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes

# Email imports
from django.core.mail import send_mail

# Get the custom User model
User = get_user_model()

# User Registration Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# Update User Serializer
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

# Password Reset Request Serializer
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']


# Set New Password Serializer (for confirming password reset)
class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['new_password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            user_id = smart_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, attrs['token']):
                raise serializers.ValidationError({'token': 'Token is invalid or expired'})

            user.set_password(attrs['new_password'])
            user.save()

        except Exception as e:
            raise serializers.ValidationError({'error': str(e)})

        return super().validate(attrs)
