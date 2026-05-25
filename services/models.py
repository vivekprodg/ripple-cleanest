from uuid import uuid4
import os
import re

from django.db import models

from core.utils.image_optimizer import optimize_uploaded_image


def _normalize_cms_text(value):
    """
    Collapse all whitespace into single spaces so CMS text renders as one
    continuous line/paragraph instead of preserving hidden line breaks.
    """
    if value is None:
        return value
    value = str(value).replace("\r", " ").replace("\n", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _strip_value(value):
    """
    Trim a string without collapsing internal spaces.
    Useful for links/URLs.
    """
    if value is None:
        return value
    return str(value).strip()


def _field_file_changed(instance, field_name: str) -> bool:
    """
    Returns True only when the uploaded file is new or has changed.
    This prevents re-optimizing an already-saved image on every admin save.
    """
    if not instance.pk:
        return True

    try:
        old_instance = type(instance).objects.only(field_name).get(pk=instance.pk)
    except type(instance).DoesNotExist:
        return True

    old_file = getattr(old_instance, field_name, None)
    new_file = getattr(instance, field_name, None)

    old_name = getattr(old_file, "name", "") or ""
    new_name = getattr(new_file, "name", "") or ""

    return old_name != new_name


def _save_optimized_image(instance, field_name: str) -> None:
    """
    Optimizes an uploaded image and saves it with a fresh basename only.
    This avoids nested paths like services/why_choose/services/why_choose/...
    """
    file_obj = getattr(instance, field_name, None)
    if not file_obj:
        return

    optimized = optimize_uploaded_image(file_obj)

    original_name = os.path.basename(getattr(file_obj, "name", "") or "")
    optimized_name = os.path.basename(getattr(optimized, "name", "") or "")

    ext = os.path.splitext(original_name)[1] or os.path.splitext(optimized_name)[1] or ".jpg"
    new_filename = f"{uuid4().hex}{ext}"

    field_file = getattr(instance, field_name)
    field_file.save(new_filename, optimized, save=False)


# ================= SERVICES HERO SECTION =================
class ServicesHeroSection(models.Model):
    """
    CMS model for Services page Hero section.
    Designed as a singleton (only one active record expected).
    """

    kicker = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        help_text="Small top label (e.g. Premium Architecture Services)"
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Main hero heading"
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text="Hero description paragraph"
    )

    hero_image = models.ImageField(
        upload_to="services/hero/",
        max_length=255,
        blank=True,
        null=True,
        help_text="Hero background image"
    )

    btn_primary_text = models.CharField(
        max_length=80,
        blank=True,
        null=True
    )
    btn_primary_link = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    btn_secondary_text = models.CharField(
        max_length=80,
        blank=True,
        null=True
    )
    btn_secondary_link = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    stat_1_text = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    stat_2_text = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    stat_3_text = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    stat_4_text = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Services Hero Section"
        verbose_name_plural = "Services Hero Section"

    def __str__(self):
        return self.title or ""

    def save(self, *args, **kwargs):
        if not self.pk and ServicesHeroSection.objects.exists():
            raise ValueError("Only one ServicesHeroSection instance is allowed.")

        self.kicker = _normalize_cms_text(self.kicker)
        self.title = _normalize_cms_text(self.title)
        self.description = _normalize_cms_text(self.description)

        self.btn_primary_text = _normalize_cms_text(self.btn_primary_text)
        self.btn_primary_link = _strip_value(self.btn_primary_link)

        self.btn_secondary_text = _normalize_cms_text(self.btn_secondary_text)
        self.btn_secondary_link = _strip_value(self.btn_secondary_link)

        self.stat_1_text = _normalize_cms_text(self.stat_1_text)
        self.stat_2_text = _normalize_cms_text(self.stat_2_text)
        self.stat_3_text = _normalize_cms_text(self.stat_3_text)
        self.stat_4_text = _normalize_cms_text(self.stat_4_text)

        if self.hero_image and _field_file_changed(self, "hero_image"):
            _save_optimized_image(self, "hero_image")

        super().save(*args, **kwargs)


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="services/", max_length=255)
    is_active = models.BooleanField(default=True, help_text="Show on the Services page")
    show_on_home = models.BooleanField(default=False, help_text="Show on the homepage services section")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = _normalize_cms_text(self.title)
        self.description = _normalize_cms_text(self.description)
        super().save(*args, **kwargs)


