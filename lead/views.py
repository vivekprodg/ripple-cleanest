from __future__ import annotations

import json
from typing import Any

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Lead
from .services import (
    apply_filters,
    archive_lead,
    create_lead,
    delete_lead,
    get_active_queryset,
    get_base_queryset,
    get_board_queryset,
    get_lead_by_id,
    get_lead_stats,
    group_leads_by_status,
    parse_tags,
    restore_lead,
    set_priority,
    set_source,
    set_status,
    unarchive_lead,
    update_lead,
    update_lead_notes,
    update_lead_tags,
)


def _wants_json(request):
    accept = request.headers.get("Accept", "")
    requested_with = request.headers.get("X-Requested-With", "")
    content_type = request.headers.get("Content-Type", "")
    return (
        "application/json" in accept
        or requested_with == "XMLHttpRequest"
        or content_type.startswith("application/json")
    )


def _payload_from_request(request):
    if request.content_type and request.content_type.startswith("application/json"):
        try:
            return json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return {}
    return request.POST.dict()


def _boolish(value):
    if value in (True, False):
        return value
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _safe_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _get_value(data, *keys, default=""):
    for key in keys:
        if key in data and data.get(key) not in (None, ""):
            return data.get(key)
    return default


def _get_value_str(data, *keys, default=""):
    return _safe_str(_get_value(data, *keys, default=default))


def _normalize_tags(value):
    if value is None or value == "":
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return []
        return parse_tags(stripped)

    return parse_tags(value)


def _request_filters(request):
    """
    Support both backend query params and front-end filter names.
    """
    data = request.GET

    search = data.get("search") or data.get("q") or data.get("searchInput") or ""
    lead_type = data.get("lead_type") or data.get("filterType") or ""
    status = data.get("status") or data.get("filterStatus") or ""
    priority = data.get("priority") or data.get("filterPriority") or ""
    source = data.get("source") or data.get("filterSource") or ""

    is_archived = data.get("is_archived")
    if is_archived is None:
        is_archived = data.get("archived")

    is_deleted = data.get("is_deleted")
    if is_deleted is None:
        is_deleted = data.get("deleted")

    is_archived = _boolish(is_archived)
    is_deleted = _boolish(is_deleted)

    return {
        "search": search.strip() if search else "",
        "lead_type": lead_type.strip() if lead_type else "",
        "status": status.strip() if status else "",
        "priority": priority.strip() if priority else "",
        "source": source.strip() if source else "",
        "is_archived": is_archived,
        "is_deleted": is_deleted,
    }


def _build_intake_notes(data):
    """
    Build a single notes block that can absorb RFQ, contact, website,
    ad, WhatsApp, and future intake payloads without needing a separate model.
    """
    parts = []

    typology = _get_value_str(data, "typology", "project", "project_type", "lead_project")
    site_status = _get_value_str(data, "site_status")
    services = _get_value_str(data, "services")
    budget = _get_value_str(data, "budget")
    referral = _get_value_str(data, "referral")
    location = _get_value_str(data, "location")
    scale = _get_value_str(data, "scale")
    timeline = _get_value_str(data, "timeline")

    message = _get_value_str(
        data,
        "vision_narrative",
        "message",
        "notes",
        "description",
        "project_details",
    )

    if typology:
        parts.append(f"Project: {typology}")
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
    if timeline:
        parts.append(f"Timeline: {timeline}")

    if message:
        parts.append("")
        parts.append("Message:")
        parts.append(message.strip())

    return "\n".join(parts).strip()


def _resolve_lead_type(data):
    """
    Resolve lead type for all intake sources.
    """
    value = _get_value_str(data, "lead_type", "type", "intake_type").lower()
    valid_types = {choice[0] for choice in Lead.LeadType.choices}

    if value in valid_types:
        return value

    source = _get_value_str(data, "source", "lead_source").lower()
    valid_sources = {choice[0] for choice in Lead.LeadSource.choices}

    if source in valid_types:
        return source
    if source in valid_sources:
        return source

    return Lead.LeadType.WEBSITE


