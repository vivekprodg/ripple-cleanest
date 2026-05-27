from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q

from .models import Lead


def normalize_text(value):
    """
    Normalize a text value for safe storage.

    - None -> ""
    - strips surrounding whitespace
    - converts non-string values to string
    """
    if value is None:
        return ""
    return str(value).strip()


def parse_tags(value):
    """
    Convert tags input into a clean list.

    Accepts:
    - list/tuple/set
    - comma-separated string
    - None

    Returns a list of stripped non-empty tag strings.
    """
    if not value:
        return []

    if isinstance(value, (list, tuple, set)):
        return [str(tag).strip() for tag in value if str(tag).strip()]

    if isinstance(value, str):
        return [tag.strip() for tag in value.split(",") if tag.strip()]

    return []


def _to_bool(value):
    """
    Convert common truthy/falsey values safely.
    """
    if value in (True, False):
        return value

    if value is None:
        return False

    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}

    return bool(value)


def _pick_first_non_empty(data, *keys, default=""):
    """
    Return the first non-empty value from a dict using multiple possible keys.
    """
    if not data:
        return default

    for key in keys:
        if key not in data:
            continue
        value = data.get(key)
        if value not in (None, ""):
            return value

    return default


def lead_defaults():
    """
    Default lead payload with empty, optional-friendly values.
    Useful for initial forms or programmatic creation.
    """
    return {
        "name": "",
        "email": "",
        "phone": "",
        "lead_type": Lead.LeadType.WEBSITE,
        "status": Lead.LeadStatus.NEW,
        "priority": Lead.LeadPriority.COLD,
        "source": Lead.LeadSource.WEBSITE,
        "budget": "",
        "project": "",
        "location": "",
        "timeline": "",
        "typology": "",
        "site_status": "",
        "services": "",
        "referral": "",
        "scale": "",
        "vision_narrative": "",
        "avatar": "",
        "notes": "",
        "tags": [],
        "is_subscriber": False,
        "is_archived": False,
        "is_deleted": False,
    }


def clean_lead_data(data):
    """
    Normalize incoming lead data.

    This is intentionally permissive:
    - no field is required
    - unknown keys are ignored
    - empty values are preserved as safe defaults
    - common aliases from contact/RFQ forms are accepted
    """
    cleaned = lead_defaults()

    if not data:
        return cleaned

    alias_map = {
        "name": ("name", "full_name", "principal_name"),
        "email": ("email", "email_address", "principal_email"),
        "phone": ("phone", "phone_number", "principal_phone"),
        "lead_type": ("lead_type",),
        "status": ("status",),
        "priority": ("priority",),
        "source": ("source",),
        "budget": ("budget",),
        "project": ("project", "subject", "service", "typology", "project_type", "lead_project"),
        "location": ("location",),
        "timeline": ("timeline",),
        "typology": ("typology", "project", "project_type", "lead_project"),
        "site_status": ("site_status",),
        "services": ("services",),
        "referral": ("referral",),
        "scale": ("scale",),
        "vision_narrative": ("vision_narrative", "message", "notes", "description", "project_details"),
        "avatar": ("avatar",),
        "notes": ("notes", "message", "description", "project_details", "vision_narrative"),
        "tags": ("tags",),
        "is_subscriber": ("is_subscriber",),
        "is_archived": ("is_archived",),
        "is_deleted": ("is_deleted",),
    }

    for key in cleaned.keys():
        value = _pick_first_non_empty(data, *alias_map.get(key, (key,)), default=None)

        if value is None and key not in data:
            continue

        if key == "tags":
            cleaned[key] = parse_tags(value)
        elif key in {"is_subscriber", "is_archived", "is_deleted"}:
            cleaned[key] = _to_bool(value)
        elif key in {
            "name",
            "email",
            "phone",
            "lead_type",
            "status",
            "priority",
            "source",
            "budget",
            "project",
            "location",
            "timeline",
            "typology",
            "site_status",
            "services",
            "referral",
            "scale",
            "vision_narrative",
            "avatar",
            "notes",
        }:
            cleaned[key] = normalize_text(value)
        else:
            cleaned[key] = value

    return cleaned


