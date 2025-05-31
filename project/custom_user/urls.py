from django.urls import path
from . import views

app_name = 'custom_user'

# URL patterns for the 'custom_user' app, mapping URL paths to corresponding view functions.

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('registration-information/', views.registration_information, name='registration-information'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify/', views.verify_view, name='verify-please'),
    path('email-success/', views.verification_successful_view, name='successful-email-verification'),

    
]
