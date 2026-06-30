from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        DOCTOR = 'Doctor', 'Doctor'
        RECEPTIONIST = 'Receptionist', 'Receptionist'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RECEPTIONIST)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
