from django.contrib import admin
from django.utils.html import format_html

from .models import (
    HomePageSettings,
    RippleDifferenceSection,
    MaterialStackSection,
    MaterialStackCard,
    TeamSectionSettings,
    TeamMember,
    ClientTestimonial,
)


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


# =========================================================
# HOME PAGE SETTINGS
# =========================================================
@admin.register(HomePageSettings)
class HomePageSettingsAdmin(SingletonAdmin):

    list_display = (
        "__str__",
        "hero_aria_label",
        "hero_background_image",
        "hero_mobile_image",
        "testimonials_eyebrow",
        "testimonials_heading",
    )

    fieldsets = (
        (
            "Hero Background",
            {
                "fields": (
                    "hero_aria_label",
                    "hero_background_image",
                    "hero_mobile_image",
                    "hero_background_alt",
                )
            }
        ),

        (
            "Hero Content",
            {
                "fields": (
                    "hero_heading",
                    "hero_subheading",
                    "hero_primary_cta_text",
                    "hero_primary_cta_link",
                    "hero_secondary_cta_text",
                    "hero_secondary_cta_link",
                )
            }
        ),

        (
            "Hero Stats",
            {
                "fields": (
                    "hero_stat_1_value",
                    "hero_stat_1_label",
                    "hero_stat_2_value",
                    "hero_stat_2_label",
                    "hero_stat_3_value",
                    "hero_stat_3_label",
                )
            }
        ),

        (
            "Featured Project Text",
            {
                "fields": (
                    "featured_project_label",
                    "featured_project_title",
                    "featured_project_description",
                    "featured_project_type",
                    "featured_project_location",
                    "featured_project_status",
                )
            }
        ),

        (
            "Featured Project Images",
            {
                "fields": (
                    "featured_project_image_1",
                    "featured_project_image_1_alt",
                    "featured_project_image_1_caption",

                    "featured_project_image_2",
                    "featured_project_image_2_alt",
                    "featured_project_image_2_caption",

                    "featured_project_image_3",
                    "featured_project_image_3_alt",
                    "featured_project_image_3_caption",
                )
            }
        ),

        (
            "Testimonials Section",
            {
                "fields": (
                    "testimonials_eyebrow",
                    "testimonials_heading",
                )
            }
        ),

        (
            "Hero Theme Colors",
            {
                "fields": (
                    "overlay_color",
                    "overlay_deep_color",
                    "text_color",
                    "muted_color",
                    "border_color",
                    "card_bg_color",
                    "card_bg_strong_color",
                )
            }
        ),
    )


# =========================================================
# RIPPLE DIFFERENCE
# =========================================================
@admin.register(RippleDifferenceSection)
class RippleDifferenceSectionAdmin(SingletonAdmin):

    list_display = (
        "__str__",
        "is_active",
        "button_text",
        "image_preview",
    )

    list_editable = (
        "is_active",
    )

    search_fields = (
        "subtitle",
        "heading",
        "feature_one_title",
        "feature_two_title",
    )

    readonly_fields = (
        "image_preview",
    )

    fieldsets = (
        (
            "Section Content",
            {
                "fields": (
                    "subtitle",
                    "heading",
                    "description",
                    "button_text",
                    "button_url",
                    "is_active",
                )
            }
        ),

        (
            "Feature One",
            {
                "fields": (
                    "feature_one_title",
                    "feature_one_description",
                )
            }
        ),

        (
            "Feature Two",
            {
                "fields": (
                    "feature_two_title",
                    "feature_two_description",
                )
            }
        ),

        (
            "Images",
            {
                "fields": (
                    "main_image",
                    "secondary_image",
                    "image_preview",
                )
            }
        ),
    )


# =========================================================
# MATERIAL STACK CARD INLINE
# =========================================================
class MaterialStackCardInline(admin.TabularInline):

    model = MaterialStackCard

    extra = 0
    min_num = 0

    fields = (
        "order",
        "meta_num",
        "title",
        "description",
        "image",
        "is_active",
    )

    ordering = ("order",)

    show_change_link = True


# =========================================================
# MATERIAL STACK SECTION
# =========================================================
@admin.register(MaterialStackSection)
class MaterialStackSectionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "eyebrow",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    fieldsets = (
        (
            "Header Content",
            {
                "fields": (
                    "eyebrow",
                    "title",
                )
            }
        ),

        (
            "System",
            {
                "fields": (
                    "is_active",
                )
            }
        ),
    )

    inlines = [MaterialStackCardInline]


# =========================================================
# MATERIAL STACK CARD
# =========================================================
@admin.register(MaterialStackCard)
class MaterialStackCardAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "meta_num",
        "section",
        "order",
        "is_active",
    )

    list_filter = (
        "section",
        "is_active",
    )

    search_fields = (
        "title",
        "meta_num",
        "description",
    )

    ordering = (
        "section",
        "order",
    )

    fieldsets = (
        (
            "Content",
            {
                "fields": (
                    "section",
                    "order",
                    "meta_num",
                    "title",
                    "description",
                )
            }
        ),

        (
            "Media",
            {
                "fields": (
                    "image",
                )
            }
        ),

        (
            "Status",
            {
                "fields": (
                    "is_active",
                )
            }
        ),
    )


# =========================================================
# TEAM MEMBER INLINE
# =========================================================
class TeamMemberInline(admin.TabularInline):

    model = TeamMember

    extra = 0

    fields = (
        "image_preview",
        "image",
        "full_name",
        "designation",
        "display_order",
        "is_active",
    )

    readonly_fields = (
        "image_preview",
    )

    ordering = (
        "display_order",
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="80" '
                'style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


# =========================================================
# TEAM SECTION SETTINGS
# =========================================================
@admin.register(TeamSectionSettings)
class TeamSectionSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "heading",
        "eyebrow",
        "is_active",
    )

    list_editable = (
        "is_active",
    )

    search_fields = (
        "heading",
        "eyebrow",
    )

    inlines = [TeamMemberInline]


# =========================================================
# TEAM MEMBER
# =========================================================
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "full_name",
        "designation",
        "display_order",
        "is_active",
        "updated_at",
    )

    list_editable = (
        "display_order",
        "is_active",
    )

    list_filter = (
        "is_active",
        "section",
    )

    search_fields = (
        "full_name",
        "designation",
    )

    ordering = (
        "display_order",
        "id",
    )

    fields = (
        "section",
        "image_preview",
        "image",
        "alt_text",
        "full_name",
        "designation",
        "display_order",
        "is_active",
    )

    readonly_fields = (
        "image_preview",
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="100" '
                'style="object-fit: cover; border-radius: 6px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


# =========================================================
# CLIENT TESTIMONIALS
# =========================================================
@admin.register(ClientTestimonial)
class ClientTestimonialAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "designation",
        "company",
        "order",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "created_at",
        "company",
    )

    search_fields = (
        "name",
        "designation",
        "company",
        "quote",
    )

    ordering = (
        "order",
    )

    list_editable = (
        "order",
        "is_active",
    )

    fieldsets = (
        (
            "Identity Section",
            {
                "fields": (
                    "name",
                    "designation",
                    "company",
                )
            }
        ),

        (
            "Media",
            {
                "fields": (
                    "image",
                )
            }
        ),

        (
            "Content",
            {
                "fields": (
                    "quote",
                )
            }
        ),

        (
            "Slider Control",
            {
                "fields": (
                    "order",
                    "is_active",
                )
            }
        ),

        (
            "Metadata",
            {
                "fields": (
                    "slug",
                    "created_at",
                )
            }
        ),
    )

    readonly_fields = (
        "slug",
        "created_at",
    )

    list_per_page = 25