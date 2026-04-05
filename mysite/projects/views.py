from django.shortcuts import render, get_object_or_404
from .models import Project

# Create your views here.
def project_detail(request, pk):
    # get_object_or_404 is a great safety net. If someone types in a URL
    # for project #99, but you only have 3 projects, it shows a clean 404 page
    # instead of crashing the server
    project = get_object_or_404(Project, pk=pk)

    return render(request, 'projects/project_detail.html', {'project': project})

def projects_page(request):
    # grab all the projects from the database
    my_projects = Project.objects.all()

    # hand my_projects to the template in a context dictinoary
    return render(request, 'projects/projects_page.html', {'projects': my_projects})


