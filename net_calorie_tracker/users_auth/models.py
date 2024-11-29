from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password

class CustomUser(AbstractUser):
    name = models.CharField(max_length=150, blank=False)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female')],
        null=True,
        blank=True,
    )
    dob = models.DateField(help_text="Date of birth", null=True, blank=True)
    is_admin = models.BooleanField(default=False, help_text="True for admin users")

    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        """Override to ensure password is hashed"""
        self.password = make_password(raw_password)

    @property
    def age(self):
        """Calculate age based on the date of birth."""
        from datetime import date
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None