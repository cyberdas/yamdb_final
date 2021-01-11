from django.db import models
from django.contrib.auth.models import AbstractUser

class EmailCode(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True)
    confirmation_code = models.CharField(max_length=88)

    def __str__(self):
        return self.username

class UserRole(models.TextChoices):
    admin = 'admin'
    moderator = 'moderator'
    user = 'user'

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.user)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username