# This file defines the database models for the tutor application.
# Models are Python classes that represent database tables. Each model class
# defines the structure of a table, including its fields and relationships.

from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
import uuid

def generate_unique_slug(instance):
    return str(uuid.uuid4())[:8]

class subject(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self) -> str:
        return self.name 

class School(models.Model):
    # CharField is used for text with a maximum length
    name = models.CharField(max_length=100, unique=True)
    # SlugField is used for URL-friendly versions of names
    # unique=True ensures no two schools can have the same slug
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class tutor(models.Model):
    # Choices for grade levels
    GRADELEVEL_CHOICES = {
        "7": "7th grade",
        "8": "8th grade",
        "9": "9th grade",
        "10": "10th grade",
        "11": "11th grade",
        "12": "12th grade",
        "Postgraduate": "Postgraduate"
    }

    # Choices for teaching languages
    LANGUAGE_CHOICES = {
        "English": "English",
        "German": "German",
        "German and English": "Both languages"
    }

    first_name = models.CharField(max_length=50)
    # CharField for tutor's last name
    last_name = models.CharField(max_length=50)
    # SlugField for URL-friendly version of name
    slug = AutoSlugField(populate_from=generate_unique_slug, unique=True)
    gradeLevel = models.CharField(max_length=15, choices=GRADELEVEL_CHOICES, default="12")
    asking_price = models.DecimalField(max_digits=10, decimal_places=2, default="10")
    subjects = models.ManyToManyField(subject)
    # CharField for teaching language with choices
    teaching_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default="Eng")
    picture = models.ImageField(default='fallback.png', upload_to='profile_pictures/')
    body = models.TextField(max_length=1000)
    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tutor')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='tutors')
    verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
