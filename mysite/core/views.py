from django.shortcuts import render
from projects.models import Project

# Create your views here.
def home(request):
    # fetch all projects in database
    projects = Project.objects.all()

    # Pass them to the template in a context dictionary
    context = {
        'projects': projects 
    }
    # this renders an html file. send it the context aswell
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

