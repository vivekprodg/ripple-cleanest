from django.contrib import admin
from django.utils.html import format_html

from .models import (
    InteriorHeroSection,
    InteriorPhilosophySection,
    InteriorPhilosophyImage,
    InteriorPhilosophyPoint,
    InteriorService,
    InteriorSelectedWork,
    InteriorGalleryCategory,
    InteriorGalleryItem,
)


@admin.register(InteriorHeroSection)
class InteriorHeroSectionAdmin(admin.ModelAdmin):
    """
    Admin for CMS-driven Interior Hero Section
    All fields are optional, so admin is kept minimal and flexible
    """

    list_display = (
        "id",
        "eyebrow",
        "title",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "eyebrow",
        "title",
        "subtitle",
    )

    ordering = ("-updated_at",)

    fieldsets = (
        ("Hero Media", {
            "fields": ("background_image",),
            "description": "Optional background image for hero section",
        }),
        ("Hero Content", {
            "fields": ("eyebrow", "title", "subtitle"),
            "description": "All content fields are optional (CMS-driven)",
        }),
        ("Status", {
            "fields": ("is_active",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class InteriorPhilosophyImageInline(admin.TabularInline):
    model = InteriorPhilosophyImage
    extra = 1
    fields = (
        "image",
        "alt_text",
        "display_order",
        "is_active",
    )
    ordering = (
        "display_order",
        "id",
    )


class InteriorPhilosophyPointInline(admin.TabularInline):
    model = InteriorPhilosophyPoint
    extra = 1
    fields = (
        "number",
        "title",
        "description",
        "display_order",
        "is_active",
    )
    ordering = (
        "display_order",
        "id",
    )


@admin.register(InteriorPhilosophySection)
class InteriorPhilosophySectionAdmin(admin.ModelAdmin):
    list_display = (
        "heading",
        "eyebrow",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "heading",
        "eyebrow",
        "paragraph_one",
        "paragraph_two",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Section Content",
            {
                "fields": (
                    "eyebrow",
                    "heading",
                    "paragraph_one",
                    "paragraph_two",
                )
            },
        ),
        (
            "Settings",
            {
                "fields": ("is_active",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    inlines = [
        InteriorPhilosophyImageInline,
        InteriorPhilosophyPointInline,
    ]


@admin.register(InteriorPhilosophyImage)
class InteriorPhilosophyImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "section",
        "display_order",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "alt_text",
    )

    ordering = (
        "display_order",
        "id",
    )


@admin.register(InteriorPhilosophyPoint)
class InteriorPhilosophyPointAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "number",
        "section",
        "display_order",
        "is_active",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
    )

    ordering = (
        "display_order",
        "id",
    )


@admin.register(InteriorService)
class InteriorServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "is_active", "order", "created_at")
    list_editable = ("is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    ordering = ("order",)

    fieldsets = (
        (None, {
            "fields": (
                "icon",
                "title",
                "description",
                "is_active",
                "order",
            )
        }),
    )


@admin.register(InteriorSelectedWork)
class InteriorSelectedWorkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "main_title",
        "side_title_1",
        "side_title_2",
        "created_at",
    )

    search_fields = (
        "title",
        "category",
        "main_title",
        "side_title_1",
        "side_title_2",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": (
                "title",
                "category",
                "description",
            )
        }),
        ("Main Card", {
            "fields": (
                "main_image",
                "main_title",
                "main_subtitle",
                "main_desc",
            )
        }),
        ("Side Card 1", {
            "fields": (
                "side_image_1",
                "side_title_1",
                "side_subtitle_1",
                "side_desc_1",
            )
        }),
        ("Side Card 2", {
            "fields": (
                "side_image_2",
                "side_title_2",
                "side_subtitle_2",
                "side_desc_2",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )


@admin.register(InteriorGalleryCategory)
class InteriorGalleryCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "order",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "slug",
    )

    ordering = ("order", "name")
    prepopulated_fields = {
        "slug": ("name",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Category Info", {
            "fields": (
                "name",
                "slug",
                "order",
                "is_active",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )


@admin.register(InteriorGalleryItem)
class InteriorGalleryItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "gallery_category",
        "year",
        "order",
        "is_active",
        "created_at",
        "image_preview",
    )

    list_filter = (
        "gallery_category",
        "is_active",
        "year",
    )

    search_fields = (
        "title",
        "description",
        "location",
        "client",
        "slug",
        "gallery_category__name",
    )

    ordering = ("order", "-created_at")

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = ("created_at", "updated_at", "image_preview")

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "slug", "is_active")
        }),
        ("Media", {
            "fields": ("image", "image_preview")
        }),
        ("Content", {
            "fields": ("description",)
        }),
        ("Project Details", {
            "fields": ("gallery_category", "location", "year", "client", "order")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="height:60px;width:auto;border-radius:6px;" />',
                obj.image.url,
            )
        return "No Image"

    image_preview.short_description = "Preview"