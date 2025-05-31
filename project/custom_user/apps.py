# Import the AppConfig class from Django's apps module.
# AppConfig is used to configure an application and its properties.
from django.apps import AppConfig

# Define a custom application configuration class for the 'custom_user' app.
class CustomUserConfig(AppConfig):
    # The name attribute specifies the Python path to the application.
    name = 'custom_user'
    
    # The verbose_name attribute provides a human-readable name for the app.
    # This is useful for display purposes in the admin interface.
    verbose_name = 'Custom User Management'