def _resolve_source(data, lead_type=None):
    """
    Keep source and lead_type aligned, but allow explicit source override.
    """
    source = _get_value_str(data, "source", "lead_source").lower()
    valid_sources = {choice[0] for choice in Lead.LeadSource.choices}

    if source in valid_sources:
        return source

    lead_type = _safe_str(lead_type).lower()
    if lead_type in valid_sources:
        return lead_type

    return Lead.LeadSource.WEBSITE


def _serialize_lead(lead: Lead):
    return {
        "id": lead.pk,
        "name": lead.name,
        "display_name": lead.display_name,
        "email": lead.email,
        "display_email": lead.display_email,
        "phone": lead.phone,
        "is_subscriber": lead.is_subscriber,
        "lead_type": lead.lead_type,
        "lead_type_label": lead.get_lead_type_display() if lead.lead_type else "",
        "status": lead.status,
        "status_label": lead.get_status_display() if lead.status else "",
        "priority": lead.priority,
        "priority_label": lead.get_priority_display() if lead.priority else "",
        "source": lead.source,
        "source_label": lead.get_source_display() if lead.source else "",
        "budget": lead.budget,
        "project": lead.project,
        "location": lead.location,
        "timeline": lead.timeline,
        "avatar": lead.avatar,
        "notes": lead.notes,
        "tags": lead.tags_list,
        "is_archived": lead.is_archived,
        "is_deleted": lead.is_deleted,
        "created_at": lead.created_at.isoformat() if lead.created_at else None,
        "updated_at": lead.updated_at.isoformat() if lead.updated_at else None,
    }


def _lead_queryset_for_board(request):
    """
    Base board queryset.
    By default we keep archived leads available in the CRM board,
    but deleted leads can be filtered out by query params.
    """
    filters = _request_filters(request)

    queryset = get_board_queryset(
        include_deleted=True if filters["is_deleted"] is True else False,
        include_archived=True,
    )

    queryset = apply_filters(
        queryset,
        search=filters["search"] or None,
        lead_type=filters["lead_type"] or None,
        status=filters["status"] or None,
        priority=filters["priority"] or None,
        source=filters["source"] or None,
        is_archived=filters["is_archived"],
        is_deleted=filters["is_deleted"],
    )
    return queryset, filters


@staff_member_required
@require_http_methods(["GET"])
def lead_list(request):
    queryset, filters = _lead_queryset_for_board(request)

    grouped = group_leads_by_status(queryset)
    stats = get_lead_stats(queryset)

    leads = list(queryset)
    payload = [_serialize_lead(lead) for lead in leads]

    context = {
        "leads": leads,
        "lead_payload": payload,
        "leads_by_status": grouped,
        "lead_stats": stats,
        "filters": filters,
        "lead_types": Lead.LeadType.choices,
        "lead_statuses": Lead.LeadStatus.choices,
        "lead_priorities": Lead.LeadPriority.choices,
        "lead_sources": Lead.LeadSource.choices,
        "active_count": get_active_queryset().count(),
        "base_count": get_base_queryset().count(),
    }

    if _wants_json(request):
        return JsonResponse(
            {
                "ok": True,
                "stats": stats,
                "filters": filters,
                "leads": payload,
                "grouped": {
                    key: [_serialize_lead(item) for item in value]
                    for key, value in grouped.items()
                },
            }
        )

    return render(request, "lead/lead_list.html", context)


@staff_member_required
@require_http_methods(["GET", "POST"])
def lead_detail(request, pk):
    lead = get_lead_by_id(pk, include_deleted=True)
    if lead is None:
        lead = get_object_or_404(Lead, pk=pk)

    if request.method == "POST":
        data = _payload_from_request(request)

        status = data.get("status", lead.status)
        priority = data.get("priority", lead.priority)
        notes = data.get("notes", lead.notes)
        tags = data.get("tags", None)
        source = data.get("source", lead.source)
        lead_type = data.get("lead_type", lead.lead_type)

        update_kwargs = {
            "status": status,
            "priority": priority,
            "notes": notes,
            "source": source,
            "lead_type": lead_type,
        }

        if tags is not None:
            update_kwargs["tags"] = _normalize_tags(tags)

        update_lead(lead, **update_kwargs)

        if _wants_json(request):
            return JsonResponse(
                {
                    "ok": True,
                    "lead": _serialize_lead(lead),
                    "message": "Lead updated successfully.",
                }
            )

        messages.success(request, "Lead updated successfully.")
        return redirect("lead:lead_detail", pk=lead.pk)

    context = {
        "lead": lead,
        "lead_types": Lead.LeadType.choices,
        "lead_statuses": Lead.LeadStatus.choices,
        "lead_priorities": Lead.LeadPriority.choices,
        "lead_sources": Lead.LeadSource.choices,
        "lead_payload": _serialize_lead(lead),
    }

    if _wants_json(request):
        return JsonResponse({"ok": True, "lead": _serialize_lead(lead)})

    return render(request, "lead/lead_detail.html", context)


