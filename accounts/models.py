from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Use email as login field
    email = models.EmailField(unique=True)

    wallet_address = models.CharField(
        max_length=42,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def display_name(self):
        return self.email.split('@')[0]

    def __str__(self):
        return self.email


class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.otp}"
