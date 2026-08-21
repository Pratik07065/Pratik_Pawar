from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('projects/<slug:slug>/', views.project_detail_view, name='project_detail'),
    path('resume/', views.resume_view, name='resume'),
]
