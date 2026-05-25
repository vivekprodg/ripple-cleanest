from django import forms
from django.contrib import admin

from .models import RFQDropdownGroup, RFQDropdownOption, QuoteHeroSection


class RFQDropdownOptionInline(admin.TabularInline):
    model = RFQDropdownOption
    extra = 1
    fields = ("label", "value", "order", "is_active")
    ordering = ("order", "id")
    show_change_link = True


@admin.register(RFQDropdownGroup)
class RFQDropdownGroupAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "order", "is_active", "option_count")
    list_filter = ("is_active",)
    search_fields = ("key", "title")
    ordering = ("order", "id")
    list_editable = ("order", "is_active")
    inlines = [RFQDropdownOptionInline]

    def option_count(self, obj):
        return obj.options.count()

    option_count.short_description = "Options"


@admin.register(RFQDropdownOption)
class RFQDropdownOptionAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "group", "order", "is_active")
    list_filter = ("group", "is_active")
    search_fields = ("label", "value", "group__title", "group__key")
    ordering = ("group__order", "order", "id")
    list_editable = ("order", "is_active")


class QuoteHeroSectionForm(forms.ModelForm):
    class Meta:
        model = QuoteHeroSection
        fields = "__all__"
        widgets = {
            "subtitle": forms.Textarea(attrs={"rows": 4}),
            "visual_description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False


@admin.register(QuoteHeroSection)
class QuoteHeroSectionAdmin(admin.ModelAdmin):
    form = QuoteHeroSectionForm

    list_display = ("title", "is_active", "order", "slug", "updated_at")
    list_filter = ("is_active",)
    search_fields = (
        "title",
        "badge_text",
        "subtitle",
        "visual_label",
        "visual_title",
        "visual_description",
        "slug",
    )
    ordering = ("order", "-created_at", "id")
    list_editable = ("is_active", "order")
    readonly_fields = ("slug", "created_at", "updated_at")

    fieldsets = (
        (
            "Hero Content",
            {
                "fields": (
                    "title",
                    "badge_text",
                    "subtitle",
                )
            },
        ),
        (
            "Hero Meta",
            {
                "fields": (
                    "meta_one",
                    "meta_two",
                    "meta_three",
                )
            },
        ),
        (
            "Buttons",
            {
                "fields": (
                    "primary_button_text",
                    "primary_button_link",
                    "secondary_button_text",
                    "secondary_button_link",
                )
            },
        ),
        (
            "Visual Card",
            {
                "fields": (
                    "visual_label",
                    "visual_title",
                    "visual_description",
                )
            },
        ),
        (
            "Media & Styling",
            {
                "fields": (
                    "background_image",
                    "background_image_mobile",
                    "overlay_opacity",
                    "text_color",
                    "accent_color",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": (
                    "is_active",
                    "order",
                )
            },
        ),
        (
            "System",
            {
                "fields": (
                    "slug",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )