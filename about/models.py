from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile

from core.utils.image_optimizer import optimize_uploaded_image

# =========================================
# ABSTRACT SINGLETON MODEL
# =========================================
class SingletonModel(models.Model):
    """
    Base singleton model for CMS-style single-record sections.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def delete(self, *args, **kwargs):
        raise ValidationError("Singleton models cannot be deleted.")

    def __str__(self):
        return self.__class__.__name__

# =========================================
# ABOUT PAGE SETTINGS
# =========================================
class AboutPageSettings(SingletonModel):
    """
    Global CMS settings for About page.
    Everything optional.
    """

    page_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default=""
    )

    meta_description = models.TextField(
        blank=True,
        null=True,
        default=""
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "About Page Settings"
        verbose_name_plural = "About Page Settings"

    def __str__(self):
        return self.page_title or "About Page Settings"

# =========================================
# ABOUT HERO SECTION
# =========================================
class AboutHeroSection(SingletonModel):
    """
    CMS-driven About Hero Section (fully optional fields)
    """

    is_active = models.BooleanField(default=True)

    eyebrow = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        default=""
    )

    title = models.TextField(
        blank=True,
        null=True,
        default=""
    )

    description = models.TextField(
        blank=True,
        null=True,
        default=""
    )

    background_image = models.ImageField(
        upload_to="about/hero/",
        blank=True,
        null=True
    )

    primary_button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default=""
    )

    primary_button_url = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        default=""
    )

    secondary_button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default=""
    )

    secondary_button_url = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        default=""
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "About Hero Section"
        verbose_name_plural = "About Hero Section"

    def __str__(self):
        return "About Hero Section"

    def save(self, *args, **kwargs):
        """
        Optional image optimization (safe fallback)
        """
        if self.background_image:
            try:
                optimized_image = optimize_uploaded_image(self.background_image)
                self.background_image.save(
                    optimized_image.name,
                    ContentFile(optimized_image.read()),
                    save=False
                )
            except Exception:
                pass

        super().save(*args, **kwargs)

# =========================================
# ABOUT OVERVIEW SECTION
# =========================================
class AboutOverviewSection(SingletonModel):
    """
    CMS-driven Overview section for About page.
    Acts as the single source of truth for:
    - subtitle
    - title
    - description
    - button text
    - button link
    - main image
    - secondary image
    - section visibility
    """

    # =====================================
    # SECTION CONTROL
    # =====================================
    is_active = models.BooleanField(
        default=True,
        help_text="Show or hide the overview section."
    )

    # =====================================
    # CONTENT
    # =====================================
    subtitle = models.CharField(
        max_length=120,
        default="Firm Overview",
        help_text="Small upper heading above the title."
    )

    title = models.CharField(
        max_length=300,
        default="Designing spaces with purpose. Creating a continuous ripple in modern living.",
        help_text="Main overview heading."
    )

    description = models.TextField(
        default=(
            "We believe in an architectural philosophy that bridges "
            "the gap between the built environment and human experience. "
            "By eliminating rigid boundaries and uncompromising constraints, "
            "we shape fluid, dynamic spaces tailored to exact specifications."
        ),
        help_text="Overview section description."
    )

    # =====================================
    # BUTTON
    # =====================================
    button_text = models.CharField(
        max_length=100,
        default="Discover Our Office",
        blank=True
    )

    button_link = models.CharField(
        max_length=300,
        default="#office",
        blank=True
    )

    # =====================================
    # IMAGES
    # =====================================
    main_image = models.ImageField(
        upload_to="about/overview/",
        blank=True,
        null=True,
        help_text="Primary overview image."
    )

    secondary_image = models.ImageField(
        upload_to="about/overview/",
        blank=True,
        null=True,
        help_text="Secondary overlapping image."
    )

    # =====================================
    # IMAGE ALT TEXT
    # =====================================
    main_image_alt = models.CharField(
        max_length=200,
        default="Modern architectural exterior with clean lines",
        blank=True
    )

    secondary_image_alt = models.CharField(
        max_length=200,
        default="Refined interior design detailing",
        blank=True
    )

    # =====================================
    # META
    # =====================================
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "About Overview Section"
        verbose_name_plural = "About Overview Section"

    def __str__(self):
        return "About Overview Section"
    
class VisionMissionValues(models.Model):
    section_title = models.CharField(max_length=255, default="Vision, Mission & Values")

    is_active = models.BooleanField(default=True)

    # =========================
    # VISION
    # =========================
    vision_title = models.CharField(max_length=100, default="Vision")
    vision_text = models.TextField()

    vision_icon = models.CharField(
        max_length=100,
        default="fa-solid fa-eye",
        help_text="FontAwesome class"
    )

    # =========================
    # MISSION
    # =========================
    mission_title = models.CharField(max_length=100, default="Mission")
    mission_text = models.TextField()

    mission_icon = models.CharField(
        max_length=100,
        default="fa-solid fa-compass",
        help_text="FontAwesome class"
    )

    # =========================
    # VALUES
    # =========================
    values_title = models.CharField(max_length=100, default="Values")
    values_text = models.TextField()

    values_icon = models.CharField(
        max_length=100,
        default="fa-solid fa-gem",
        help_text="FontAwesome class"
    )

    class Meta:
        verbose_name = "Vision Mission Values"
        verbose_name_plural = "Vision Mission Values"

    def __str__(self):
        return self.section_title
    
# =========================================================
# KEY STATS SECTION (PARENT / SINGLETON STYLE)
# =========================================================

class KeyStatsSection(models.Model):
    """
    CMS container for Key Stats section (About Page)
    Acts like Vision / Hero style singleton section
    """

    title = models.CharField(
        max_length=255,
        default="Numbers That Define Our Architectural Journey"
    )

    subtitle = models.TextField(
        blank=True,
        default="A reflection of our commitment to precision, innovation, and timeless architectural excellence."
    )

    tag = models.CharField(
        max_length=100,
        default="OUR IMPACT"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Key Stats Section"
        verbose_name_plural = "Key Stats Section"

    def __str__(self):
        return "Key Stats Section"


# =========================================================
# KEY STAT ITEMS (CHILD / INLINE CMS CARDS)
# =========================================================
class KeyStatItem(models.Model):
    """
    Individual stat card (child of KeyStatsSection)
    Example:
        120 + Projects Completed
    """

    section = models.ForeignKey(
        KeyStatsSection,
        on_delete=models.CASCADE,
        related_name="items"
    )

    label = models.CharField(
        max_length=150
    )

    value = models.PositiveIntegerField()

    suffix = models.CharField(
        max_length=10,
        blank=True,
        default="+"
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Key Stat Item"
        verbose_name_plural = "Key Stat Items"

    def __str__(self):
        return f"{self.label} ({self.value}{self.suffix})"
    
# =========================================================
# ASSOCIATED WITH SECTION SETTINGS (OPTIONAL CMS SAFE)
# =========================================================
class AssociatedWithSection(SingletonModel):
    """
    CMS-controlled section settings
    for the About Us -> Associated With section.
    """

    is_active = models.BooleanField(default=True)

    kicker = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default=""
    )

    heading = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default=""
    )

    description = models.TextField(
        blank=True,
        null=True,
        default=""
    )

    section_padding_top = models.PositiveIntegerField(default=110)

    section_padding_bottom = models.PositiveIntegerField(default=110)

    marquee_speed = models.PositiveIntegerField(default=22)

    class Meta:
        verbose_name = "Associated With Section"
        verbose_name_plural = "Associated With Section"

    def __str__(self):
        return "Associated With Section"

# =========================================================
# PARTNER LOGO MODEL (FULLY OPTIONAL SAFE)
# =========================================================
class AssociatedPartner(models.Model):
    """
    Individual partner / associated company logo.
    Fully CMS-flexible (no required fields).
    """

    section = models.ForeignKey(
        AssociatedWithSection,
        on_delete=models.CASCADE,
        related_name="partners",
        blank=True,
        null=True
    )

    name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        default=""
    )

    logo = models.ImageField(
        upload_to="about/associated_partners/",
        blank=True,
        null=True
    )

    website_url = models.URLField(
        blank=True,
        null=True
    )

    display_order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Associated Partner"
        verbose_name_plural = "Associated Partners"

    def __str__(self):
        return self.name or "Unnamed Partner"

# =========================================================
# OUR TEAM SECTION (CMS CONTROL)
# =========================================================
class OurTeamSection(models.Model):
    """
    Controls the entire Our Team section.
    Designed to be flexible and non-restrictive.
    """

    section_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default="Our Collective"
    )

    eyebrow = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default="The Studio"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Our Team Section"
        verbose_name_plural = "Our Team Sections"

    def __str__(self):
        return self.section_title or "Our Team Section"


# =========================================================
# TEAM MEMBER (FULLY OPTIONAL CMS CONTENT)
# =========================================================
class TeamMember(models.Model):
    """
    Repeatable team member block.
    Everything is optional except section relation.
    """

    section = models.ForeignKey(
        OurTeamSection,
        on_delete=models.CASCADE,
        related_name="members"
    )

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="about/team/",
        blank=True,
        null=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return self.name or "Unnamed Team Member"