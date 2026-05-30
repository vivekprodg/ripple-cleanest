from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Lead(models.Model):
    class LeadType(models.TextChoices):
        RFQ = "quote", "RFQ"
        CONTACT = "contact", "Contact"
        WEBSITE = "website", "Website"
        AD = "ad", "Ad Campaign"
        WHATSAPP = "whatsapp", "WhatsApp"
        SUBSCRIPTION = "subscription", "Subscription"

    class LeadStatus(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    class LeadPriority(models.TextChoices):
        COLD = "cold", "Cold"
        WARM = "warm", "Warm"
        HOT = "hot", "Hot"

    class LeadSource(models.TextChoices):
        WEBSITE = "website", "Website"
        RFQ_FORM = "quote", "RFQ Form"
        CONTACT_FORM = "contact", "Contact Form"
        FACEBOOK = "facebook", "Facebook"
        LINKEDIN = "linkedin", "LinkedIn"
        WHATSAPP = "whatsapp", "WhatsApp"
        SUBSCRIPTION = "subscription", "Subscription Footer"

    # Core contact fields
    name = models.CharField(max_length=255, blank=True, default="")
    email = models.EmailField(blank=True, default="", db_index=True)
    phone = models.CharField(max_length=50, blank=True, default="")

    # Subscription field
    is_subscriber = models.BooleanField(default=False)

    # Lead classification
    lead_type = models.CharField(
        max_length=20,
        choices=LeadType.choices,
        blank=True,
        default=LeadType.WEBSITE,
    )

    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        blank=True,
        default=LeadStatus.NEW,
    )

    priority = models.CharField(
        max_length=20,
        choices=LeadPriority.choices,
        blank=True,
        default=LeadPriority.COLD,
    )

    source = models.CharField(
        max_length=20,
        choices=LeadSource.choices,
        blank=True,
        default=LeadSource.WEBSITE,
    )

    # Common business fields
    budget = models.CharField(max_length=100, blank=True, default="")
    project = models.CharField(max_length=255, blank=True, default="")
    location = models.CharField(max_length=255, blank=True, default="")
    timeline = models.CharField(max_length=100, blank=True, default="")

    # RFQ-specific flexible fields
    typology = models.CharField(max_length=255, blank=True, default="")
    site_status = models.CharField(max_length=255, blank=True, default="")
    services = models.CharField(max_length=255, blank=True, default="")
    referral = models.CharField(max_length=255, blank=True, default="")
    scale = models.CharField(max_length=100, blank=True, default="")
    vision_narrative = models.TextField(blank=True, default="")

    # Internal CRM fields
    avatar = models.URLField(blank=True, default="")
    notes = models.TextField(blank=True, default="")
    tags = models.JSONField(blank=True, default=list)

    # Lifecycle flags
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Lead Assignment

    assigned_to = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="assigned_leads",
    )

    supervisor = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="supervised_leads",
    )

    assigned_at = models.DateTimeField(
    null=True,
    blank=True,
    )

    last_followup_at = models.DateTimeField(
    null=True,
    blank=True,
    )

    next_followup_at = models.DateTimeField(
    null=True,
    blank=True,
    )

    class Meta:
        ordering = ["-created_at", "-id"]
        verbose_name = "Lead"
        verbose_name_plural = "Leads"

    def __str__(self):
        return self.name or self.email or f"Lead #{self.pk}"

    @property
    def display_name(self):
        return self.name or "Lead Name"

    @property
    def display_email(self):
        return self.email or "no-email@example.com"

    @property
    def tags_list(self):
        if isinstance(self.tags, list):
            return self.tags

        if isinstance(self.tags, str) and self.tags.strip():
            return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

        return []

    @property
    def status_label(self):
        return self.get_status_display() if self.status else "New"

    @property
    def priority_label(self):
        return self.get_priority_display() if self.priority else "Cold"

    @property
    def lead_type_label(self):
        return self.get_lead_type_display() if self.lead_type else "Website"

    @property
    def source_label(self):
        return self.get_source_display() if self.source else "Website"