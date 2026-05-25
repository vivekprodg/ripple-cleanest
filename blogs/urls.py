from django.urls import path
from .views import blog_page, blog_detail

app_name = "blogs"

urlpatterns = [
    # -----------------------------
    # BLOG LISTING PAGE (CMS DRIVEN)
    # -----------------------------
    path(
        "",
        blog_page,
        name="blog_page",
    ),

    # -----------------------------
    # BLOG DETAIL PAGE (CMS DRIVEN VIA SLUG)
    # -----------------------------
    path(
        "<slug:slug>/",
        blog_detail,
        name="blog_detail",
    ),
]