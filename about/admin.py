from django.contrib import admin
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.html import format_html

from .models import (
    AboutPageSettings,
    AboutHeroSection,
    AboutOverviewSection,
    VisionMissionValues,
    KeyStatsSection,
    KeyStatItem,
    AssociatedWithSection,
    AssociatedPartner,
    OurTeamSection,
    TeamMember,
)

# =========================================
# SINGLETON ADMIN BASE
# =========================================
class SingletonAdmin(admin.ModelAdmin):
    """
    Safe singleton admin base.
    Prevents delete, keeps Django default permissions intact.
    """

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return not self.model.objects.exists()


# =========================================
# ABOUT PAGE SETTINGS ADMIN
# =========================================
@admin.register(AboutPageSettings)
class AboutPageSettingsAdmin(SingletonAdmin):

    list_display = (
        "safe_title",
        "is_active",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "page_title",
        "meta_description",
    )

    list_filter = (
        "is_active",
    )

    fieldsets = (
        ("Page Settings", {
            "fields": (
                "is_active",
                "page_title",
                "meta_description",
            ),
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            ),
        }),
    )

    def safe_title(self, obj):
        title = getattr(obj, "page_title", None)
        return title or "—"

    safe_title.short_description = "Page Title"


# =========================================
# ABOUT HERO SECTION ADMIN
# =========================================
@admin.register(AboutHeroSection)
class AboutHeroSectionAdmin(SingletonAdmin):

    list_display = (
        "hero_preview_safe",
        "safe_eyebrow",
        "short_title_safe",
        "is_active",
        "updated_at",
    )

    readonly_fields = (
        "background_preview_safe",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "eyebrow",
        "title",
        "description",
        "primary_button_text",
        "secondary_button_text",
    )

    list_filter = (
        "is_active",
    )

    fieldsets = (
        ("Hero Visibility", {
            "fields": ("is_active",),
        }),
        ("Hero Content", {
            "fields": (
                "eyebrow",
                "title",
                "description",
            ),
        }),
        ("Hero Background Image", {
            "fields": (
                "background_image",
                "background_preview_safe",
            ),
        }),
        ("Primary Button", {
            "fields": (
                "primary_button_text",
                "primary_button_url",
            ),
        }),
        ("Secondary Button", {
            "fields": (
                "secondary_button_text",
                "secondary_button_url",
            ),
        }),
        ("System Information", {
            "fields": (
                "created_at",
                "updated_at",
            ),
        }),
    )

    def safe_eyebrow(self, obj):
        return getattr(obj, "eyebrow", "") or "—"

    safe_eyebrow.short_description = "Eyebrow"

    def short_title_safe(self, obj):
        title = getattr(obj, "title", "") or ""
        title = str(title).replace("\n", " ").strip()
        if not title:
            return "—"
        return title[:60] + "..." if len(title) > 60 else title

    short_title_safe.short_description = "Hero Title"

    def hero_preview_safe(self, obj):
        img = getattr(obj, "background_image", None)

        try:
            if img and hasattr(img, "url"):
                return format_html(
                    """
                    <img src="{}"
                         style="
                            width:80px;
                            height:60px;
                            object-fit:cover;
                            border-radius:10px;
                            border:1px solid rgba(0,0,0,0.08);
                         ">
                    """,
                    img.url,
                )
        except Exception:
            pass

        return "—"

    hero_preview_safe.short_description = "Preview"

    def background_preview_safe(self, obj):
        img = getattr(obj, "background_image", None)

        try:
            if img and hasattr(img, "url"):
                return format_html(
                    """
                    <div style="margin-top:10px;">
                        <img src="{}"
                             style="
                                width:100%;
                                max-width:900px;
                                height:420px;
                                object-fit:cover;
                                border-radius:16px;
                                border:1px solid rgba(0,0,0,0.08);
                                box-shadow:0 10px 30px rgba(0,0,0,0.08);
                             ">
                    </div>
                    """,
                    img.url,
                )
        except Exception:
            pass

        return format_html(
            """
            <div style="
                padding:24px;
                border-radius:12px;
                background:#f5f5f5;
                color:#666;
                text-align:center;
                font-size:14px;
            ">
                No image uploaded
            </div>
            """
        )

    background_preview_safe.short_description = "Image Preview"


