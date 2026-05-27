from django.contrib import admin

from .models import (
    HeroTypographySettings,
    NavItem,
    SiteLogo,
    NavbarSettings,
    FooterSettings,
    FooterProjectLink,
    FooterPracticeLink,
    FooterSocialLink,
    WhatsAppSettings,
)


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj:
            return self.change_view(request, str(obj.id))
        return super().changelist_view(request, extra_context)


@admin.register(HeroTypographySettings)
class HeroTypographySettingsAdmin(admin.ModelAdmin):
    list_display = (
        "page_type",
        "title_font_family",
        "body_font_family",
        "button_font_family",
        "stats_font_family",
        "panel_font_family",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "page_type",
        "is_active",
    )

    search_fields = (
        "page_type",
        "title_font_family",
        "body_font_family",
        "button_font_family",
        "stats_font_family",
        "panel_font_family",
    )

    ordering = (
        "page_type",
    )

    list_editable = (
        "is_active",
    )

    fieldsets = (
        (
            "Hero Target",
            {
                "fields": (
                    "page_type",
                    "is_active",
                )
            },
        ),
        (
            "Title Typography",
            {
                "fields": (
                    "title_font_family",
                    "title_font_type",
                    "title_font_weight",
                    "title_font_size_desktop",
                    "title_font_size_tablet",
                    "title_font_size_mobile",
                    "title_line_height",
                    "title_letter_spacing",
                    "title_text_transform",
                    "title_color",
                )
            },
        ),
        (
            "Body Typography",
            {
                "fields": (
                    "body_font_family",
                    "body_font_type",
                    "body_font_weight",
                    "body_font_size_desktop",
                    "body_font_size_tablet",
                    "body_font_size_mobile",
                    "body_line_height",
                    "body_letter_spacing",
                    "body_text_transform",
                    "body_color",
                )
            },
        ),
        (
            "Button Typography",
            {
                "fields": (
                    "button_font_family",
                    "button_font_type",
                    "button_font_weight",
                    "button_font_size",
                    "button_letter_spacing",
                    "button_text_transform",
                    "button_color",
                )
            },
        ),
        (
            "Stats Typography",
            {
                "fields": (
                    "stats_font_family",
                    "stats_font_type",
                    "stats_font_weight",
                    "stats_font_size",
                    "stats_line_height",
                    "stats_letter_spacing",
                    "stats_text_transform",
                    "stats_color",
                )
            },
        ),
        (
            "Panel Typography",
            {
                "fields": (
                    "panel_font_family",
                    "panel_font_type",
                    "panel_font_weight",
                    "panel_font_size",
                    "panel_line_height",
                    "panel_letter_spacing",
                    "panel_text_transform",
                    "panel_color",
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

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "url",
        "order",
        "type",
        "is_active",
    )

    list_filter = (
        "is_active",
        "type",
    )

    search_fields = (
        "title",
        "url",
    )

    ordering = (
        "order",
        "id",
    )

    list_editable = (
        "order",
        "is_active",
        "type",
    )


@admin.register(SiteLogo)
class SiteLogoAdmin(SingletonAdmin):
    list_display = (
        "__str__",
        "updated_at",
    )


@admin.register(NavbarSettings)
class NavbarSettingsAdmin(SingletonAdmin):
    list_display = (
        "__str__",
        "nav_bg_color",
        "nav_text_color",
        "nav_logo_height",
    )

    fieldsets = (
        (
            "Navbar Colors",
            {
                "fields": (
                    "nav_bg_color",
                    "nav_text_color",
                    "nav_text_dark",
                    "nav_hover_color",
                    "nav_border_color",
                )
            },
        ),
        (
            "Navbar Layout",
            {
                "fields": (
                    "nav_padding_y",
                    "nav_padding_x",
                    "nav_logo_height",
                )
            },
        ),
    )


class FooterProjectLinkInline(admin.TabularInline):
    model = FooterProjectLink
    extra = 0
    fields = (
        "title",
        "url",
        "order",
        "is_active",
    )
    ordering = (
        "order",
        "id",
    )


class FooterPracticeLinkInline(admin.TabularInline):
    model = FooterPracticeLink
    extra = 0
    fields = (
        "title",
        "url",
        "order",
        "is_active",
    )
    ordering = (
        "order",
        "id",
    )


class FooterSocialLinkInline(admin.TabularInline):
    model = FooterSocialLink
    extra = 0
    fields = (
        "name",
        "url",
        "icon_name",
        "icon_svg",
        "order",
        "is_active",
    )
    ordering = (
        "order",
        "id",
    )


@admin.register(FooterSettings)
class FooterSettingsAdmin(SingletonAdmin):
    list_display = (
        "__str__",
        "background_color",
        "text_color",
        "accent_color",
    )

    inlines = [
        FooterProjectLinkInline,
        FooterPracticeLinkInline,
        FooterSocialLinkInline,
    ]

    fieldsets = (
        (
            "Footer Branding",
            {
                "fields": (
                    "company_name",
                    "company_description",
                    "logo_image",
                    "logo_alt",
                    "logo_url",
                )
            },
        ),
        (
            "Footer Colors",
            {
                "fields": (
                    "background_color",
                    "border_color",
                    "text_color",
                    "muted_color",
                    "accent_color",
                )
            },
        ),
        (
            "Footer Headings",
            {
                "fields": (
                    "projects_heading",
                    "practice_heading",
                    "subscription_heading",
                )
            },
        ),
        (
            "Newsletter Settings",
            {
                "fields": (
                    "newsletter_text",
                    "newsletter_placeholder",
                    "newsletter_button_text",
                    "newsletter_action_url",
                )
            },
        ),
        (
            "Footer Bottom",
            {
                "fields": (
                    "copyright_text",
                    "bottom_alignment",
                    "social_alignment",
                )
            },
        ),
    )


@admin.register(WhatsAppSettings)
class WhatsAppSettingsAdmin(SingletonAdmin):
    list_display = (
        "__str__",
        "phone_number",
        "is_active",
        "updated_at",
    )

    fieldsets = (
        (
            "WhatsApp Configuration",
            {
                "fields": (
                    "phone_number",
                    "prefilled_text",
                    "is_active",
                )
            },
        ),
        (
            "System",
            {
                "fields": (
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "updated_at",
    )