#from django.http import HttpResponse
from django.shortcuts import render, redirect
# Import the School model
from users.models import School # Assuming School is in your users app models.py

# views for the homepage
def homepage(request):
    # If a school is selected, redirect to that school's page
    school_slug = request.GET.get('school_slug')
    if school_slug:
        return redirect(f'/{school_slug}/')

    # Fetch all school objects from the database
    all_schools = School.objects.all()

    # Prepare the context to pass to the template
    context = {
        'schools': all_schools, # Pass the list of schools to the template
        # Add any other context variables your homepage needs
        # 'some_other_data': value,
    }

    # Render the homepage template, passing the context
    return render(request, 'home.html', context) # Make sure 'home.html' is the correct template path

