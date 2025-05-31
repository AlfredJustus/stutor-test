"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from . import views
from users import views as users_views

# URL patterns for the main app, mapping URL paths to corresponding view functions and to other apps.

urlpatterns = [
    path('admin/', admin.site.urls), # this is where the admin page will be 
    path('', views.homepage),
    path('custom_user/', include('custom_user.urls')),
    path('<slug:school_slug>/', include('users.urls', namespace='users')), # this refers to the urls that are introduced in the users app
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # telling the app where to find the images
 