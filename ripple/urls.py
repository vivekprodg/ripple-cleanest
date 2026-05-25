from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # ADMIN PANEL
    path("admin/", admin.site.urls),

    # CORE APP (global utilities, APIs, shared logic)
    path("core/", include("core.urls")),

    # HOME PAGE
    path("", include("home.urls")),

    # PROJECTS PAGE
    path("projects/", include("projects.urls")),

    # ABOUT PAGE
    path("about/", include("about.urls")),

    # SERVICES PAGE
    path("services/", include("services.urls")),

    # INTERIOR PAGE
    path("interior/", include("interior.urls")),

    # CONTACT PAGE
    path("contact/", include("contact.urls")),

    # BLOG CMS (FULLY DYNAMIC)
    # - Listing: /blogs/
    # - Detail:  /blogs/<slug>/
    path("blogs/", include("blogs.urls")),

    # REQUEST QUOTE
    path("request_quote/", include("quote.urls")),

    # LEAD CRM
    path("lead/", include("lead.urls")),
]

# MEDIA & STATIC FILES (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)