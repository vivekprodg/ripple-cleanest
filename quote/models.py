from django.db import models
from django.utils.text import slugify


class RFQDropdownGroup(models.Model):
    key = models.SlugField(
        unique=True,
        blank=True,
        null=True,
        help_text="Example: typology, site_status, services, budget, referral",
    )
    title = models.CharField(max_length=120, blank=True, default="")

    order = models.PositiveIntegerField(blank=True, null=True, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "RFQ Dropdown Group"
        verbose_name_plural = "RFQ Dropdown Groups"

    def save(self, *args, **kwargs):
        if not self.key and self.title:
            self.key = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self.key or "RFQ Dropdown Group"


class RFQDropdownOption(models.Model):
    group = models.ForeignKey(
        RFQDropdownGroup,
        on_delete=models.CASCADE,
        related_name="options",
        blank=True,
        null=True,
    )
    label = models.CharField(max_length=255, blank=True, default="")
    value = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "RFQ Dropdown Option"
        verbose_name_plural = "RFQ Dropdown Options"

    def save(self, *args, **kwargs):
        if not self.value and self.label:
            self.value = slugify(self.label)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.label or self.value or "RFQ Dropdown Option"


class QuoteHeroSection(models.Model):
    """
    CMS-driven RFQ hero section.
    All fields are optional.
    Create one or more active records in admin and use the active one in the template.
    """

    title = models.CharField(max_length=200, blank=True, default="")
    badge_text = models.CharField(max_length=200, blank=True, default="")
    subtitle = models.TextField(blank=True, default="")

    meta_one = models.CharField(max_length=120, blank=True, default="")
    meta_two = models.CharField(max_length=120, blank=True, default="")
    meta_three = models.CharField(max_length=120, blank=True, default="")

    primary_button_text = models.CharField(max_length=100, blank=True, default="")
    primary_button_link = models.CharField(max_length=255, blank=True, default="")

    secondary_button_text = models.CharField(max_length=100, blank=True, default="")
    secondary_button_link = models.CharField(max_length=255, blank=True, default="")

    visual_label = models.CharField(max_length=200, blank=True, default="")
    visual_title = models.CharField(max_length=200, blank=True, default="")
    visual_description = models.TextField(blank=True, default="")

    background_image = models.ImageField(
        upload_to="quote/hero/",
        blank=True,
        null=True,
    )
    background_image_mobile = models.ImageField(
        upload_to="quote/hero/mobile/",
        blank=True,
        null=True,
        help_text="Optional mobile-specific hero image.",
    )

    overlay_opacity = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        default=None,
        help_text="Overlay strength between 0.00 and 1.00",
    )

    text_color = models.CharField(max_length=20, blank=True, default="")
    accent_color = models.CharField(max_length=20, blank=True, default="")

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(blank=True, null=True, default=0)

    slug = models.SlugField(max_length=220, blank=True, null=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at", "id"]
        verbose_name = "Quote Hero Section"
        verbose_name_plural = "Quote Hero Sections"

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self.slug or "Quote Hero Section"