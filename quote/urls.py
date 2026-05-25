from django.urls import path
from . import views

app_name = "quote"

urlpatterns = [
    # RFQ form page
    path("", views.request_quote_view, name="request_quote"),

    # RFQ submission endpoint
    # This route stays here; the view is the wrapper that creates a unified Lead.
    path("submit/", views.submit_rfq, name="submit"),
]