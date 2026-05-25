from django.urls import path
from .views import projects_page

urlpatterns = [
    path('', projects_page, name='projects'),
]