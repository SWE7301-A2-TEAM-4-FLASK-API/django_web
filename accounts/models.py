from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('consumer', 'Consumer'),
        ('researcher', 'Researcher'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='consumer')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_2fa_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    plan = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

class UserUpdate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='settings')
    email_notifications = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50, default='UTC')

    def __str__(self):
        return f'Settings of {self.user.username}'