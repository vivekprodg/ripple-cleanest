from django.db import models

class HeroTypographySettings(models.Model):
    page_type = models.CharField(
        max_length=50,
        unique=True,
    )

    title_font_family = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
    )
    title_font_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
    )
    title_font_weight = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        default="",
    )
    title_font_size_desktop = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    title_font_size_tablet = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    title_font_size_mobile = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    title_line_height = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    title_letter_spacing = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    title_text_transform = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    title_color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
    )

    body_font_family = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
    )
    body_font_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
    )
    body_font_weight = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        default="",
    )
    body_font_size_desktop = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    body_font_size_tablet = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    body_font_size_mobile = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    body_line_height = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    body_letter_spacing = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    body_text_transform = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    body_color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
    )

    button_font_family = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
    )
    button_font_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
    )
    button_font_weight = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        default="",
    )
    button_font_size = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    button_letter_spacing = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    button_text_transform = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    button_color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
    )

    stats_font_family = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
    )
    stats_font_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
    )
    stats_font_weight = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        default="",
    )
    stats_font_size = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    stats_line_height = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    stats_letter_spacing = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    stats_text_transform = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    stats_color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
    )

    panel_font_family = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
    )
    panel_font_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
    )
    panel_font_weight = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        default="",
    )
    panel_font_size = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    panel_line_height = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    panel_letter_spacing = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    panel_text_transform = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
    )
    panel_color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="",
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["page_type"]
        verbose_name = "Hero Typography Setting"
        verbose_name_plural = "Hero Typography Settings"

    def __str__(self):
        return f"{self.page_type or 'Hero'} Typography"


class NavItem(models.Model):
    TYPE_CHOICES = [
        ("link", "Link"),
        ("cta", "CTA Button"),
    ]

    title = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default="link"
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Navigation Item"
        verbose_name_plural = "Navigation Items"

    def __str__(self):
        return self.title


class SiteLogo(models.Model):
    logo = models.ImageField(
        upload_to="logo/",
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Logo"
        verbose_name_plural = "Site Logo"

    def __str__(self):
        return "Site Logo"

class NavbarSettings(models.Model):
    nav_bg_color = models.CharField(
        max_length=20,
        blank=True,
        default="#ffffff"
    )
    nav_text_color = models.CharField(
        max_length=20,
        blank=True,
        default="#6b7280"
    )
    nav_text_dark = models.CharField(
        max_length=20,
        blank=True,
        default="#111827"
    )
    nav_hover_color = models.CharField(
        max_length=20,
        blank=True,
        default="#111827"
    )
    nav_border_color = models.CharField(
        max_length=30,
        blank=True,
        default="rgba(0, 0, 0, 0.08)"
    )
    nav_padding_y = models.PositiveIntegerField(default=12)
    nav_padding_x = models.PositiveIntegerField(default=20)
    nav_logo_height = models.PositiveIntegerField(default=40)

    class Meta:
        verbose_name = "Navbar Settings"
        verbose_name_plural = "Navbar Settings"

    def __str__(self):
        return "Navbar Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class FooterSettings(models.Model):
    ALIGNMENT_CHOICES = [
        ("left", "Left"),
        ("center", "Center"),
        ("space-between", "Space Between"),
    ]

    SOCIAL_ALIGNMENT_CHOICES = [
        ("left", "Left"),
        ("center", "Center"),
        ("right", "Right"),
    ]

    background_color = models.CharField(
        max_length=20,
        blank=True,
        default="#080808"
    )
    border_color = models.CharField(
        max_length=20,
        blank=True,
        default="#1a1a1a"
    )
    text_color = models.CharField(
        max_length=20,
        blank=True,
        default="#f4f4f0"
    )
    muted_color = models.CharField(
        max_length=20,
        blank=True,
        default="#8a8a8a"
    )
    accent_color = models.CharField(
        max_length=20,
        blank=True,
        default="#b89768"
    )
    company_name = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )
    company_description = models.TextField(
        blank=True,
        default=""
    )
    projects_heading = models.CharField(
        max_length=50,
        blank=True,
        default="Projects"
    )
    practice_heading = models.CharField(
        max_length=50,
        blank=True,
        default="Practice"
    )
    subscription_heading = models.CharField(
        max_length=50,
        blank=True,
        default="Subscription"
    )
    newsletter_text = models.TextField(
        blank=True,
        default="Sign up to receive our biannual curation of architectural insights.",
    )
    newsletter_placeholder = models.CharField(
        max_length=100,
        blank=True,
        default="Email Address"
    )
    newsletter_button_text = models.CharField(
        max_length=50,
        blank=True,
        default="Join"
    )
    newsletter_action_url = models.CharField(
        max_length=255,
        blank=True,
        default="#"
    )
    copyright_text = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )
    bottom_alignment = models.CharField(
        max_length=20,
        choices=ALIGNMENT_CHOICES,
        default="space-between",
    )
    social_alignment = models.CharField(
        max_length=20,
        choices=SOCIAL_ALIGNMENT_CHOICES,
        default="center",
    )
    logo_image = models.ImageField(
        upload_to="footer/logo/",
        blank=True,
        null=True
    )
    logo_alt = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )
    logo_url = models.CharField(
        max_length=255,
        blank=True,
        default="/"
    )

    class Meta:
        verbose_name = "Footer Settings"
        verbose_name_plural = "Footer Settings"

    def __str__(self):
        return self.company_name or "Footer Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class FooterProjectLink(models.Model):
    footer = models.ForeignKey(
        FooterSettings,
        related_name="project_links",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Footer Project Link"
        verbose_name_plural = "Footer Project Links"

    def __str__(self):
        return self.title


class FooterPracticeLink(models.Model):
    footer = models.ForeignKey(
        FooterSettings,
        related_name="practice_links",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Footer Practice Link"
        verbose_name_plural = "Footer Practice Links"

    def __str__(self):
        return self.title


class FooterSocialLink(models.Model):
    ICON_CHOICES = [
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("x", "X"),
        ("facebook", "Facebook"),
        ("custom", "Custom SVG"),
    ]

    footer = models.ForeignKey(
        FooterSettings,
        related_name="social_links",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=500)
    icon_name = models.CharField(
        max_length=20,
        choices=ICON_CHOICES,
        default="instagram"
    )
    icon_svg = models.TextField(blank=True, default="")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Footer Social Link"
        verbose_name_plural = "Footer Social Links"

    def __str__(self):
        return self.name
    
class WhatsAppSettings(models.Model):
    phone_number = models.CharField(
        max_length=20,
        default="9779802113456",
        help_text="WhatsApp number with country code (no +, no spaces)"
    )

    prefilled_text = models.TextField(
        default="Hello! I would like to get more information about your services.",
        help_text="Default WhatsApp message"
    )

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "WhatsApp Settings"
        verbose_name_plural = "WhatsApp Settings"

    def __str__(self):
        return "WhatsApp Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)