@transaction.atomic
def create_lead(**data):
    """
    Create a Lead using optional, normalized data.

    Used by RFQ, contact, website, ad, WhatsApp, subscription, and manual lead entry.
    """
    cleaned = clean_lead_data(data)

    lead = Lead.objects.create(
        name=cleaned["name"],
        email=cleaned["email"],
        phone=cleaned["phone"],
        lead_type=cleaned["lead_type"] or Lead.LeadType.WEBSITE,
        status=cleaned["status"] or Lead.LeadStatus.NEW,
        priority=cleaned["priority"] or Lead.LeadPriority.COLD,
        source=cleaned["source"] or Lead.LeadSource.WEBSITE,
        budget=cleaned["budget"],
        project=cleaned["project"],
        location=cleaned["location"],
        timeline=cleaned["timeline"],
        typology=cleaned["typology"],
        site_status=cleaned["site_status"],
        services=cleaned["services"],
        referral=cleaned["referral"],
        scale=cleaned["scale"],
        vision_narrative=cleaned["vision_narrative"],
        avatar=cleaned["avatar"],
        notes=cleaned["notes"],
        tags=cleaned["tags"],
        is_subscriber=cleaned["is_subscriber"],
        is_archived=cleaned["is_archived"],
        is_deleted=cleaned["is_deleted"],
    )
    return lead


@transaction.atomic
def update_lead(lead, **data):
    """
    Update an existing Lead with optional data.

    Only recognized fields are applied.
    """
    if lead is None:
        return None

    cleaned = clean_lead_data(data)

    for field in (
        "name",
        "email",
        "phone",
        "lead_type",
        "status",
        "priority",
        "source",
        "budget",
        "project",
        "location",
        "timeline",
        "typology",
        "site_status",
        "services",
        "referral",
        "scale",
        "vision_narrative",
        "avatar",
        "notes",
        "is_subscriber",
        "is_archived",
        "is_deleted",
    ):
        value = cleaned.get(field)
        if value is not None:
            setattr(lead, field, value)

    if "tags" in cleaned:
        lead.tags = cleaned["tags"]

    lead.save()
    return lead


def set_status(lead, status):
    """
    Set a lead's status and save it.
    """
    if lead is None:
        return None

    lead.status = status or Lead.LeadStatus.NEW
    lead.save(update_fields=["status", "updated_at"])
    return lead


def set_priority(lead, priority):
    """
    Set a lead's priority and save it.
    """
    if lead is None:
        return None

    lead.priority = priority or Lead.LeadPriority.COLD
    lead.save(update_fields=["priority", "updated_at"])
    return lead


def set_source(lead, source):
    """
    Set a lead's source and save it.
    """
    if lead is None:
        return None

    lead.source = source or Lead.LeadSource.WEBSITE
    lead.save(update_fields=["source", "updated_at"])
    return lead


def archive_lead(lead):
    """
    Mark a lead as archived.
    """
    if lead is None:
        return None

    lead.is_archived = True
    lead.save(update_fields=["is_archived", "updated_at"])
    return lead


def unarchive_lead(lead):
    """
    Remove archived state from a lead.
    """
    if lead is None:
        return None

    lead.is_archived = False
    lead.save(update_fields=["is_archived", "updated_at"])
    return lead


def delete_lead(lead):
    """
    Soft-delete a lead.
    """
    if lead is None:
        return None

    lead.is_deleted = True
    lead.save(update_fields=["is_deleted", "updated_at"])
    return lead


def restore_lead(lead):
    """
    Restore a soft-deleted lead.
    """
    if lead is None:
        return None

    lead.is_deleted = False
    lead.save(update_fields=["is_deleted", "updated_at"])
    return lead