@staff_member_required
@require_http_methods(["POST"])
def lead_create(request):
    data = _payload_from_request(request)

    lead_type = _resolve_lead_type(data)
    source = _resolve_source(data, lead_type=lead_type)

    lead = create_lead(
        name=_get_value_str(data, "name", "principal_name", "full_name"),
        email=_get_value_str(data, "email", "principal_email", "email_address"),
        phone=_get_value_str(data, "phone", "principal_phone", "phone_number"),
        lead_type=lead_type,
        status=_get_value_str(data, "status", default=Lead.LeadStatus.NEW) or Lead.LeadStatus.NEW,
        priority=_get_value_str(data, "priority", default=Lead.LeadPriority.COLD) or Lead.LeadPriority.COLD,
        source=source,
        budget=_get_value_str(data, "budget"),
        project=_get_value_str(data, "project", "typology", "project_type", "lead_project"),
        location=_get_value_str(data, "location"),
        timeline=_get_value_str(data, "timeline"),
        avatar=_get_value_str(data, "avatar"),
        notes=_build_intake_notes(data),
        tags=_normalize_tags(_get_value(data, "tags", default=[])),
        is_archived=_boolish(data.get("is_archived", False)) or False,
        is_deleted=_boolish(data.get("is_deleted", False)) or False,
    )

    if _wants_json(request):
        return JsonResponse(
            {
                "ok": True,
                "lead": _serialize_lead(lead),
                "message": "Lead created successfully.",
            },
            status=201,
        )

    messages.success(request, "Lead created successfully.")
    return redirect("lead:lead_detail", pk=lead.pk)


@csrf_exempt
@require_http_methods(["POST"])
def lead_intake_api(request):
    """
    Public intake endpoint for all lead sources.

    RFQ, contact form, website form, ad campaigns, WhatsApp, and future sources
    should all be able to post here and end up in the unified Lead table.
    """
    data = _payload_from_request(request)

    lead_type = _resolve_lead_type(data)
    source = _resolve_source(data, lead_type=lead_type)

    name = _get_value_str(data, "name", "principal_name", "full_name")
    email = _get_value_str(data, "email", "principal_email", "email_address")
    phone = _get_value_str(data, "phone", "principal_phone", "phone_number")

    notes = _build_intake_notes(data)

    lead = create_lead(
        name=name,
        email=email,
        phone=phone,
        lead_type=lead_type,
        source=source,
        status=_get_value_str(data, "status", default=Lead.LeadStatus.NEW) or Lead.LeadStatus.NEW,
        priority=_get_value_str(data, "priority", default=Lead.LeadPriority.COLD) or Lead.LeadPriority.COLD,
        budget=_get_value_str(data, "budget"),
        project=_get_value_str(data, "project", "typology", "project_type", "lead_project"),
        location=_get_value_str(data, "location"),
        timeline=_get_value_str(data, "timeline"),
        avatar=_get_value_str(data, "avatar"),
        notes=notes,
        tags=_normalize_tags(_get_value(data, "tags", default=[])),
        is_archived=_boolish(data.get("is_archived", False)) or False,
        is_deleted=_boolish(data.get("is_deleted", False)) or False,
    )

    return JsonResponse(
        {
            "ok": True,
            "status": "success",
            "message": "Lead received successfully.",
            "lead": _serialize_lead(lead),
        },
        status=201,
    )


