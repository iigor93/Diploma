from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model"""
    default_password = models.CharField(max_length=20, default='qwerty123')
