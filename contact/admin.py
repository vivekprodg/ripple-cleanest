from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ContactInfoBox,
    ContactInquiry,
    ContactPageSettings,
    ContactSocialLink,
    ContactTopCard,
)


class ContactTopCardInline(admin.TabularInline):
    model = ContactTopCard
    extra = 0
    fields = (
        "sort_order",
        "is_active",
        "icon_text",
        "title",
        "value",
        "link_url",
    )
    ordering = ("sort_order", "id")
    classes = ("collapse",)
    show_change_link = True


class ContactInfoBoxInline(admin.TabularInline):
    model = ContactInfoBox
    extra = 0
    fields = (
        "sort_order",
        "is_active",
        "icon_text",
        "title",
        "value",
    )
    ordering = ("sort_order", "id")
    classes = ("collapse",)
    show_change_link = True


class ContactSocialLinkInline(admin.TabularInline):
    model = ContactSocialLink
    extra = 0
    fields = (
        "sort_order",
        "is_active",
        "label",
        "icon_text",
        "url",
    )
    ordering = ("sort_order", "id")
    classes = ("collapse",)
    show_change_link = True


@admin.register(ContactPageSettings)
class ContactPageSettingsAdmin(admin.ModelAdmin):
    inlines = [
        ContactTopCardInline,
        ContactInfoBoxInline,
        ContactSocialLinkInline,
    ]

    list_display = (
        "page_title",
        "is_active",
        "updated_at",
    )
    list_filter = ("is_active",)
    search_fields = (
        "page_title",
        "seo_title",
        "seo_description",
        "hero_title",
        "hero_description",
        "contact_email",
        "contact_phone",
        "contact_location",
        "contact_address",
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "is_active",
                    "page_title",
                    "seo_title",
                    "seo_description",
                )
            },
        ),
        (
            "Hero Section",
            {
                "fields": (
                    "hero_badge",
                    "hero_title",
                    "hero_description",
                    "hero_background_image",
                    "hero_overlay_strength",
                )
            },
        ),
        (
            "Left Panel",
            {
                "fields": (
                    "left_section_badge",
                    "left_section_title",
                    "left_section_description",
                    "left_section_background_image",
                )
            },
        ),
        (
            "Form Section",
            {
                "fields": (
                    "form_title",
                    "form_subtitle",
                    "submit_button_text",
                    "success_message",
                )
            },
        ),
        (
            "Map Section",
            {
                "fields": (
                    "map_title",
                    "map_description",
                    "map_embed_url",
                    "map_location_text",
                )
            },
        ),
        (
            "Direct Contact",
            {
                "fields": (
                    "contact_email",
                    "contact_phone",
                    "contact_location",
                    "contact_address",
                )
            },
        ),
        (
            "Social",
            {
                "fields": (
                    "social_heading",
                    "instagram_url",
                    "facebook_url",
                    "linkedin_url",
                )
            },
        ),
        (
            "System",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        # Singleton-style admin: only one settings record should exist.
        if ContactPageSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def changelist_view(self, request, extra_context=None):
        obj = ContactPageSettings.get_solo()
        return self.change_view(request, str(obj.pk), extra_context=extra_context)

    def response_add(self, request, obj, post_url_continue=None):
        return super().response_add(request, obj, post_url_continue)

    def save_model(self, request, obj, form, change):
        obj.pk = 1
        super().save_model(request, obj, form, change)


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email_address",
        "phone_number",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "full_name",
        "email_address",
        "phone_number",
        "project_details",
        "source_page",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "ip_address",
        "user_agent",
    )
    ordering = ("-created_at", "-id")
    fieldsets = (
        (
            "Inquiry Details",
            {
                "fields": (
                    "full_name",
                    "email_address",
                    "phone_number",
                    "project_details",
                )
            },
        ),
        (
            "Admin Handling",
            {
                "fields": (
                    "status",
                    "admin_notes",
                )
            },
        ),
        (
            "Tracking",
            {
                "fields": (
                    "source_page",
                    "ip_address",
                    "user_agent",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(ContactTopCard)
class ContactTopCardAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "value",
        "sort_order",
        "is_active",
        "settings",
    )
    list_filter = ("is_active",)
    search_fields = (
        "title",
        "value",
        "icon_text",
        "link_url",
    )
    ordering = ("sort_order", "id")


@admin.register(ContactInfoBox)
class ContactInfoBoxAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "value",
        "sort_order",
        "is_active",
        "settings",
    )
    list_filter = ("is_active",)
    search_fields = (
        "title",
        "value",
        "icon_text",
    )
    ordering = ("sort_order", "id")


@admin.register(ContactSocialLink)
class ContactSocialLinkAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "url",
        "sort_order",
        "is_active",
        "settings",
    )
    list_filter = ("is_active",)
    search_fields = (
        "label",
        "url",
        "icon_text",
    )
    ordering = ("sort_order", "id")