@csrf_exempt
@require_http_methods(["POST"])
def subscription_create(request):
    """
    Footer newsletter subscription endpoint.
    """
    data = _payload_from_request(request)

    email = _get_value_str(
        data,
        "email",
        "subscriber_email",
    ).lower()

    if not email:
        return JsonResponse(
            {
                "ok": False,
                "message": "Email is required.",
            },
            status=400,
        )

    existing = Lead.objects.filter(
        email__iexact=email,
        is_subscriber=True,
        is_deleted=False,
    ).first()

    if existing:
        return JsonResponse(
            {
                "ok": True,
                "message": "You are already subscribed.",
                "lead": _serialize_lead(existing),
            }
        )

    lead = create_lead(
        name="Newsletter Subscriber",
        email=email,
        phone="",
        lead_type=Lead.LeadType.SUBSCRIPTION,
        source=Lead.LeadSource.SUBSCRIPTION,
        status=Lead.LeadStatus.NEW,
        priority=Lead.LeadPriority.COLD,
        budget="",
        project="Newsletter Subscription",
        location="",
        timeline="",
        avatar="",
        notes="Subscribed from website footer subscription form.",
        tags=["subscription", "newsletter"],
        is_archived=False,
        is_deleted=False,
    )

    lead.is_subscriber = True
    lead.save(update_fields=["is_subscriber"])

    return JsonResponse(
        {
            "ok": True,
            "status": "success",
            "message": "Subscription successful.",
            "lead": _serialize_lead(lead),
        },
        status=201,
    )


@staff_member_required
@require_http_methods(["POST"])
def lead_update(request, pk):
    lead = get_lead_by_id(pk, include_deleted=True)
    if lead is None:
        lead = get_object_or_404(Lead, pk=pk)

    data = _payload_from_request(request)

    update_kwargs = {
        "name": data.get("name", lead.name),
        "email": data.get("email", lead.email),
        "phone": data.get("phone", lead.phone),
        "lead_type": data.get("lead_type", lead.lead_type),
        "status": data.get("status", lead.status),
        "priority": data.get("priority", lead.priority),
        "source": data.get("source", lead.source),
        "budget": data.get("budget", lead.budget),
        "project": data.get("project", lead.project),
        "location": data.get("location", lead.location),
        "timeline": data.get("timeline", lead.timeline),
        "avatar": data.get("avatar", lead.avatar),
        "notes": data.get("notes", lead.notes),
        "is_archived": _boolish(data.get("is_archived", lead.is_archived)),
        "is_deleted": _boolish(data.get("is_deleted", lead.is_deleted)),
    }

    if "tags" in data:
        update_kwargs["tags"] = _normalize_tags(data.get("tags"))

    update_lead(lead, **update_kwargs)

    if _wants_json(request):
        return JsonResponse(
            {
                "ok": True,
                "lead": _serialize_lead(lead),
                "message": "Lead updated successfully.",
            }
        )

    messages.success(request, "Lead updated successfully.")
    return redirect("lead:lead_detail", pk=lead.pk)


@staff_member_required
@require_http_methods(["POST"])
def lead_set_status(request, pk):
    lead = get_lead_by_id(pk, include_deleted=True)
    if lead is None:
        lead = get_object_or_404(Lead, pk=pk)

    data = _payload_from_request(request)
    status = data.get("status", Lead.LeadStatus.NEW)
    set_status(lead, status)

    if _wants_json(request):
        return JsonResponse({"ok": True, "lead": _serialize_lead(lead)})

    messages.success(request, "Lead status updated.")
    return redirect("lead:lead_detail", pk=lead.pk)


@staff_member_required
@require_http_methods(["POST"])
def lead_set_priority(request, pk):
    lead = get_lead_by_id(pk, include_deleted=True)
    if lead is None:
        lead = get_object_or_404(Lead, pk=pk)

    data = _payload_from_request(request)
    priority = data.get("priority", Lead.LeadPriority.COLD)
    set_priority(lead, priority)

    if _wants_json(request):
        return JsonResponse({"ok": True, "lead": _serialize_lead(lead)})

    messages.success(request, "Lead priority updated.")
    return redirect("lead:lead_detail", pk=lead.pk)


