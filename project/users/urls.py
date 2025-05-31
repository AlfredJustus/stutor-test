"""
This file tells the website what to show when someone visits different urls. You don't see the school
   slug here because it's already in the url. 
It sets up two main pages:
1. The main school page: When someone visits /school-name/
   (like /gymnasium-muenchen/), it shows all tutors at that school. 
2. The tutor profile page: When someone visits /school-name/tutor/tutor-name/
   (like /gymnasium-muenchen/tutor/john-smith/), it shows that tutor's profile
This is like a map that helps the website know which page to show for each URL.
"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # School-specific URLs
    path('', views.show_tutors, name='show-tutors'),  # Make this the default view for a school
    path('tutor/<slug:slug>/', views.tutor_profile, name='profile'),
    # Non-school-specific RLs
    
]