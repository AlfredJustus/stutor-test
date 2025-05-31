"""
This file creates the filter form that students use to find tutors.
It lets students filter tutors by:
- What subject they want to learn (like Math, English, etc.)
- What language the tutor teaches in (German or English)
- What grade level they need (like 5th grade, 6th grade, etc.)
- How much they're willing to pay per hour
This form appears on the school's main page where all tutors are listed.
"""

from django import forms
from .models import tutor, subject

# Form for filtering tutors based on specific criteria such as subject, grade level, and price range.
class tutorFilter(forms.Form):
    # Field for selecting a subject from available subjects in the database.
    subject = forms.ModelChoiceField(
        queryset=subject.objects.all(),  # Get subjects from the database
        required=False,
        label='Subject',
        empty_label='All Subjects',  # Placeholder for the default "All Subjects" option
    )

    teaching_language = forms.ChoiceField(
        choices=[('', 'Tutor Language')] + [(lang, tutor.LANGUAGE_CHOICES[lang]) for lang in tutor.LANGUAGE_CHOICES.keys()],
        required=False,
        label='Tutor Language'
    )

    # Field for selecting a grade level from predefined choices in the tutor model.
    gradeLevel = forms.ChoiceField(
        choices=[('', 'Grade Level')] + [(grade, tutor.GRADELEVEL_CHOICES[grade]) for grade in tutor.GRADELEVEL_CHOICES.keys()],
        required=False,
        label='Grade Level'
    )

    # Field for entering a maximum price for filtering tutors.
    max_price = forms.DecimalField(
        required=False,
        label='Maximum Price',
        min_value=0,
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={'placeholder': 'Max Price'})
    )