def get_base_queryset():
    """
    Base queryset for app usage.

    By default this excludes deleted records but keeps archived leads.
    """
    return Lead.objects.all().order_by("-created_at", "-id")


def get_active_queryset():
    """
    Non-deleted leads only.
    """
    return get_base_queryset().filter(is_deleted=False)


def get_board_queryset(include_deleted=False, include_archived=True):
    """
    Queryset suitable for board/list views.

    - excludes deleted by default
    - optionally excludes archived
    """
    qs = get_base_queryset()

    if not include_deleted:
        qs = qs.filter(is_deleted=False)

    if not include_archived:
        qs = qs.filter(is_archived=False)

    return qs


def apply_filters(
    queryset,
    search=None,
    lead_type=None,
    status=None,
    priority=None,
    source=None,
    is_archived=None,
    is_deleted=None,
):
    """
    Apply flexible filtering to a lead queryset.

    All parameters are optional.
    """
    if queryset is None:
        queryset = get_base_queryset()

    if search:
        search = normalize_text(search)
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
            | Q(project__icontains=search)
            | Q(location__icontains=search)
            | Q(notes__icontains=search)
            | Q(budget__icontains=search)
            | Q(timeline__icontains=search)
            | Q(typology__icontains=search)
            | Q(site_status__icontains=search)
            | Q(services__icontains=search)
            | Q(referral__icontains=search)
            | Q(scale__icontains=search)
            | Q(vision_narrative__icontains=search)
        )

    if lead_type:
        queryset = queryset.filter(lead_type=lead_type)

    if status:
        queryset = queryset.filter(status=status)

    if priority:
        queryset = queryset.filter(priority=priority)

    if source:
        queryset = queryset.filter(source=source)

    if is_archived is not None:
        queryset = queryset.filter(is_archived=bool(is_archived))

    if is_deleted is not None:
        queryset = queryset.filter(is_deleted=bool(is_deleted))

    return queryset


def get_lead_stats(queryset=None):
    """
    Return a simple stats payload for dashboards / boards.

    Output shape:
    {
        "total": 0,
        "new": 0,
        "contacted": 0,
        "won": 0,
        "lost": 0,
        "archived": 0,
        "deleted": 0,
        "conversion_rate": 0
    }
    """
    if queryset is None:
        queryset = get_active_queryset()

    total = queryset.count()
    new_count = queryset.filter(status=Lead.LeadStatus.NEW).count()
    contacted_count = queryset.filter(status=Lead.LeadStatus.CONTACTED).count()
    won_count = queryset.filter(status=Lead.LeadStatus.WON).count()
    lost_count = queryset.filter(status=Lead.LeadStatus.LOST).count()
    archived_count = queryset.filter(is_archived=True).count()
    deleted_count = queryset.filter(is_deleted=True).count()

    conversion_rate = 0
    if total > 0:
        conversion_rate = round((won_count / total) * 100)

    return {
        "total": total,
        "new": new_count,
        "contacted": contacted_count,
        "won": won_count,
        "lost": lost_count,
        "archived": archived_count,
        "deleted": deleted_count,
        "conversion_rate": conversion_rate,
    }


def group_leads_by_status(queryset=None):
    """
    Return leads grouped by status for board-style UIs.
    """
    if queryset is None:
        queryset = get_active_queryset()

    return {
        Lead.LeadStatus.NEW: queryset.filter(status=Lead.LeadStatus.NEW),
        Lead.LeadStatus.CONTACTED: queryset.filter(status=Lead.LeadStatus.CONTACTED),
        Lead.LeadStatus.WON: queryset.filter(status=Lead.LeadStatus.WON),
        Lead.LeadStatus.LOST: queryset.filter(status=Lead.LeadStatus.LOST),
    }


def search_leads(term):
    """
    Convenience search helper.
    """
    if not term:
        return get_active_queryset()

    return apply_filters(get_active_queryset(), search=term)


def get_lead_by_id(lead_id, include_deleted=False):
    """
    Fetch a lead by primary key.

    By default deleted records are hidden.
    """
    qs = Lead.objects.all()
    if not include_deleted:
        qs = qs.filter(is_deleted=False)
    return qs.filter(pk=lead_id).first()


def update_lead_notes(lead, notes):
    """
    Update notes only.
    """
    if lead is None:
        return None

    lead.notes = normalize_text(notes)
    lead.save(update_fields=["notes", "updated_at"])
    return lead


def update_lead_tags(lead, tags):
    """
    Update tags only.
    """
    if lead is None:
        return None

    lead.tags = parse_tags(tags)
    lead.save(update_fields=["tags", "updated_at"])
    return lead


def _subscription_subject(lead):
    company_name = getattr(settings, "SITE_NAME", None) or getattr(
        settings, "PROJECT_NAME", None
    ) or "Ripple Cleanest"
    return f"Subscription confirmed — {company_name}"


def _subscription_message(lead):
    company_name = getattr(settings, "SITE_NAME", None) or getattr(
        settings, "PROJECT_NAME", None
    ) or "Ripple Cleanest"

    subscriber_name = lead.display_name if getattr(lead, "name", "") else "Subscriber"

    return (
        f"Hello {subscriber_name},\n\n"
        f"Thanks for subscribing to {company_name}.\n"
        f"We have received your email: {lead.email}.\n\n"
        f"You will now receive our architectural insights and updates.\n\n"
        f"Best regards,\n"
        f"{company_name}"
    )


@transaction.atomic
def create_subscription_lead(email, name="", send_confirmation=True, notify_admin=False):
    """
    Create a subscription lead and optionally send emails.

    Recommended use after footer newsletter form submission.
    """
    lead = create_lead(
        name=name or "Newsletter Subscriber",
        email=email,
        phone="",
        lead_type=Lead.LeadType.SUBSCRIPTION,
        status=Lead.LeadStatus.NEW,
        priority=Lead.LeadPriority.COLD,
        source=Lead.LeadSource.SUBSCRIPTION,
        budget="",
        project="Newsletter Subscription",
        location="",
        timeline="",
        typology="",
        site_status="",
        services="",
        referral="",
        scale="",
        vision_narrative="",
        avatar="",
        notes="Subscribed from website footer subscription form.",
        tags=["subscription", "newsletter"],
        is_subscriber=True,
        is_archived=False,
        is_deleted=False,
    )

    if send_confirmation:
        send_subscription_confirmation_email(lead)

    if notify_admin:
        send_subscription_admin_notification(lead)

    return lead


def send_subscription_confirmation_email(lead):
    """
    Send a confirmation email to the subscriber.

    Returns True when Django reports a successful send.
    """
    if lead is None or not lead.email:
        return False

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(
        settings, "EMAIL_HOST_USER", None
    ) or "no-reply@example.com"

    return send_mail(
        subject=_subscription_subject(lead),
        message=_subscription_message(lead),
        from_email=from_email,
        recipient_list=[lead.email],
        fail_silently=True,
    ) > 0


def send_subscription_admin_notification(lead):
    """
    Optional admin notification for a new subscription lead.
    """
    if lead is None or not lead.email:
        return False

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(
        settings, "EMAIL_HOST_USER", None
    ) or "no-reply@example.com"

    admin_email = getattr(settings, "SUBSCRIPTION_NOTIFICATION_EMAIL", None) or getattr(
        settings, "DEFAULT_FROM_EMAIL", None
    )

    if not admin_email:
        return False

    subject = "New footer subscription lead"
    message = (
        f"A new newsletter subscription was captured.\n\n"
        f"Name: {lead.name}\n"
        f"Email: {lead.email}\n"
        f"Created: {lead.created_at}\n"
    )

    return send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[admin_email],
        fail_silently=True,
    ) > 0