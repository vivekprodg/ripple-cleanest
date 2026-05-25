from __future__ import annotations

from typing import Any

from django.contrib import messages
from django.shortcuts import redirect, render

from .models import ContactInquiry, ContactPageSettings


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _image_url(field_file) -> str:
    try:
        if field_file and getattr(field_file, "url", ""):
            return field_file.url
    except Exception:
        pass
    return ""


def _get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") or ""


def contact_page(request):
    settings = ContactPageSettings.get_solo()

    if request.method == "POST":
        ContactInquiry.objects.create(
            full_name=_safe_text(request.POST.get("full_name")),
            email_address=_safe_text(request.POST.get("email_address")),
            phone_number=_safe_text(request.POST.get("phone_number")),
            project_details=_safe_text(request.POST.get("project_details")),
            source_page=request.path,
            ip_address=_get_client_ip(request),
            user_agent=_safe_text(request.META.get("HTTP_USER_AGENT")),
        )

        success_message = _safe_text(settings.success_message)
        if success_message:
            messages.success(request, success_message)

        return redirect("contact:contact")

    top_cards = list(settings.top_cards.filter(is_active=True).order_by("sort_order", "id"))
    info_boxes = list(settings.info_boxes.filter(is_active=True).order_by("sort_order", "id"))
    social_links = list(settings.social_links.filter(is_active=True).order_by("sort_order", "id"))

    context = {
        "page_settings": settings,
        "page_title": _safe_text(settings.page_title),
        "seo_title": _safe_text(settings.seo_title),
        "seo_description": _safe_text(settings.seo_description),
        "hero_badge": _safe_text(settings.hero_badge),
        "hero_title": _safe_text(settings.hero_title),
        "hero_description": _safe_text(settings.hero_description),
        "hero_background_image_url": _image_url(settings.hero_background_image),
        "hero_overlay_strength": settings.hero_overlay_strength if settings.hero_overlay_strength is not None else "",
        "top_cards_heading": _safe_text(settings.top_cards_heading),
        "top_cards_subheading": _safe_text(settings.top_cards_subheading),
        "top_cards": top_cards,
        "left_section_badge": _safe_text(settings.left_section_badge),
        "left_section_title": _safe_text(settings.left_section_title),
        "left_section_description": _safe_text(settings.left_section_description),
        "left_section_background_image_url": _image_url(settings.left_section_background_image),
        "info_boxes": info_boxes,
        "form_title": _safe_text(settings.form_title),
        "form_subtitle": _safe_text(settings.form_subtitle),
        "submit_button_text": _safe_text(settings.submit_button_text),
        "success_message_text": _safe_text(settings.success_message),
        "map_title": _safe_text(settings.map_title),
        "map_description": _safe_text(settings.map_description),
        "map_embed_url": _safe_text(settings.map_embed_url),
        "map_location_text": _safe_text(settings.map_location_text),
        "contact_email": _safe_text(settings.contact_email),
        "contact_phone": _safe_text(settings.contact_phone),
        "contact_location": _safe_text(settings.contact_location),
        "contact_address": _safe_text(settings.contact_address),
        "social_heading": _safe_text(settings.social_heading),
        "social_links": social_links,
    }

    return render(request, "contact/contact.html", context)