# social/models.py
from django.conf import settings  # Import settings
from django.db import models

class SocialAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL
    platform = models.CharField(max_length=100)  # e.g., 'facebook', 'tiktok', etc.
    account_id = models.CharField(max_length=255)  # Unique identifier for the social account
    access_token = models.CharField(max_length=255)  # Token for API calls
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} account for {self.user.username}"
