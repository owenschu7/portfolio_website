from django.urls import path
from . import views

urlpatterns = [
    path('', views.gRPC_view, name='demo_page'),
]