# =========================================
# ABOUT OVERVIEW SECTION ADMIN
# =========================================
@admin.register(AboutOverviewSection)
class AboutOverviewSectionAdmin(SingletonAdmin):
    """
    Premium CMS admin for About Overview section.
    """

    fieldsets = (
        ("Section Control", {
            "fields": (
                "is_active",
            )
        }),
        ("Overview Content", {
            "fields": (
                "subtitle",
                "title",
                "description",
            )
        }),
        ("Overview Button", {
            "fields": (
                "button_text",
                "button_link",
            )
        }),
        ("Primary Image", {
            "fields": (
                "main_image",
                "main_image_alt",
                "main_image_preview",
            )
        }),
        ("Secondary Image", {
            "fields": (
                "secondary_image",
                "secondary_image_alt",
                "secondary_image_preview",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    readonly_fields = (
        "main_image_preview",
        "secondary_image_preview",
        "created_at",
        "updated_at",
    )

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '''
                <img
                    src="{}"
                    style="
                        width: 320px;
                        height: auto;
                        border-radius: 8px;
                        object-fit: cover;
                    "
                />
                ''',
                obj.main_image.url
            )
        return "No main image uploaded"

    main_image_preview.short_description = "Main Image Preview"

    def secondary_image_preview(self, obj):
        if obj.secondary_image:
            return format_html(
                '''
                <img
                    src="{}"
                    style="
                        width: 260px;
                        height: auto;
                        border-radius: 8px;
                        object-fit: cover;
                    "
                />
                ''',
                obj.secondary_image.url
            )
        return "No secondary image uploaded"

    secondary_image_preview.short_description = "Secondary Image Preview"


# =========================================
# VISION / MISSION / VALUES ADMIN
# =========================================
@admin.register(VisionMissionValues)
class VisionMissionValuesAdmin(admin.ModelAdmin):

    list_display = (
        "section_title",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    fieldsets = (
        ("SECTION SETTINGS", {
            "fields": (
                "section_title",
                "is_active",
            )
        }),
        ("VISION BLOCK", {
            "fields": (
                "vision_title",
                "vision_text",
                "vision_icon",
            )
        }),
        ("MISSION BLOCK", {
            "fields": (
                "mission_title",
                "mission_text",
                "mission_icon",
            )
        }),
        ("VALUES BLOCK", {
            "fields": (
                "values_title",
                "values_text",
                "values_icon",
            )
        }),
    )


# =========================================================
# INLINE ADMIN: KEY STAT ITEMS
# =========================================================
class KeyStatItemInline(admin.TabularInline):
    """
    Inline editor for individual stat cards inside KeyStatsSection.
    """
    model = KeyStatItem
    extra = 1
    fields = ("label", "value", "suffix", "order")
    ordering = ("order",)


# =========================================================
# KEY STATS SECTION ADMIN (PARENT)
# =========================================================
@admin.register(KeyStatsSection)
class KeyStatsSectionAdmin(SingletonAdmin):
    """
    Singleton-style CMS admin for Key Stats section.
    """

    list_display = ("safe_title", "is_active")
    list_editable = ("is_active",)

    fieldsets = (
        ("Section Control", {
            "fields": ("is_active", "tag")
        }),
        ("Content", {
            "fields": ("title", "subtitle")
        }),
    )

    inlines = [KeyStatItemInline]

    def safe_title(self, obj):
        return getattr(obj, "title", "") or "—"

    safe_title.short_description = "Title"

    def changelist_view(self, request, extra_context=None):
        obj = KeyStatsSection.objects.first()
        if obj:
            return redirect(reverse("admin:about_keystatssection_change", args=[obj.pk]))
        return super().changelist_view(request, extra_context)
    
# =========================================================
# ASSOCIATED PARTNER INLINE
# =========================================================
class AssociatedPartnerInline(admin.TabularInline):
    model = AssociatedPartner
    extra = 0  # prevents forced empty required form rows

    ordering = (
        "display_order",
        "id",
    )

    fields = (
        "logo_preview",
        "name",
        "logo",
        "website_url",
        "display_order",
        "is_active",
    )

    readonly_fields = (
        "logo_preview",
    )

    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html(
                '<img src="{}" style="height:60px;width:auto;border-radius:6px;background:#fff;padding:6px;border:1px solid #e5e7eb;" />',
                obj.logo.url
            )
        return "No Logo"

    logo_preview.short_description = "Preview"


# =========================================================
# ASSOCIATED WITH SECTION ADMIN
# =========================================================
@admin.register(AssociatedWithSection)
class AssociatedWithSectionAdmin(SingletonAdmin):

    list_display = (
        "heading",
        "is_active",
    )

    inlines = [AssociatedPartnerInline]

    fieldsets = (
        (
            "Section Visibility",
            {
                "fields": ("is_active",)
            }
        ),

        (
            "Section Content",
            {
                "fields": (
                    "kicker",
                    "heading",
                    "description",
                )
            }
        ),

        (
            "Layout Settings",
            {
                "fields": (
                    "section_padding_top",
                    "section_padding_bottom",
                    "marquee_speed",
                )
            }
        ),
    )


# =========================================================
# ASSOCIATED PARTNER ADMIN
# =========================================================
@admin.register(AssociatedPartner)
class AssociatedPartnerAdmin(admin.ModelAdmin):

    list_display = (
        "logo_preview",
        "name",
        "display_order",
        "is_active",
    )

    ordering = (
        "display_order",
        "id",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "is_active",
    )

    fields = (
        "section",
        "name",
        "logo_preview",
        "logo",
        "website_url",
        "display_order",
        "is_active",
    )

    readonly_fields = (
        "logo_preview",
    )

    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html(
                '<img src="{}" style="height:70px;width:auto;border-radius:6px;background:#fff;padding:6px;border:1px solid #e5e7eb;" />',
                obj.logo.url
            )
        return "No Logo"

    logo_preview.short_description = "Logo"

# =========================================================
# TEAM MEMBER INLINE (DRAG + INLINE CMS EDITING)
# =========================================================
class TeamMemberInline(admin.TabularInline):
    """
    Inline CMS editor for team members.
    Allows drag-like ordering via display_order.
    """

    model = TeamMember
    extra = 1
    ordering = ("display_order",)

    fields = (
        "display_order",
        "name",
        "role",
        "description",
        "image",
        "is_active",
        "preview_image",
    )

    readonly_fields = ("preview_image",)

    def preview_image(self, obj):
        """
        Admin thumbnail preview (safe optional field)
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px;width:50px;object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return "-"

    preview_image.short_description = "Preview"


# =========================================================
# OUR TEAM SECTION ADMIN
# =========================================================
@admin.register(OurTeamSection)
class OurTeamSectionAdmin(admin.ModelAdmin):
    """
    CMS control for entire Our Team section
    """

    inlines = [TeamMemberInline]

    list_display = (
        "section_title",
        "eyebrow",
        "is_active",
        "member_count",
    )

    list_editable = ("is_active",)

    fieldsets = (
        ("Section Content", {
            "fields": (
                "section_title",
                "eyebrow",
                "is_active",
            )
        }),
    )

    def member_count(self, obj):
        """
        Shows number of active team members
        """
        return obj.members.count()

    member_count.short_description = "Members"


# =========================================================
# OPTIONAL: TEAM MEMBER DIRECT ADMIN VIEW
# (useful for bulk editing / search / filtering)
# =========================================================
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """
    Standalone admin for advanced CMS control
    """

    list_display = (
        "name",
        "role",
        "section",
        "display_order",
        "is_active",
    )

    list_filter = (
        "section",
        "is_active",
    )

    search_fields = (
        "name",
        "role",
        "description",
    )

    list_editable = (
        "display_order",
        "is_active",
    )

    ordering = ("section", "display_order")

    fieldsets = (
        ("Basic Info", {
            "fields": (
                "section",
                "name",
                "role",
                "description",
            )
        }),
        ("Media", {
            "fields": (
                "image",
            )
        }),
        ("Control", {
            "fields": (
                "display_order",
                "is_active",
            )
        }),
    )