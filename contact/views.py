from __future__ import annotations

from typing import Any

from django.contrib import messages
from django.shortcuts import redirect, render

from lead.services import create_lead

from .models import ContactPageSettings


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


def _first_non_empty(data, *keys, default="") -> str:
    for key in keys:
        value = _safe_text(data.get(key))
        if value:
            return value
    return default


def _build_contact_notes(request, message: str) -> str:
    parts = []

    if message:
        parts.append("Message:")
        parts.append(message.strip())

    ip_address = _get_client_ip(request)
    user_agent = _safe_text(request.META.get("HTTP_USER_AGENT"))
    source_page = _safe_text(request.path)

    if source_page:
        parts.append("")
        parts.append(f"Source Page: {source_page}")
    if ip_address:
        parts.append(f"IP Address: {ip_address}")
    if user_agent:
        parts.append(f"User Agent: {user_agent}")

    return "\n".join(parts).strip()


def contact_page(request):
    settings = ContactPageSettings.get_solo()

    if request.method == "POST":
        name = _first_non_empty(request.POST, "full_name", "name", "principal_name")
        email = _first_non_empty(request.POST, "email_address", "email", "principal_email")
        phone = _first_non_empty(request.POST, "phone_number", "phone", "principal_phone")
        message = _first_non_empty(
            request.POST,
            "project_details",
            "message",
            "notes",
            "description",
        )

        project = _first_non_empty(
            request.POST,
            "project",
            "subject",
            "service",
            default="Contact Inquiry",
        )

        lead = create_lead(
            name=name,
            email=email,
            phone=phone,
            lead_type="contact",
            source="contact",
            status="new",
            priority="cold",
            budget="",
            project=project or "Contact Inquiry",
            location="",
            timeline="",
            avatar="",
            notes=_build_contact_notes(request, message),
            tags=["contact", "website"],
            is_archived=False,
            is_deleted=False,
        )

        success_message = _safe_text(settings.success_message)
        if success_message:
            messages.success(request, success_message)
        else:
            messages.success(request, "Thank you. Your message has been received.")

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