@staff_member_required
@require_http_methods(["POST"])
def lead_set_source(request, pk):
    lead = get_lead_by_id(pk, include_deleted=True)
    if lead is None:
        lead = get_object_or_404(Lead, pk=pk)

    data = _payload_from_request(request)
    source = data.get("source", Lead.LeadSource.WEBSITE)
    set_source(lead, source)

    if _wants_json(request):
        return JsonResponse({"ok": True, "lead": _serialize_lead(lead)})

    messages.success(request, "Lead source updated.")
    return redirect("lead:lead_detail", pk=lead.pk)


@staff_member_required
@require_http_methods(["POST"])
def lead_update_notes(request, pk):
    lead = get_lead_by_id(pk, include_deleted=True)
    if lead is None:
        lead = get_object_or_404(Lead, pk=pk)

    data = _payload_from_request(request)
    notes = data.get("notes", "")
    update_lead_notes(lead, notes)

    if _wants_json(request):
        return JsonResponse({"ok": True, "lead": _serialize_lead(lead)})

    messages.success(request, "Lead notes updated.")
    return redirect("lead:lead_detail", pk=lead.pk)


@staff_member_required
@require_http_methods(["POST"])
def lead_update_tags(request, pk):
    lead = get_lead_by_id(pk, include_deleted=True)
    if lead is None:
        lead = get_object_or_404(Lead, pk=pk)

    data = _payload_from_request(request)
    tags = data.get("tags", [])
    update_lead_tags(lead, tags)

    if _wants_json(request):
        return JsonResponse({"ok": True, "lead": _serialize_lead(lead)})

    messages.success(request, "Lead tags updated.")
    return redirect("lead:lead_detail", pk=lead.pk)


@staff_member_required
@require_http_methods(["POST"])
def lead_archive(request, pk):
    lead = get_lead_by_id(pk, include_deleted=True)
    if lead is None:
        lead = get_object_or_404(Lead, pk=pk)

    archive_lead(lead)

    if _wants_json(request):
        return JsonResponse({"ok": True, "lead": _serialize_lead(lead)})

    messages.success(request, "Lead archived.")
    return redirect("lead:lead_detail", pk=lead.pk)


@staff_member_required
@require_http_methods(["POST"])
def lead_unarchive(request, pk):
    lead = get_lead_by_id(pk, include_deleted=True)
    if lead is None:
        lead = get_object_or_404(Lead, pk=pk)

    unarchive_lead(lead)

    if _wants_json(request):
        return JsonResponse({"ok": True, "lead": _serialize_lead(lead)})

    messages.success(request, "Lead unarchived.")
    return redirect("lead:lead_detail", pk=lead.pk)


@staff_member_required
@require_http_methods(["POST"])
def lead_delete(request, pk):
    lead = get_lead_by_id(pk, include_deleted=True)
    if lead is None:
        lead = get_object_or_404(Lead, pk=pk)

    delete_lead(lead)

    if _wants_json(request):
        return JsonResponse({"ok": True, "lead": _serialize_lead(lead)})

    messages.success(request, "Lead marked as deleted.")
    return redirect("lead:lead_detail", pk=lead.pk)


@staff_member_required
@require_http_methods(["POST"])
def lead_restore(request, pk):
    lead = get_lead_by_id(pk, include_deleted=True)
    if lead is None:
        lead = get_object_or_404(Lead, pk=pk)

    restore_lead(lead)

    if _wants_json(request):
        return JsonResponse({"ok": True, "lead": _serialize_lead(lead)})

    messages.success(request, "Lead restored.")
    return redirect("lead:lead_detail", pk=lead.pk)


@staff_member_required
@require_http_methods(["GET"])
def lead_stats_api(request):
    queryset, _filters = _lead_queryset_for_board(request)
    stats = get_lead_stats(queryset)

    return JsonResponse({"ok": True, "stats": stats})


@staff_member_required
@require_http_methods(["GET"])
def lead_board_api(request):
    queryset, filters = _lead_queryset_for_board(request)
    grouped = group_leads_by_status(queryset)
    stats = get_lead_stats(queryset)

    return JsonResponse(
        {
            "ok": True,
            "filters": filters,
            "stats": stats,
            "grouped": {
                key: [_serialize_lead(item) for item in value]
                for key, value in grouped.items()
            },
        }
    )