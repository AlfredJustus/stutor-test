"""
This file helps keep track of which school a user is viewing.
When someone visits a school's page (like /school-name/), this code automatically
figures out which school they're looking at and makes that information available
to all pages. This is important because our app shows different tutors and information
depending on which school you're viewing.
"""

from users.models import tutor, School 
from django.conf import settings
from django.urls import resolve, Resolver404


def school_context(request):
    """
    Context processor to add the current school object to the context
    if a school_slug is present in the URL.
    """
    # Default value if no school is found/identified
    context = {'current_school': None}

    # Get the full path from the request
    path = request.path_info

    # Try to match the path to a URL pattern to extract parameters
    try:
        # resolve() matches the path to a URL pattern and gives us the match object
        match = resolve(path)
        # Check if 'school_slug' is one of the keyword arguments captured by the URL pattern
        if 'school_slug' in match.kwargs:
            school_slug = match.kwargs['school_slug']
            # Try to fetch the School object based on the slug
            try:
                school = School.objects.get(slug=school_slug)
                # Add the school object to the context dictionary
                context['current_school'] = school
            except School.DoesNotExist:
                # If the slug in the URL doesn't match a school,
                # you could log this or handle it as appropriate.
                # For now, we'll just leave current_school as None.
                pass
    except Resolver404:
        # The path didn't match any URL pattern.
        # This processor will just return the default context {'current_school': None}.
        pass
    except Exception as e:
         # Catch other potential errors during resolution or fetching
         print(f"Error in school_context processor: {e}")
         pass
    
    return context
