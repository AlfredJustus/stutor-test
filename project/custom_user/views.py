"""
This file handles everything related to user accounts and login.
It controls:
1. The registration process:
   - When new users sign up
   - Sending verification emails
   - Making sure users verify their email before they can log in
2. The login process:
   - Checking if email and password are correct
   - Remembering which school the user belongs to
   - Taking users to the right page after they log in
3. The logout process
4. Email verification when users click the link in their email
This is where all the account-related stuff happens.
"""

# importiert alle nötigen packages von Django
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout, get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from .tokens import account_activation_token
from django.urls import reverse
from users.models import School

# Email address used for system notifications and tutor communications
ADMIN_EMAIL = 'help.stutor@gmail.com'

def register_view(request): 
    """
    Handles user registration with school association.
    Flow:
    1. User submits registration form
    2. If valid, creates inactive user account
    3. Associates user with school from session
    4. Sends verification email
    5. Redirects to verification page
    """
    if request.method == "POST": 
        form = CustomUserCreationForm(request.POST)
        if form.is_valid(): 
            # Create user but don't save to database yet
            user = form.save(commit=False)
            user.is_active = False  # User must verify email before activation
            
            # Associate user with school from session
            active_school_slug = request.session.get('active_school_slug')
            if active_school_slug:
                try:
                    school = School.objects.get(slug=active_school_slug)
                    user.school = school
                except School.DoesNotExist:
                    pass
            
            user.save()
            # Send verification email
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect("custom_user:verify-please")
    else:   
        form = CustomUserCreationForm()
        # If coming from a school-specific page, store school info
        if request.GET.get('next'):
            next_url = request.GET.get('next')
            school_slug = next_url.split('/')[1]  # Extract school slug from URL
            request.session['active_school_slug'] = school_slug
    return render(request, 'custom_user/register.html', {"form": form})

def activateEmail(request, user, to_email):
    """
    Sends account verification email to new users.
    Email contains a unique token that must be clicked to activate the account.
    """
    # Generate verification link with user's ID and token
    text_content = render_to_string(
        "custom_user/activate_account.txt",
        context={
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        },
    )

    # HTML version of the email
    html_content = render_to_string(
        "custom_user/template_activate_account.html",
        context={
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        },
    )

    # Send multipart email (both text and HTML versions)
    msg = EmailMultiAlternatives(
        "stutor: Please verify your email",
        text_content,
        ADMIN_EMAIL,
        [to_email],
        headers={"List-Unsubscribe": "<mailto:unsub@example.com>"},
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def activate(request, uidb64, token):
    """
    Handles email verification process.
    When user clicks verification link in email:
    1. Decodes user ID from URL
    2. Verifies token is valid
    3. Activates user account if everything checks out
    """
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('custom_user:successful-email-verification')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('/')

def login_view(request):
    """
    Handles user login with school context.
    Flow:
    1. User submits login form
    2. If valid, logs in user
    3. Sets active school in session
    4. Redirects to:
       - 'next' URL if provided
       - User's school page if user has a school
       - Homepage as fallback
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Set active school in session if user has one
            if user.school:
                request.session['active_school_slug'] = user.school.slug

            # Handle redirect after login
            next_url = request.GET.get('next')
            if not next_url:
                next_url = request.POST.get('next')

            if next_url:
                return redirect(next_url)
            else:
                # Default redirect based on user's school
                if user.school:
                    return redirect(f'/{user.school.slug}/')
                return redirect('/')

    else:
        form = AuthenticationForm()

    return render(request, 'custom_user/login.html', {"form": form})

def logout_view(request):
    """Handles user logout and redirects to homepage."""
    if request.method == "POST":
        logout(request)
        return redirect("/")

def verify_view(request):
    """Renders the email verification pending page."""
    return render(request, 'custom_user/verify-please.html')

def verification_successful_view(request):
    """Renders the successful email verification page."""
    return render(request, 'custom_user/successful-email-verification.html')

def registration_information(request):
    """Renders the registration information page with release forms."""
    return render(request, 'custom_user/registration-information.html')

