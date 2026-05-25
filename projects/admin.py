from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ProjectHeroSection,
    ProjectStatus,
    ProjectCategory,
    ProjectSubCategory,
    Project,
    ProjectGallery,
)

# =========================================================
# PROJECT HERO SECTION ADMIN
# =========================================================
@admin.register(ProjectHeroSection)
class ProjectHeroSectionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "is_active",
        "updated_at",
    )

    search_fields = (
        "title",
        "description",
    )

    readonly_fields = (
        "background_image_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        (
            "Hero Content",
            {
                "fields": (
                    "title",
                    "description",
                ),
            },
        ),

        (
            "Hero Background",
            {
                "fields": (
                    "background_image",
                    "background_image_preview",
                ),
            },
        ),

        (
            "Visual Settings",
            {
                "fields": (
                    "overlay_opacity",
                    "is_active",
                ),
            },
        ),

        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),

    )

    def background_image_preview(self, obj):

        if obj.background_image:

            return format_html(
                """
                <img
                    src="{}"
                    style="
                        width:320px;
                        max-width:100%;
                        border-radius:12px;
                        border:1px solid #ddd;
                        object-fit:cover;
                    "
                >
                """,
                obj.background_image.url
            )

        return "No image uploaded."

    background_image_preview.short_description = "Background Preview"

    def has_add_permission(self, request):

        if ProjectHeroSection.objects.exists():
            return False

        return True

# =========================================================
# PROJECT STATUS ADMIN
# =========================================================
@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "created_at",
    )

    search_fields = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    ordering = (
        "name",
    )

# =========================================================
# PROJECT CATEGORY ADMIN
# =========================================================
@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "created_at",
    )

    search_fields = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    ordering = (
        "name",
    )

# =========================================================
# PROJECT SUBCATEGORY ADMIN
# =========================================================
@admin.register(ProjectSubCategory)
class ProjectSubCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "slug",
        "created_at",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    ordering = (
        "name",
    )

# =========================================================
# PROJECT GALLERY INLINE
# =========================================================
class ProjectGalleryInline(admin.TabularInline):

    model = ProjectGallery

    extra = 1

    fields = (
        "title",
        "image",
        "image_preview",
        "display_order",
    )

    readonly_fields = (
        "image_preview",
    )

    def image_preview(self, obj):

        if obj.image:

            return format_html(
                """
                <img
                    src="{}"
                    style="
                        width:120px;
                        height:80px;
                        object-fit:cover;
                        border-radius:8px;
                        border:1px solid #ddd;
                    "
                >
                """,
                obj.image.url
            )

        return "-"

    image_preview.short_description = "Preview"

# =========================================================
# PROJECT ADMIN
# =========================================================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    # ================= LIST VIEW =================
    list_display = (
        "title",
        "client",
        "status",
        "category",
        "subcategory",
        "is_active",
        "created_at",
    )

    list_filter = (
        "status",
        "category",
        "subcategory",
        "is_active",
    )

    search_fields = (
        "title",
        "client",
        "description",
    )

    ordering = (
        "-created_at",
    )

    # ================= AUTO SLUG =================
    prepopulated_fields = {
        "slug": ("title",)
    }

    # ================= INLINE =================
    inlines = [
        ProjectGalleryInline
    ]

    # ================= READONLY =================
    readonly_fields = (
        "image_preview",
        "created_at",
        "updated_at",
    )

    # ================= FIELDSETS =================
    fieldsets = (

        (
            "Project Information",
            {
                "fields": (
                    "title",
                    "slug",
                    "client",
                    "date",
                )
            }
        ),

        (
            "Project Classification",
            {
                "fields": (
                    "status",
                    "category",
                    "subcategory",
                    "is_active",
                )
            }
        ),

        (
            "Project Content",
            {
                "fields": (
                    "description",
                )
            }
        ),

        (
            "Featured Image",
            {
                "fields": (
                    "image",
                    "image_preview",
                )
            }
        ),

        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),

    )

    # ================= IMAGE PREVIEW =================
    def image_preview(self, obj):

        if obj.image:

            return format_html(
                """
                <img
                    src="{}"
                    style="
                        width:320px;
                        max-width:100%;
                        border-radius:12px;
                        border:1px solid #ddd;
                        object-fit:cover;
                    "
                >
                """,
                obj.image.url
            )

        return "No image uploaded."

    image_preview.short_description = "Featured Image Preview"