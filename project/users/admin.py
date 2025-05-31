"""
This file controls the admin panel where school administrators manage the platform.
Admins can:
1. Review and verify new tutor applications
2. Send automatic emails to tutors when they're verified
3. Send emails when tutors are rejected or their accounts are deleted
4. Manage the list of subjects that tutors can teach
5. Add and manage schools in the system
This is where all the behind-the-scenes management happens.
"""

from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import tutor, subject, School
from django.contrib import messages

@admin.register(tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'school', 'verified')
    list_filter = ('verified', 'school', 'subjects')
    search_fields = ('first_name', 'last_name', 'school__name')
    filter_horizontal = ('subjects',)
    
    def save_model(self, request, obj, form, change):
        if change:  # Only for existing objects
            old_obj = self.model.objects.get(pk=obj.pk)
            # Check if verified status changed from False to True
            if not old_obj.verified and obj.verified:
                # Prepare the email
                html_message = render_to_string('users/verification_email.html', {
                    'tutor': obj,
                })
                plain_message = strip_tags(html_message)
                
                # Send the email
                try:
                    send_mail(
                        subject='Congratulations! You are now a verified tutor on Stutor',
                        message=plain_message,
                        from_email='help.stutor@gmail.com',
                        recipient_list=[obj.author.email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                except Exception as e:
                    self.message_user(request, f"Error sending verification email: {str(e)}", level='ERROR')
                else:
                    self.message_user(request, f"Verification email sent to {obj.author.email}")
        
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """Handle single object deletion"""
        self._send_deletion_email(request, obj)
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        """Handle bulk deletion"""
        for obj in queryset:
            self._send_deletion_email(request, obj)
        super().delete_queryset(request, queryset)

    def _send_deletion_email(self, request, obj):
        """Helper method to send appropriate deletion email"""
        try:
            if obj.verified:
                template = 'users/account_deletion_email.html'
                subject = 'Your Stutor Account Has Been Deleted'
            else:
                template = 'users/rejection_email.html'
                subject = 'Stutor Application Status'

            html_message = render_to_string(template, {
                'tutor': obj,
            })
            plain_message = strip_tags(html_message)

            send_mail(
                subject=subject,
                message=plain_message,
                from_email='help.stutor@gmail.com',
                recipient_list=[obj.author.email],
                html_message=html_message,
                fail_silently=False,
            )
            self.message_user(
                request, 
                f"Notification email sent to {obj.author.email}",
                messages.SUCCESS
            )
        except Exception as e:
            self.message_user(
                request,
                f"Error sending notification email to {obj.author.email}: {str(e)}",
                messages.ERROR
            )

@admin.register(subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}