class WhyChooseSection(models.Model):
    chip_text = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        default="Crafted for impact"
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    subtitle = models.TextField(
        blank=True,
        null=True
    )

    card_heading = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    card_description = models.TextField(
        blank=True,
        null=True
    )

    card_image = models.ImageField(
        upload_to="services/why_choose/",
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Why Choose Section"
        verbose_name_plural = "Why Choose Section"

    def __str__(self):
        return self.title or ""

    def save(self, *args, **kwargs):
        if not self.pk and WhyChooseSection.objects.exists():
            raise ValueError("Only one WhyChooseSection instance is allowed.")

        self.chip_text = _normalize_cms_text(self.chip_text)
        self.title = _normalize_cms_text(self.title)
        self.subtitle = _normalize_cms_text(self.subtitle)
        self.card_heading = _normalize_cms_text(self.card_heading)
        self.card_description = _normalize_cms_text(self.card_description)

        if self.card_image and _field_file_changed(self, "card_image"):
            _save_optimized_image(self, "card_image")

        super().save(*args, **kwargs)


class WhyChooseFeature(models.Model):
    section = models.ForeignKey(
        WhyChooseSection,
        on_delete=models.CASCADE,
        related_name="features"
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    title = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Why Choose Feature"
        verbose_name_plural = "Why Choose Features"
        ordering = ["id"]

    def __str__(self):
        return self.title or ""

    def save(self, *args, **kwargs):
        self.icon = _normalize_cms_text(self.icon)
        self.title = _normalize_cms_text(self.title)
        self.description = _normalize_cms_text(self.description)
        super().save(*args, **kwargs)


# ================= SERVICES EXTRA SECTIONS =================
class ServicesExtraSection(models.Model):
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # PROCESS
    process_label = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )
    process_title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    process_subtitle = models.TextField(
        blank=True,
        null=True
    )

    # METRICS
    metrics_label = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )
    metrics_title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    metrics_subtitle = models.TextField(
        blank=True,
        null=True
    )

    # FAQ
    faq_label = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )
    faq_title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    faq_subtitle = models.TextField(
        blank=True,
        null=True
    )

    faq_side_title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    faq_side_description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Services Extra Section"
        verbose_name_plural = "Services Extra Sections"

    def __str__(self):
        return self.title or "Services Extra Section"

    def save(self, *args, **kwargs):
        if not self.pk and ServicesExtraSection.objects.exists():
            raise ValueError("Only one ServicesExtraSection instance is allowed.")

        self.title = _normalize_cms_text(self.title)

        self.process_label = _normalize_cms_text(self.process_label)
        self.process_title = _normalize_cms_text(self.process_title)
        self.process_subtitle = _normalize_cms_text(self.process_subtitle)

        self.metrics_label = _normalize_cms_text(self.metrics_label)
        self.metrics_title = _normalize_cms_text(self.metrics_title)
        self.metrics_subtitle = _normalize_cms_text(self.metrics_subtitle)

        self.faq_label = _normalize_cms_text(self.faq_label)
        self.faq_title = _normalize_cms_text(self.faq_title)
        self.faq_subtitle = _normalize_cms_text(self.faq_subtitle)

        self.faq_side_title = _normalize_cms_text(self.faq_side_title)
        self.faq_side_description = _normalize_cms_text(self.faq_side_description)

        super().save(*args, **kwargs)

        # Auto-create related singleton children
        ServiceSpotlight.objects.get_or_create(section=self)
        ServiceCTA.objects.get_or_create(section=self)


