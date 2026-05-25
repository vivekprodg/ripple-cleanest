from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from lead.services import create_lead

from .models import RFQDropdownGroup, RFQDropdownOption, QuoteHeroSection


# Canonical CMS keys expected by the views.
# These match the intended slug-style structure in models.py/admin.py.
RFQ_GROUP_KEYS = {
    "typology": ("Project_Typology", "Project Typology", "Typology"),
    "site_status": ("Site_Status", "Site Status", "SiteStatus"),
    "services": ("Services", "Service"),
    "budget": ("Budget",),
    "referral": ("Referral",),
}


def _candidate_terms(*terms):
    """
    Build a de-duplicated list of safe lookup variants for each term.
    This helps the view resolve both canonical slug keys and older CMS values.
    """
    candidates = []
    seen = set()

    for term in terms:
        if not term:
            continue

        raw = str(term).strip()
        if not raw:
            continue

        variants = {
            raw,
            slugify(raw),
            raw.replace("_", " ").strip(),
            slugify(raw.replace("_", " ").strip()),
        }

        for variant in variants:
            variant = (variant or "").strip()
            if variant and variant not in seen:
                seen.add(variant)
                candidates.append(variant)

    return candidates


def _get_group_by_keys(*keys):
    """
    Resolve an RFQDropdownGroup by matching against key/title using
    canonical and legacy lookup variants.
    """
    candidates = _candidate_terms(*keys)

    query = Q()
    for candidate in candidates:
        query |= Q(key__iexact=candidate)
        query |= Q(title__iexact=candidate)

    return (
        RFQDropdownGroup.objects
        .filter(query, is_active=True)
        .prefetch_related("options")
        .order_by("order", "id")
        .first()
    )


def _get_active_options(group_key):
    """
    Return active RFQ dropdown options for a given group key.
    Falls back to legacy/admin-entered group names when needed.
    """
    aliases = RFQ_GROUP_KEYS.get(group_key, ())
    group = _get_group_by_keys(group_key, *aliases)

    if not group:
        return RFQDropdownOption.objects.none()

    return (
        group.options
        .filter(is_active=True)
        .order_by("order", "id")
    )


def _get_active_quote_hero():
    """
    Returns the first active hero section ordered by CMS order.
    Falls back to the latest available record if no active one exists.
    """
    hero = (
        QuoteHeroSection.objects
        .filter(is_active=True)
        .order_by("order", "-created_at", "id")
        .first()
    )

    if hero:
        return hero

    return (
        QuoteHeroSection.objects
        .order_by("order", "-created_at", "id")
        .first()
    )


def _build_rfq_notes(
    typology="",
    site_status="",
    services="",
    budget="",
    referral="",
    location="",
    scale="",
    vision_narrative="",
):
    """
    Keep RFQ-specific details available even though RFQLead is removed.
    These details are stored inside the shared Lead notes field.
    """
    parts = []

    if typology:
        parts.append(f"Typology: {typology}")
    if site_status:
        parts.append(f"Site Status: {site_status}")
    if services:
        parts.append(f"Services: {services}")
    if budget:
        parts.append(f"Budget: {budget}")
    if referral:
        parts.append(f"Referral: {referral}")
    if location:
        parts.append(f"Location: {location}")
    if scale:
        parts.append(f"Scale: {scale}")
    if vision_narrative:
        parts.append("")
        parts.append("Message:")
        parts.append(vision_narrative)

    return "\n".join(parts).strip()


def request_quote_view(request):
    context = {
        "quote_hero": _get_active_quote_hero(),
        "typologies": _get_active_options("typology"),
        "site_statuses": _get_active_options("site_status"),
        "services": _get_active_options("services"),
        "budgets": _get_active_options("budget"),
        "referrals": _get_active_options("referral"),
    }
    return render(request, "quote/request_quote.html", context)


@csrf_exempt
def submit_rfq(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    typology = (request.POST.get("typology") or "").strip()
    site_status = (request.POST.get("site_status") or "").strip()
    services = (request.POST.get("services") or "").strip()
    budget = (request.POST.get("budget") or "").strip()
    referral = (request.POST.get("referral") or "").strip()

    location = (request.POST.get("location") or "").strip()
    scale = (request.POST.get("scale") or "").strip()
    vision_narrative = (request.POST.get("vision_narrative") or "").strip()

    name = (request.POST.get("principal_name") or "").strip()
    email = (request.POST.get("principal_email") or "").strip()
    phone = (request.POST.get("principal_phone") or "").strip()

    # RFQLead is removed completely.
    # RFQ now creates a shared Lead record directly.
    rfq_notes = _build_rfq_notes(
        typology=typology,
        site_status=site_status,
        services=services,
        budget=budget,
        referral=referral,
        location=location,
        scale=scale,
        vision_narrative=vision_narrative,
    )

    lead = create_lead(
        name=name,
        email=email,
        phone=phone,
        lead_type="quote",
        source="quote",
        status="new",
        priority="warm",
        project=typology,
        location=location,
        budget=budget,
        notes=rfq_notes,
    )

    studio_email = (
        getattr(settings, "RFQ_STUDIO_EMAIL", None)
        or getattr(settings, "DEFAULT_FROM_EMAIL", None)
    )

    # Email to studio / internal team.
    if studio_email:
        send_mail(
            subject="New RFQ Lead Received",
            message=f"""
New Lead:

Name: {lead.name or "-"}
Email: {lead.email or "-"}
Phone: {lead.phone or "-"}

Typology: {typology or "-"}
Site Status: {site_status or "-"}
Services: {services or "-"}
Budget: {budget or "-"}
Referral: {referral or "-"}

Location: {location or "-"}
Scale: {scale or "-"}

Message:
{vision_narrative or "-"}
            """.strip(),
            from_email=studio_email,
            recipient_list=[studio_email],
            fail_silently=True,
        )

    # Confirmation email to client only when email exists.
    if lead.email and studio_email:
        send_mail(
            subject="We Received Your Architecture Brief",
            message=f"""
Dear {lead.name or "Client"},

We have received your project brief.
Our studio will review it and contact you shortly.

— Ripple Architecture
            """.strip(),
            from_email=studio_email,
            recipient_list=[lead.email],
            fail_silently=True,
        )

    return JsonResponse(
        {
            "status": "success",
            "message": "RFQ submitted successfully.",
            "lead_id": lead.id,
        }
    )