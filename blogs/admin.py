from django.contrib import admin
from django.utils.html import format_html

from .models import (
    BlogHeaderSection,
    BlogPageIntro,
    BlogCategory,
    BlogAuthor,
    BlogTag,
    BlogPost,
)


class OptionalFieldsAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field in form.base_fields.values():
            field.required = False
        return form


@admin.register(BlogHeaderSection)
class BlogHeaderSectionAdmin(OptionalFieldsAdmin):
    list_display = (
        "title",
        "eyebrow",
        "is_active",
        "updated_at",
        "image_preview",
    )
    list_editable = ("is_active",)
    list_filter = ("is_active", "updated_at")
    search_fields = ("title", "eyebrow", "description")
    readonly_fields = ("updated_at", "image_preview")
    ordering = ("-updated_at",)

    fieldsets = (
        (
            "Header Content",
            {
                "fields": (
                    "eyebrow",
                    "title",
                    "description",
                    "background_image",
                    "image_preview",
                    "is_active",
                )
            },
        ),
        ("System", {"fields": ("updated_at",)}),
    )

    def image_preview(self, obj):
        if obj and obj.background_image:
            return format_html(
                '<img src="{}" style="max-width: 320px; height: auto; border-radius: 8px;" />',
                obj.background_image.url,
            )
        return "No image"

    image_preview.short_description = "Background Image Preview"


@admin.register(BlogPageIntro)
class BlogPageIntroAdmin(OptionalFieldsAdmin):
    list_display = ("heading", "volume_label", "is_active", "updated_at")
    list_editable = ("is_active",)
    list_filter = ("is_active", "updated_at")
    search_fields = ("volume_label", "heading", "description")
    readonly_fields = ("updated_at",)
    ordering = ("-updated_at",)

    fieldsets = (
        (
            "Intro Content",
            {
                "fields": (
                    "volume_label",
                    "heading",
                    "description",
                    "is_active",
                )
            },
        ),
        ("System", {"fields": ("updated_at",)}),
    )


@admin.register(BlogCategory)
class BlogCategoryAdmin(OptionalFieldsAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    ordering = ("name",)


@admin.register(BlogAuthor)
class BlogAuthorAdmin(OptionalFieldsAdmin):
    list_display = ("name", "designation", "profile_preview")
    search_fields = ("name", "designation", "bio")
    readonly_fields = ("profile_preview",)
    ordering = ("name",)

    fieldsets = (
        (
            "Author Details",
            {
                "fields": (
                    "name",
                    "designation",
                    "bio",
                    "profile_image",
                    "profile_preview",
                )
            },
        ),
        (
            "Social Links",
            {
                "fields": (
                    "instagram_url",
                    "linkedin_url",
                    "twitter_url",
                )
            },
        ),
    )

    def profile_preview(self, obj):
        if obj and obj.profile_image:
            return format_html(
                '<img src="{}" style="max-width: 120px; height: auto; border-radius: 50%;" />',
                obj.profile_image.url,
            )
        return "No image"

    profile_preview.short_description = "Profile Preview"


@admin.register(BlogTag)
class BlogTagAdmin(OptionalFieldsAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    ordering = ("name",)


@admin.register(BlogPost)
class BlogPostAdmin(OptionalFieldsAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "published_date",
        "read_time",
        "is_featured",
        "is_published",
        "show_on_homepage",
        "updated_at",
        "featured_preview",
    )
    list_editable = ("is_featured", "is_published", "show_on_homepage")
    list_filter = (
        "is_featured",
        "is_published",
        "show_on_homepage",
        "category",
        "author",
        "published_date",
        "updated_at",
    )
    search_fields = ("title", "excerpt", "content", "category__name", "author__name")
    readonly_fields = ("created_at", "updated_at", "featured_preview")
    ordering = ("-published_date", "-created_at")
    filter_horizontal = ("tags",)

    fieldsets = (
        (
            "Post Content",
            {
                "fields": (
                    "title",
                    "slug",
                    "excerpt",
                    "content",
                    "featured_image",
                    "featured_preview",
                )
            },
        ),
        (
            "Post Meta",
            {
                "fields": (
                    "category",
                    "author",
                    "tags",
                    "read_time",
                    "published_date",
                )
            },
        ),
        (
            "Visibility",
            {
                "fields": (
                    "is_featured",
                    "show_on_homepage",
                    "is_published",
                )
            },
        ),
        ("System", {"fields": ("created_at", "updated_at")}),
    )

    def featured_preview(self, obj):
        if obj and obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 240px; height: auto; border-radius: 8px;" />',
                obj.featured_image.url,
            )
        return "No image"

    featured_preview.short_description = "Featured Image Preview"