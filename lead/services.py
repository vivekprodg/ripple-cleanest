from __future__ import annotations

import datetime as dt

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import Lead

User = get_user_model()


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


def _parse_int(value):
    """
    Parse an integer safely.
    """
    if value in (None, ""):
        return None

    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _parse_datetime_value(value):
    """
    Parse a datetime value safely from string/datetime input.
    """
    if value in (None, ""):
        return None

    if isinstance(value, dt.datetime):
        if timezone.is_naive(value):
            try:
                return timezone.make_aware(value, timezone.get_current_timezone())
            except Exception:
                return value
        return value

    if isinstance(value, str):
        parsed = parse_datetime(value.strip())
        if parsed is None:
            return None
        if timezone.is_naive(parsed):
            try:
                return timezone.make_aware(parsed, timezone.get_current_timezone())
            except Exception:
                return parsed
        return parsed

    return None


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


def _company_name():
    return (
        getattr(settings, "SITE_NAME", None)
        or getattr(settings, "PROJECT_NAME", None)
        or "Ripple Cleanest"
    )


def _from_email():
    return (
        getattr(settings, "DEFAULT_FROM_EMAIL", None)
        or getattr(settings, "EMAIL_HOST_USER", None)
        or "no-reply@example.com"
    )


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
        "assigned_to_id": None,
        "supervisor_id": None,
        "assigned_at": None,
        "last_followup_at": None,
        "next_followup_at": None,
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
        "assigned_to_id": ("assigned_to_id", "assigned_to"),
        "supervisor_id": ("supervisor_id", "supervisor"),
        "assigned_at": ("assigned_at",),
        "last_followup_at": ("last_followup_at",),
        "next_followup_at": ("next_followup_at",),
    }

    for key in cleaned.keys():
        value = _pick_first_non_empty(data, *alias_map.get(key, (key,)), default=None)

        if value is None and key not in data:
            continue

        if key == "tags":
            cleaned[key] = parse_tags(value)
        elif key in {"is_subscriber", "is_archived", "is_deleted"}:
            cleaned[key] = _to_bool(value)
        elif key in {"assigned_to_id", "supervisor_id"}:
            cleaned[key] = _parse_int(value)
        elif key in {"assigned_at", "last_followup_at", "next_followup_at"}:
            cleaned[key] = _parse_datetime_value(value)
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


def _apply_assignment_defaults(lead):
    """
    Ensure assigned_at is populated when assignment exists.
    """
    if lead is None:
        return lead

    if lead.assigned_to_id and not lead.assigned_at:
        lead.assigned_at = timezone.now()

    return lead


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
        assigned_to_id=cleaned["assigned_to_id"],
        supervisor_id=cleaned["supervisor_id"],
        assigned_at=cleaned["assigned_at"],
        last_followup_at=cleaned["last_followup_at"],
        next_followup_at=cleaned["next_followup_at"],
    )

    _apply_assignment_defaults(lead)

    if lead.assigned_at and lead.pk:
        lead.save(update_fields=["assigned_at"])

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
        "assigned_at",
        "last_followup_at",
        "next_followup_at",
    ):
        value = cleaned.get(field)
        if value is not None:
            setattr(lead, field, value)

    if cleaned.get("assigned_to_id", None) is not None:
        lead.assigned_to_id = cleaned["assigned_to_id"]

    if cleaned.get("supervisor_id", None) is not None:
        lead.supervisor_id = cleaned["supervisor_id"]

    if "tags" in cleaned:
        lead.tags = cleaned["tags"]

    _apply_assignment_defaults(lead)
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


def _lead_assignment_subject_staff():
    return "New Lead Assigned"


def _lead_assignment_subject_supervisor():
    return "Lead Assignment Notification"


def _lead_assignment_message_staff(lead):
    assigned_to = getattr(lead, "assigned_to", None)

    return (
        f"Lead Name: {lead.display_name}\n"
        f"Contact: {lead.phone or '—'}\n"
        f"Email: {lead.email or '—'}\n\n"
        f"Please follow up.\n"
        f"\n"
        f"Assigned To: {assigned_to.get_full_name() if assigned_to and hasattr(assigned_to, 'get_full_name') else getattr(assigned_to, 'username', '') if assigned_to else ''}\n"
        f"Assigned At: {lead.assigned_at or '—'}\n"
    )


def _lead_assignment_message_supervisor(lead):
    assigned_to = getattr(lead, "assigned_to", None)
    assigned_name = ""
    if assigned_to:
        full_name = ""
        if hasattr(assigned_to, "get_full_name"):
            full_name = (assigned_to.get_full_name() or "").strip()
        assigned_name = full_name or getattr(assigned_to, "username", "") or getattr(assigned_to, "email", "") or "the staff member"

    return (
        f"Lead {lead.display_name} has been assigned to {assigned_name}.\n\n"
        f"Please monitor progress.\n\n"
        f"Lead Contact: {lead.phone or '—'}\n"
        f"Lead Email: {lead.email or '—'}\n"
        f"Assigned At: {lead.assigned_at or '—'}\n"
    )


def _send_mail_safe(subject, message, recipient_list):
    """
    Send email safely. Returns True only when at least one message is sent.
    """
    recipient_list = [email for email in recipient_list if email]
    if not recipient_list:
        return False

    try:
        return (
            send_mail(
                subject=subject,
                message=message,
                from_email=_from_email(),
                recipient_list=recipient_list,
                fail_silently=True,
            )
            > 0
        )
    except Exception:
        return False


def send_lead_assignment_notification(lead):
    """
    Send assignment emails to the assigned staff and supervisor.

    Staff receives:
    - Subject: New Lead Assigned

    Supervisor receives:
    - Subject: Lead Assignment Notification
    """
    if lead is None:
        return False

    sent_any = False

    staff_email = getattr(getattr(lead, "assigned_to", None), "email", "") or ""
    supervisor_email = getattr(getattr(lead, "supervisor", None), "email", "") or ""

    if lead.assigned_to and staff_email:
        sent_any = _send_mail_safe(
            subject=_lead_assignment_subject_staff(),
            message=_lead_assignment_message_staff(lead),
            recipient_list=[staff_email],
        ) or sent_any

    if lead.supervisor and supervisor_email and supervisor_email != staff_email:
        sent_any = _send_mail_safe(
            subject=_lead_assignment_subject_supervisor(),
            message=_lead_assignment_message_supervisor(lead),
            recipient_list=[supervisor_email],
        ) or sent_any

    return sent_any


def _subscription_subject(lead):
    company_name = _company_name()
    return f"Subscription confirmed — {company_name}"


def _subscription_message(lead):
    company_name = _company_name()

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

    return _send_mail_safe(
        subject=_subscription_subject(lead),
        message=_subscription_message(lead),
        recipient_list=[lead.email],
    )


def send_subscription_admin_notification(lead):
    """
    Optional admin notification for a new subscription lead.
    """
    if lead is None or not lead.email:
        return False

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

    return _send_mail_safe(
        subject=subject,
        message=message,
        recipient_list=[admin_email],
    )