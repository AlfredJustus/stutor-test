
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Custom form to handle user creation, extending from Django's built-in UserCreationForm.
# Adds a required email field and customizes the fields for user creation.
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        # Specify the custom User model and the fields to be used in the form.
        model = User  
        fields = ('email', 'password1', 'password2')