from django.contrib import admin
from django.utils import timezone

from .models import Lead

try:
    from .services import send_lead_assignment_notification
except ImportError:
    send_lead_assignment_notification = None


class IntakePathFilter(admin.SimpleListFilter):
    title = "Intake path"
    parameter_name = "intake_path"

    def lookups(self, request, model_admin):
        return (
            ("rfq_website", "RFQ / Website"),
            ("contact", "Contact"),
            ("ad", "Ad Campaign"),
            ("whatsapp", "WhatsApp"),
            ("subscription", "Subscription"),
            ("rfq_only", "RFQ only"),
            ("website_only", "Website only"),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == "rfq_website":
            return queryset.filter(
                source__in=[Lead.LeadSource.WEBSITE, Lead.LeadSource.RFQ_FORM]
            )

        if value == "rfq_only":
            return queryset.filter(source=Lead.LeadSource.RFQ_FORM)

        if value == "website_only":
            return queryset.filter(source=Lead.LeadSource.WEBSITE)

        if value == "contact":
            return queryset.filter(source=Lead.LeadSource.CONTACT_FORM)

        if value == "ad":
            return queryset.filter(source=Lead.LeadSource.FACEBOOK)

        if value == "whatsapp":
            return queryset.filter(source=Lead.LeadSource.WHATSAPP)

        if value == "subscription":
            return queryset.filter(is_subscriber=True)

        return queryset


class SubscriptionFilter(admin.SimpleListFilter):
    title = "Subscription"
    parameter_name = "subscription"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Subscribed"),
            ("no", "Not subscribed"),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == "yes":
            return queryset.filter(is_subscriber=True)

        if value == "no":
            return queryset.filter(is_subscriber=False)

        return queryset


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "display_name_admin",
        "display_email_admin",
        "lead_type",
        "status",
        "priority",
        "source",
        "assigned_to",
        "supervisor",
        "assigned_at",
        "is_subscriber",
        "project",
        "location",
        "created_at",
        "is_archived",
        "is_deleted",
    )

    list_display_links = ("display_name_admin",)

    list_editable = (
        "lead_type",
        "status",
        "priority",
        "source",
        "assigned_to",
        "supervisor",
        "is_subscriber",
        "is_archived",
        "is_deleted",
    )

    list_filter = (
        IntakePathFilter,
        SubscriptionFilter,
        "lead_type",
        "status",
        "priority",
        "source",
        "assigned_to",
        "supervisor",
        "is_subscriber",
        "is_archived",
        "is_deleted",
        "created_at",
        "updated_at",
        "assigned_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
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
        "notes",
        "tags",
        "assigned_to__username",
        "assigned_to__first_name",
        "assigned_to__last_name",
        "assigned_to__email",
        "supervisor__username",
        "supervisor__first_name",
        "supervisor__last_name",
        "supervisor__email",
    )

    ordering = ("-created_at", "-id")
    date_hierarchy = "created_at"
    save_as = True
    save_on_top = True
    empty_value_display = "—"
    list_per_page = 50

    fieldsets = (
        (
            "Contact",
            {
                "fields": (
                    "name",
                    "email",
                    "phone",
                    "avatar",
                )
            },
        ),
        (
            "Assignment",
            {
                "fields": (
                    "assigned_to",
                    "supervisor",
                    "assigned_at",
                )
            },
        ),
        (
            "Lead Classification",
            {
                "fields": (
                    "lead_type",
                    "status",
                    "priority",
                    "source",
                    "is_subscriber",
                )
            },
        ),
        (
            "Project Details",
            {
                "fields": (
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
                )
            },
        ),
        (
            "Internal Tracking",
            {
                "fields": (
                    "tags",
                    "notes",
                )
            },
        ),
        (
            "System",
            {
                "fields": (
                    "is_archived",
                    "is_deleted",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at", "assigned_at")

    actions = (
        "mark_new",
        "mark_contacted",
        "mark_won",
        "mark_lost",
        "mark_archived",
        "mark_unarchived",
        "mark_deleted",
        "mark_restored",
        "mark_subscribed",
        "mark_unsubscribed",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("assigned_to", "supervisor")

    @admin.display(description="Lead Name", ordering="name")
    def display_name_admin(self, obj):
        return obj.display_name

    @admin.display(description="Email", ordering="email")
    def display_email_admin(self, obj):
        return obj.display_email

    def save_model(self, request, obj, form, change):
        old_assigned_to_id = None
        old_supervisor_id = None

        if change and obj.pk:
            old = Lead.objects.filter(pk=obj.pk).only(
                "assigned_to_id",
                "supervisor_id",
                "assigned_at",
            ).first()
            if old:
                old_assigned_to_id = old.assigned_to_id
                old_supervisor_id = old.supervisor_id

        assignment_changed = (
            old_assigned_to_id != obj.assigned_to_id
            or old_supervisor_id != obj.supervisor_id
        )

        if assignment_changed and obj.assigned_to and not obj.assigned_at:
            obj.assigned_at = timezone.now()

        super().save_model(request, obj, form, change)

        if assignment_changed and obj.assigned_to and send_lead_assignment_notification:
            send_lead_assignment_notification(obj)

    @admin.action(description="Mark selected leads as New")
    def mark_new(self, request, queryset):
        queryset.update(status=Lead.LeadStatus.NEW)

    @admin.action(description="Mark selected leads as Contacted")
    def mark_contacted(self, request, queryset):
        queryset.update(status=Lead.LeadStatus.CONTACTED)

    @admin.action(description="Mark selected leads as Won")
    def mark_won(self, request, queryset):
        queryset.update(status=Lead.LeadStatus.WON)

    @admin.action(description="Mark selected leads as Lost")
    def mark_lost(self, request, queryset):
        queryset.update(status=Lead.LeadStatus.LOST)

    @admin.action(description="Archive selected leads")
    def mark_archived(self, request, queryset):
        queryset.update(is_archived=True)

    @admin.action(description="Unarchive selected leads")
    def mark_unarchived(self, request, queryset):
        queryset.update(is_archived=False)

    @admin.action(description="Mark selected leads as Deleted")
    def mark_deleted(self, request, queryset):
        queryset.update(is_deleted=True)

    @admin.action(description="Restore selected leads")
    def mark_restored(self, request, queryset):
        queryset.update(is_deleted=False)

    @admin.action(description="Mark selected leads as Subscribed")
    def mark_subscribed(self, request, queryset):
        queryset.update(is_subscriber=True)

    @admin.action(description="Mark selected leads as Not Subscribed")
    def mark_unsubscribed(self, request, queryset):
        queryset.update(is_subscriber=False)