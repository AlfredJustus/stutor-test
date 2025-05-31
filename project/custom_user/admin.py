# custom_user/admin.py

from django.contrib import admin
from django.contrib.admin import SimpleListFilter # Import SimpleListFilter
from django_use_email_as_username.admin import BaseUserAdmin
from django.contrib import admin, messages # Import messages
from django.contrib.admin import SimpleListFilter
from django.urls import path, reverse # Import path and reverse
from django.shortcuts import redirect # Import redirect
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import User # Assuming your custom User model is in .models
from users.models import School # Import School model for filtering
import logging # For logging the action
logger = logging.getLogger(__name__)

# --- Custom Filter Classes ---
class HasTutorFilter(SimpleListFilter):
    """
    Custom admin filter to filter Users based on whether they have a
    related Tutor object. This helps admins quickly find users who have
    completed their tutor profile vs those who haven't.
    """
    # Human-readable title displayed in the filter sidebar
    title = ('Has Tutor Account')

    # Parameter name for the filter in the URL query string
    parameter_name = 'has_tutor'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. Each tuple is a pair:
        (value, human_readable_label) for the filter options.
        """
        return [
            ('yes', ('Yes')),
            ('no', ('No')),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value selected in the lookup.
        'yes' filters for users with a related tutor.
        'no' filters for users without a related tutor.
        """
        # The 'tutor' part comes from the related_name='tutor' on the
        # OneToOneField in the Tutor model that links back to the User.
        if self.value() == 'yes':
            # Filter users who have a related tutor object (where the tutor link is not null)
            return queryset.filter(tutor__isnull=False)
        if self.value() == 'no':
            # Filter users who do NOT have a related tutor object (where the tutor link is null)
            return queryset.filter(tutor__isnull=True)

        # Return the original queryset if no filter is selected
        return queryset

class SchoolFilter(SimpleListFilter):
    """
    Custom admin filter to filter Users based on their associated school.
    This helps admins manage users by their school affiliation.
    """
    title = 'School'
    parameter_name = 'school'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples containing all available schools.
        Each tuple is (school_id, school_name).
        """
        schools = School.objects.all()
        return [(school.id, school.name) for school in schools]

    def queryset(self, request, queryset):
        """
        Returns users filtered by the selected school.
        """
        if self.value():
            return queryset.filter(school_id=self.value())
        return queryset

# --- Admin Action to Export Selected User Emails ---
def export_selected_user_emails(modeladmin, request, queryset):
    """
    Admin action to export emails of *selected* users.
    This is useful for sending bulk emails or notifications to specific users.
    """
    # The 'queryset' here is already the set of users selected by the checkboxes.
    selected_users_queryset = queryset

    count = selected_users_queryset.count()

    if count == 0:
        # Message indicates no users were selected
        messages.warning(request, "No users were selected.")
        logger.info(f"Admin user {request.user} attempted to export emails: No users selected.")
        return # Do nothing further if no users are selected

    # Get the emails from the selected queryset
    emails = list(selected_users_queryset.values_list('email', flat=True))

    # Format as a comma-separated string for easy copying/pasting
    email_list_string = ", ".join(emails)

    # Display the emails as a success message.
    # Message indicates it's the selected users' emails
    messages.success(request,
                     f"Found {count} email(s) for the selected users. Copy the list below: "
                     f"{email_list_string}")

    logger.info(f"Admin user {request.user} exported {count} emails of selected users.")

# Define a short description for the new action dropdown
export_selected_user_emails.short_description = "Export emails of selected users"

# --- Custom User Admin Class ---
class UserAdminWithTutorFilter(BaseUserAdmin):
    """
    Custom admin interface for User model with additional filters and display options.
    This extends the base user admin to include school and tutor information.
    """
    # Add custom filters to the existing list_filter
    list_filter = BaseUserAdmin.list_filter + (HasTutorFilter, SchoolFilter)

    # Add the export action to available actions
    actions = [export_selected_user_emails]

    # Add custom fields to the list display
    list_display = BaseUserAdmin.list_display + ('has_tutor_account', 'get_school')

    def has_tutor_account(self, obj):
        """Display whether a user has a tutor account."""
        return hasattr(obj, 'tutor')

    has_tutor_account.boolean = True
    has_tutor_account.short_description = 'Has Tutor'

    def get_school(self, obj):
        """Display the user's school name."""
        return obj.school.name if obj.school else '-'

    get_school.short_description = 'School'

# --- Register the model with the new Admin class ---
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Register the User model with our custom Admin class
admin.site.register(User, UserAdminWithTutorFilter)
