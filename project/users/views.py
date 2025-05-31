"""
This file controls what students see when they visit different pages.
It has two main pages:
1. The tutor list page: Shows all verified tutors at a school and lets students
   search for tutors using the filters (like subject, grade level, etc.)
2. The tutor profile page: Shows detailed information about one specific tutor,
   including their subjects, experience, and contact information.
Only verified tutors (approved by the admin) are shown to students.
"""

from django.shortcuts import render, get_object_or_404
from .models import tutor, School, subject
from users.forms import tutorFilter

# View to display a list of tutors based on optional subject and grade level filters.
def show_tutors(request, school_slug):
    school = get_object_or_404(School, slug=school_slug)
    subject_filter = request.GET.get('subject', '')
    teaching_language = request.GET.get('teaching_language', '')
    gradeLevel = request.GET.get('gradeLevel', '')

    # Filter tutors by school AND verified status
    tutors = tutor.objects.filter(school=school, verified=True)

    if subject_filter:
        tutors = tutors.filter(subjects=subject_filter)
    if teaching_language:
        tutors = tutors.filter(teaching_language=teaching_language)
    if gradeLevel:
        tutors = tutors.filter(gradeLevel=gradeLevel)
    
    tutors = tutors.order_by('?')

    context = {
        'form': tutorFilter(initial={
            'subject': subject_filter,
            'teaching_language': teaching_language,
            'gradeLevel': gradeLevel,
        }),
        'tutors': tutors,
        'school': school,
    }

    return render(request, 'users/overview.html', context)

# View to display an individual tutor profile by their unique slug.
def tutor_profile(request, school_slug, slug):
    # school and current_school are available
    school = get_object_or_404(School, slug=school_slug)
    # Fetch the tutor, ensuring they belong to this school and are verified
    profile = get_object_or_404(tutor, slug=slug, school=school, verified=True) # Only show verified tutors

    email = profile.author.email # Get tutor's email (consider privacy if this is public)

    # Prepare context
    context = {
        'profile': profile,
        'email': email, # Consider if email should be public
        'school': school, # school and current_school are available
    }
    return render(request, 'users/profile.html', context)
