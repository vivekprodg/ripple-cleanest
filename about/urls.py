from django.urls import path
from . import views

app_name = "about"

urlpatterns = [

    # =========================
    # FRONTEND PAGE
    # =========================
    path("", views.about_page, name="about_page"),

    # =========================
    # CMS DASHBOARD ROUTES
    # =========================
    path("dashboard/", views.about_dashboard, name="about_dashboard"),

    path("hero/edit/", views.about_hero_edit, name="about_hero_edit"),

    path("hero/preview/", views.about_hero_preview, name="about_hero_preview"),

    path("preview/", views.about_page_preview, name="about_page_preview"),
]