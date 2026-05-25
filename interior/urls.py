from django.urls import path
from . import views

urlpatterns = [
    path("", views.interior_page, name="interior"),
]