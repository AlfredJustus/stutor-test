# Configuration for the 'users' app, specifying the default auto field type and the app's name.

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