class ServiceSpotlight(models.Model):
    section = models.OneToOneField(
        ServicesExtraSection,
        on_delete=models.CASCADE,
        related_name="spotlight",
    )

    label = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    subtitle = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="services/spotlight/",
        max_length=255,
        blank=True,
        null=True
    )

    primary_button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    primary_button_link = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    secondary_button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    secondary_button_link = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Service Spotlight"
        verbose_name_plural = "Service Spotlight"

    def __str__(self):
        return self.title or "Service Spotlight"

    def save(self, *args, **kwargs):
        self.label = _normalize_cms_text(self.label)
        self.title = _normalize_cms_text(self.title)
        self.subtitle = _normalize_cms_text(self.subtitle)

        self.primary_button_text = _normalize_cms_text(self.primary_button_text)
        self.primary_button_link = _strip_value(self.primary_button_link)

        self.secondary_button_text = _normalize_cms_text(self.secondary_button_text)
        self.secondary_button_link = _strip_value(self.secondary_button_link)

        if self.image and _field_file_changed(self, "image"):
            _save_optimized_image(self, "image")

        super().save(*args, **kwargs)


class ServiceSpotlightItem(models.Model):
    section = models.ForeignKey(
        ServicesExtraSection,
        on_delete=models.CASCADE,
        related_name="spotlight_items",
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Service Spotlight Item"
        verbose_name_plural = "Service Spotlight Items"
        ordering = ["id"]

    def __str__(self):
        return self.title or "Spotlight Item"

    def save(self, *args, **kwargs):
        self.icon = _normalize_cms_text(self.icon)
        self.title = _normalize_cms_text(self.title)
        self.description = _normalize_cms_text(self.description)
        super().save(*args, **kwargs)


class ServiceProcessStep(models.Model):
    section = models.ForeignKey(
        ServicesExtraSection,
        on_delete=models.CASCADE,
        related_name="process_steps",
    )

    number = models.IntegerField(
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Service Process Step"
        verbose_name_plural = "Service Process Steps"
        ordering = ["number", "id"]

    def __str__(self):
        return self.title or "Process Step"

    def save(self, *args, **kwargs):
        self.title = _normalize_cms_text(self.title)
        self.description = _normalize_cms_text(self.description)
        self.icon = _normalize_cms_text(self.icon)
        super().save(*args, **kwargs)


class ServiceMetric(models.Model):
    section = models.ForeignKey(
        ServicesExtraSection,
        on_delete=models.CASCADE,
        related_name="metrics",
    )

    value = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Service Metric"
        verbose_name_plural = "Service Metrics"
        ordering = ["id"]

    def __str__(self):
        return self.name or "Metric"

    def save(self, *args, **kwargs):
        self.value = _normalize_cms_text(self.value)
        self.name = _normalize_cms_text(self.name)
        self.description = _normalize_cms_text(self.description)
        super().save(*args, **kwargs)


class ServiceFAQ(models.Model):
    section = models.ForeignKey(
        ServicesExtraSection,
        on_delete=models.CASCADE,
        related_name="faqs",
    )

    question = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    answer = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Service FAQ"
        verbose_name_plural = "Service FAQs"
        ordering = ["id"]

    def __str__(self):
        return self.question or "FAQ"

    def save(self, *args, **kwargs):
        self.question = _normalize_cms_text(self.question)
        self.answer = _normalize_cms_text(self.answer)
        super().save(*args, **kwargs)


class ServiceCTA(models.Model):
    section = models.OneToOneField(
        ServicesExtraSection,
        on_delete=models.CASCADE,
        related_name="cta",
    )

    label = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    primary_button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    primary_button_link = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    secondary_button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    secondary_button_link = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Service CTA"
        verbose_name_plural = "Service CTA"

    def __str__(self):
        return self.title or "Service CTA"

    def save(self, *args, **kwargs):
        self.label = _normalize_cms_text(self.label)
        self.title = _normalize_cms_text(self.title)
        self.description = _normalize_cms_text(self.description)

        self.primary_button_text = _normalize_cms_text(self.primary_button_text)
        self.primary_button_link = _strip_value(self.primary_button_link)

        self.secondary_button_text = _normalize_cms_text(self.secondary_button_text)
        self.secondary_button_link = _strip_value(self.secondary_button_link)

        super().save(*args, **kwargs)