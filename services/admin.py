from django.contrib import admin
from django.db import models as dj_models
from django.forms import Textarea

from .models import (
    Service,
    ServicesHeroSection,
    WhyChooseFeature,
    WhyChooseSection,
    ServicesExtraSection,
    ServiceSpotlight,
    ServiceSpotlightItem,
    ServiceProcessStep,
    ServiceMetric,
    ServiceFAQ,
    ServiceCTA,
)


# =========================================================
# SINGLETON ADMIN MIXIN (ONLY ONE ROW ALLOWED)
# =========================================================
class SingletonModelAdmin(admin.ModelAdmin):
    """
    Restricts model to a single instance.
    Prevents creation of multiple CMS records.
    """

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# =========================================================
# WHY CHOOSE FEATURE INLINE
# =========================================================
class WhyChooseFeatureInline(admin.TabularInline):
    model = WhyChooseFeature
    extra = 3
    fields = ("icon", "title", "description")
    show_change_link = True


# =========================================================
# SERVICES HERO ADMIN
# =========================================================
@admin.register(ServicesHeroSection)
class ServicesHeroSectionAdmin(SingletonModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    search_fields = ("kicker", "title", "description")

    formfield_overrides = {
        dj_models.TextField: {"widget": Textarea(attrs={"rows": 4})},
    }

    fieldsets = (
        ("Hero Content", {
            "fields": (
                "kicker",
                "title",
                "description",
            )
        }),
        ("Hero Media", {
            "fields": (
                "hero_image",
            )
        }),
        ("Buttons", {
            "fields": (
                "btn_primary_text",
                "btn_primary_link",
                "btn_secondary_text",
                "btn_secondary_link",
            )
        }),
        ("Stats", {
            "fields": (
                "stat_1_text",
                "stat_2_text",
                "stat_3_text",
                "stat_4_text",
            )
        }),
        ("System", {
            "fields": (
                "is_active",
            )
        }),
    )


# =========================================================
# SERVICE ADMIN
# =========================================================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "show_on_home", "is_active")
    list_editable = ("order", "show_on_home", "is_active")
    list_filter = ("is_active", "show_on_home")
    search_fields = ("title", "description")
    ordering = ("order", "id")
    list_per_page = 20

    formfield_overrides = {
        dj_models.TextField: {"widget": Textarea(attrs={"rows": 4})},
    }

    fieldsets = (
        ("Service Content", {
            "fields": ("title", "description", "image")
        }),
        ("Display Settings", {
            "fields": ("is_active", "show_on_home", "order")
        }),
    )


# =========================================================
# WHY CHOOSE SECTION ADMIN
# =========================================================
@admin.register(WhyChooseSection)
class WhyChooseSectionAdmin(SingletonModelAdmin):
    list_display = ("title",)
    search_fields = ("chip_text", "title", "subtitle", "card_heading", "card_description")

    formfield_overrides = {
        dj_models.TextField: {"widget": Textarea(attrs={"rows": 4})},
    }

    fieldsets = (
        ("Main Content", {
            "fields": (
                "chip_text",
                "title",
                "subtitle",
            )
        }),
        ("Card Content", {
            "fields": (
                "card_heading",
                "card_description",
                "card_image",
            )
        }),
    )

    inlines = [WhyChooseFeatureInline]


# =========================================================
# SERVICES EXTRA SECTION INLINES
# =========================================================
class ServiceSpotlightInline(admin.StackedInline):
    model = ServiceSpotlight
    extra = 0
    max_num = 1
    can_delete = False

    fields = (
        "label",
        "title",
        "subtitle",
        "image",
        "primary_button_text",
        "primary_button_link",
        "secondary_button_text",
        "secondary_button_link",
    )


class ServiceSpotlightItemInline(admin.TabularInline):
    model = ServiceSpotlightItem
    extra = 1
    fields = (
        "icon",
        "title",
        "description",
    )
    show_change_link = True


class ServiceProcessStepInline(admin.TabularInline):
    model = ServiceProcessStep
    extra = 1
    fields = (
        "number",
        "title",
        "description",
        "icon",
    )
    show_change_link = True


class ServiceMetricInline(admin.TabularInline):
    model = ServiceMetric
    extra = 1
    fields = (
        "value",
        "name",
        "description",
    )
    show_change_link = True


class ServiceFAQInline(admin.TabularInline):
    model = ServiceFAQ
    extra = 1
    fields = (
        "question",
        "answer",
    )
    show_change_link = True


class ServiceCTAInline(admin.StackedInline):
    model = ServiceCTA
    extra = 0
    max_num = 1
    can_delete = False

    fields = (
        "label",
        "title",
        "description",
        "primary_button_text",
        "primary_button_link",
        "secondary_button_text",
        "secondary_button_link",
    )


# =========================================================
# SERVICES EXTRA SECTION ADMIN
# =========================================================
@admin.register(ServicesExtraSection)
class ServicesExtraSectionAdmin(SingletonModelAdmin):
    list_display = ("title",)
    search_fields = (
        "title",
        "process_label",
        "process_title",
        "process_subtitle",
        "metrics_label",
        "metrics_title",
        "metrics_subtitle",
        "faq_label",
        "faq_title",
        "faq_subtitle",
        "faq_side_title",
        "faq_side_description",
    )

    formfield_overrides = {
        dj_models.TextField: {"widget": Textarea(attrs={"rows": 4})},
    }

    fieldsets = (
        ("Section Settings", {
            "fields": ("title",)
        }),
        ("Process Header", {
            "fields": (
                "process_label",
                "process_title",
                "process_subtitle",
            )
        }),
        ("Metrics Header", {
            "fields": (
                "metrics_label",
                "metrics_title",
                "metrics_subtitle",
            )
        }),
        ("FAQ Header", {
            "fields": (
                "faq_label",
                "faq_title",
                "faq_subtitle",
            )
        }),
        ("FAQ Side Content", {
            "fields": (
                "faq_side_title",
                "faq_side_description",
            )
        }),
    )

    inlines = [
        ServiceSpotlightInline,
        ServiceSpotlightItemInline,
        ServiceProcessStepInline,
        ServiceMetricInline,
        ServiceFAQInline,
        ServiceCTAInline,
    ]


# =========================================================
# STANDALONE ADMINS
# =========================================================
@admin.register(ServiceSpotlight)
class ServiceSpotlightAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "section")
    search_fields = ("label", "title", "subtitle")
    list_select_related = ("section",)

    formfield_overrides = {
        dj_models.TextField: {"widget": Textarea(attrs={"rows": 4})},
    }

    fieldsets = (
        ("Spotlight Content", {
            "fields": (
                "section",
                "label",
                "title",
                "subtitle",
                "image",
            )
        }),
        ("Buttons", {
            "fields": (
                "primary_button_text",
                "primary_button_link",
                "secondary_button_text",
                "secondary_button_link",
            )
        }),
    )


