from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_page, name='projects_page'),

    # the <int:pk> part captures the project's ID number from the URL
    # eg, /projects/1/ and passes it to the view
    path('<int:pk>/', views.project_detail, name='project_detail'),
]
