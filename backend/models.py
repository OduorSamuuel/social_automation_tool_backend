# models.py in your app (e.g., 'users' or 'backend')
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name