@admin.register(ServiceSpotlightItem)
class ServiceSpotlightItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "section")
    search_fields = ("icon", "title", "description")
    list_select_related = ("section",)

    formfield_overrides = {
        dj_models.TextField: {"widget": Textarea(attrs={"rows": 4})},
    }

    fieldsets = (
        ("Item Content", {
            "fields": (
                "section",
                "icon",
                "title",
                "description",
            )
        }),
    )


@admin.register(ServiceProcessStep)
class ServiceProcessStepAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "title", "section")
    search_fields = ("title", "description", "icon")
    list_filter = ("section",)
    list_select_related = ("section",)

    formfield_overrides = {
        dj_models.TextField: {"widget": Textarea(attrs={"rows": 4})},
    }

    fieldsets = (
        ("Step Content", {
            "fields": (
                "section",
                "number",
                "title",
                "description",
                "icon",
            )
        }),
    )


@admin.register(ServiceMetric)
class ServiceMetricAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "value", "section")
    search_fields = ("value", "name", "description")
    list_filter = ("section",)
    list_select_related = ("section",)

    formfield_overrides = {
        dj_models.TextField: {"widget": Textarea(attrs={"rows": 4})},
    }

    fieldsets = (
        ("Metric Content", {
            "fields": (
                "section",
                "value",
                "name",
                "description",
            )
        }),
    )


@admin.register(ServiceFAQ)
class ServiceFAQAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "section")
    search_fields = ("question", "answer")
    list_filter = ("section",)
    list_select_related = ("section",)

    formfield_overrides = {
        dj_models.TextField: {"widget": Textarea(attrs={"rows": 4})},
    }

    fieldsets = (
        ("FAQ Content", {
            "fields": (
                "section",
                "question",
                "answer",
            )
        }),
    )


@admin.register(ServiceCTA)
class ServiceCTAAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "section")
    search_fields = (
        "label",
        "title",
        "description",
        "primary_button_text",
        "secondary_button_text",
    )
    list_select_related = ("section",)

    formfield_overrides = {
        dj_models.TextField: {"widget": Textarea(attrs={"rows": 4})},
    }

    fieldsets = (
        ("CTA Content", {
            "fields": (
                "section",
                "label",
                "title",
                "description",
            )
        }),
        ("Buttons", {
            "fields": (
                "primary_button_text",
                "primary_button_link",
                "secondary_button_text",
                "secondary_button_link",
            )
        }),
    )