from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.utils.image_optimizer import optimize_uploaded_image


def _optimize_image_field(instance, field_name: str) -> None:
    field_file = getattr(instance, field_name, None)
    if not field_file:
        return

    # Only optimize newly uploaded files.
    if getattr(field_file, "_committed", True):
        return

    try:
        optimized_file = optimize_uploaded_image(field_file)
        setattr(instance, field_name, optimized_file)
    except Exception:
        # Fail safe: keep original upload unchanged.
        pass


class ContactPageSettingsQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ContactPageSettings(models.Model):
    """
    Singleton CMS model for the contact page.
    All fields are optional.
    """

    is_active = models.BooleanField(default=True, blank=True)

    page_title = models.CharField(max_length=200, blank=True, default="Premium Contact Us")
    seo_title = models.CharField(max_length=255, blank=True, default="")
    seo_description = models.TextField(blank=True, default="")

    hero_badge = models.CharField(max_length=120, blank=True, default="Premium Architecture Studio")
    hero_title = models.CharField(max_length=200, blank=True, default="Contact Us")
    hero_description = models.TextField(
        blank=True,
        default=(
            "Reach out for architecture, interior design, consultation, renovation, "
            "planning, or project collaboration. We create modern premium spaces "
            "with timeless aesthetics."
        ),
    )
    hero_background_image = models.ImageField(
        upload_to="contact/hero/",
        blank=True,
        null=True,
    )
    hero_overlay_strength = models.PositiveSmallIntegerField(
        default=55,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    top_cards_heading = models.CharField(max_length=150, blank=True, default="")
    top_cards_subheading = models.TextField(blank=True, default="")

    left_section_badge = models.CharField(max_length=120, blank=True, default="Premium Support")
    left_section_title = models.CharField(
        max_length=200,
        blank=True,
        default="Let's Build Something Beautiful",
    )
    left_section_description = models.TextField(
        blank=True,
        default=(
            "Share your ideas and project requirements with us. We provide architecture, "
            "interior design, planning, consultation, and renovation services with premium quality."
        ),
    )
    left_section_background_image = models.ImageField(
        upload_to="contact/left_panel/",
        blank=True,
        null=True,
    )

    form_title = models.CharField(max_length=200, blank=True, default="Send Inquiry")
    form_subtitle = models.TextField(
        blank=True,
        default="Fill the form below and our team will contact you shortly.",
    )
    submit_button_text = models.CharField(max_length=120, blank=True, default="Start Your Project")
    success_message = models.CharField(
        max_length=255,
        blank=True,
        default="Thank you! Your inquiry has been submitted successfully.",
    )

    map_title = models.CharField(max_length=200, blank=True, default="Visit Our Studio")
    map_description = models.TextField(
        blank=True,
        default="Experience modern architecture and premium interior solutions.",
    )
    map_embed_url = models.CharField(max_length=1000, blank=True, default="")
    map_location_text = models.CharField(max_length=255, blank=True, default="Kathmandu, Nepal")

    contact_email = models.EmailField(blank=True, default="")
    contact_phone = models.CharField(max_length=100, blank=True, default="")
    contact_location = models.CharField(max_length=255, blank=True, default="")
    contact_address = models.CharField(max_length=255, blank=True, default="")

    social_heading = models.CharField(max_length=150, blank=True, default="")
    instagram_url = models.CharField(max_length=500, blank=True, default="")
    facebook_url = models.CharField(max_length=500, blank=True, default="")
    linkedin_url = models.CharField(max_length=500, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = ContactPageSettingsQuerySet.as_manager()

    class Meta:
        verbose_name = "Contact Page Settings"
        verbose_name_plural = "Contact Page Settings"

    def __str__(self):
        return self.page_title or "Contact Page Settings"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        _optimize_image_field(self, "hero_background_image")
        _optimize_image_field(self, "left_section_background_image")
        super().save(*args, **kwargs)


class ContactTopCard(models.Model):
    """
    Floating cards on the top of the contact page.
    """

    settings = models.ForeignKey(
        ContactPageSettings,
        related_name="top_cards",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    icon_text = models.CharField(max_length=20, blank=True, default="")
    title = models.CharField(max_length=120, blank=True, default="")
    value = models.CharField(max_length=255, blank=True, default="")
    link_url = models.CharField(max_length=500, blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True)

    class Meta:
        verbose_name = "Contact Top Card"
        verbose_name_plural = "Contact Top Cards"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title or self.value or "Contact Top Card"


class ContactInfoBox(models.Model):
    """
    Left panel info rows: email, call us, studio location, etc.
    """

    settings = models.ForeignKey(
        ContactPageSettings,
        related_name="info_boxes",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    icon_text = models.CharField(max_length=20, blank=True, default="")
    title = models.CharField(max_length=120, blank=True, default="")
    value = models.CharField(max_length=255, blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True)

    class Meta:
        verbose_name = "Contact Info Box"
        verbose_name_plural = "Contact Info Boxes"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.title or self.value or "Contact Info Box"


class ContactSocialLink(models.Model):
    """
    Social icons/links shown in the contact page.
    """

    settings = models.ForeignKey(
        ContactPageSettings,
        related_name="social_links",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    label = models.CharField(max_length=80, blank=True, default="")
    icon_text = models.CharField(max_length=20, blank=True, default="")
    url = models.CharField(max_length=500, blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True)

    class Meta:
        verbose_name = "Contact Social Link"
        verbose_name_plural = "Contact Social Links"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return self.label or "Contact Social Link"


class ContactInquiry(models.Model):
    """
    Stores submitted contact form inquiries.
    """

    STATUS_NEW = "new"
    STATUS_REVIEWED = "reviewed"
    STATUS_REPLIED = "replied"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_REVIEWED, "Reviewed"),
        (STATUS_REPLIED, "Replied"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    full_name = models.CharField(max_length=200, blank=True, default="")
    email_address = models.EmailField(blank=True, default="")
    phone_number = models.CharField(max_length=100, blank=True, default="")
    project_details = models.TextField(blank=True, default="")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        blank=True,
    )

    source_page = models.CharField(max_length=255, blank=True, default="")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, default="")
    admin_notes = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.full_name or self.email_address or "Contact Inquiry"