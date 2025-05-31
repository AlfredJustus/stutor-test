from django_use_email_as_username.models import BaseUser, BaseUserManager
from users.models import School
from django.db import models

# Define a custom user model by inheriting from BaseUser.
# The custom model uses BaseUserManager for user-related queries and operations.


class User(BaseUser):
    objects = BaseUserManager()
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
