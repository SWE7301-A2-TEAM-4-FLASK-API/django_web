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
    fullname = models.CharField(max_length=150, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
