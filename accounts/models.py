# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True,)

    def get_last_name_first_name(self):
        if self.first_name and self.last_name:
            return f"{self.last_name}, {self.first_name}"
        return None

    # changes the description of the field label in the admin panel for the method
    get_last_name_first_name.short_description = "Last Name, First Name"
