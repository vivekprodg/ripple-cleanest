from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from core.utils.image_optimizer import optimize_uploaded_image


class HomePageSettings(models.Model):
    hero_aria_label = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="Premium architecture homepage banner",
    )

    hero_background_image = models.ImageField(
        upload_to="home/hero/",
        blank=True,
        null=True,
        help_text="Main desktop hero background image.",
    )

    hero_mobile_image = models.ImageField(
        upload_to="home/hero/mobile/",
        blank=True,
        null=True,
        help_text="Optional separate mobile hero image.",
    )

    hero_background_alt = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="Homepage hero background image",
    )

    hero_heading = models.TextField(
        blank=True,
        null=True,
        default="Designing spaces\nthat feel timeless\nand profoundly modern.",
        help_text="Use line breaks to control the heading layout.",
    )

    hero_subheading = models.TextField(
        blank=True,
        null=True,
        default="A premium architecture studio shaping residential, commercial, and cultural environments with clarity, precision, and quiet confidence.",
    )

    hero_primary_cta_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Explore Projects",
    )

    hero_primary_cta_link = models.URLField(
        blank=True,
        null=True,
        default="",
    )

    hero_secondary_cta_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Book a Consultation",
    )

    hero_secondary_cta_link = models.URLField(
        blank=True,
        null=True,
        default="",
    )

    hero_stat_1_value = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="120+",
    )

    hero_stat_1_label = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Completed works",
    )

    hero_stat_2_value = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="18",
    )

    hero_stat_2_label = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Years of practice",
    )

    hero_stat_3_value = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="9",
    )

    hero_stat_3_label = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Global awards",
    )

    featured_project_label = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Featured Project",
    )

    featured_project_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default="Harbor House",
    )

    featured_project_description = models.TextField(
        blank=True,
        null=True,
        default="A refined waterfront residence defined by warm materials, strong geometry, and soft daylight.",
    )

    featured_project_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Residential",
    )

    featured_project_location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Singapore",
    )

    featured_project_status = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Completed",
    )

    featured_project_image_1 = models.ImageField(
        upload_to="home/featured/",
        blank=True,
        null=True,
        help_text="First featured project preview image.",
    )

    featured_project_image_1_alt = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="Minimal luxury interior with soft natural light",
    )

    featured_project_image_1_caption = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Interior calm",
    )

    featured_project_image_2 = models.ImageField(
        upload_to="home/featured/",
        blank=True,
        null=True,
        help_text="Second featured project preview image.",
    )

    featured_project_image_2_alt = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="Modern architectural building facade",
    )

    featured_project_image_2_caption = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Facade rhythm",
    )

    featured_project_image_3 = models.ImageField(
        upload_to="home/featured/",
        blank=True,
        null=True,
        help_text="Third featured project preview image.",
    )

    featured_project_image_3_alt = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="Contemporary architecture with sharp lines",
    )

    featured_project_image_3_caption = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Structural clarity",
    )

    testimonials_eyebrow = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        default="Endorsements of Purity",
    )

    testimonials_heading = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="The Chronicles",
    )

    overlay_color = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="rgba(9, 10, 12, 0.45)",
    )

    overlay_deep_color = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="rgba(9, 10, 12, 0.66)",
    )

    text_color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="#ffffff",
    )

    muted_color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default="rgba(255, 255, 255, 0.78)",
    )

    border_color = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="rgba(255, 255, 255, 0.12)",
    )

    card_bg_color = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="rgba(255, 255, 255, 0.06)",
    )

    card_bg_strong_color = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="rgba(255, 255, 255, 0.10)",
    )

    class Meta:
        verbose_name = "Home Page Settings"
        verbose_name_plural = "Home Page Settings"

    def __str__(self):
        return "Home Page Settings"


class RippleDifferenceSection(models.Model):
    subtitle = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        default="The Ripple Difference",
    )

    heading = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="Elevating standards through visionary design.",
    )

    description = models.TextField(
        blank=True,
        null=True,
        default="We don't just build structures; we curate experiences. Our studio combines rigorous technical expertise with a profound understanding of spatial psychology.",
    )

    feature_one_title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        default="Precision Engineering",
    )

    feature_one_description = models.TextField(
        blank=True,
        null=True,
        default="Every angle, joint, and material transition is calculated with obsessive attention to detail, ensuring flawless execution.",
    )

    feature_two_title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        default="Sustainable Integration",
    )

    feature_two_description = models.TextField(
        blank=True,
        null=True,
        default="We integrate passive cooling, natural lighting, and ethical materials to minimize environmental impact without sacrificing luxury.",
    )

    main_image = models.ImageField(
        upload_to="home/ripple_difference/",
        blank=True,
        null=True,
    )

    secondary_image = models.ImageField(
        upload_to="home/ripple_difference/",
        blank=True,
        null=True,
    )

    button_text = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        default="Learn More About Us",
    )

    button_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="/about/",
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Ripple Difference Section"
        verbose_name_plural = "Ripple Difference Section"

    def __str__(self):
        return "Ripple Difference Section"

    def save(self, *args, **kwargs):
        if self.main_image:
            self.main_image = optimize_uploaded_image(self.main_image)

        if self.secondary_image:
            self.secondary_image = optimize_uploaded_image(self.secondary_image)

        super().save(*args, **kwargs)

    def image_preview(self):
        if self.main_image:
            return mark_safe(
                f'<img src="{self.main_image.url}" style="width:120px;border-radius:8px;" />'
            )
        return "No Image"

    image_preview.short_description = "Preview"


class MaterialStackSection(models.Model):
    eyebrow = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        default=""
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=""
    )

    is_active = models.BooleanField(
        default=True,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Material Stack Section"
        verbose_name_plural = "Material Stack Section"

    def __str__(self):
        return self.title or "Material Stack Section"


class MaterialStackCard(models.Model):
    section = models.ForeignKey(
        MaterialStackSection,
        related_name="cards",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    meta_num = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default=""
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=""
    )

    description = models.TextField(
        blank=True,
        null=True,
        default=""
    )

    image = models.ImageField(
        upload_to="home/material_stack/",
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Material Stack Card"
        verbose_name_plural = "Material Stack Cards"

    def __str__(self):
        return self.title or "Material Stack Card"


class TeamSectionSettings(models.Model):
    eyebrow = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="The Studio",
    )

    heading = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default="Our Collective",
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Team Section Settings"
        verbose_name_plural = "Team Section Settings"

    def __str__(self):
        return self.heading or "Team Section Settings"


class TeamMember(models.Model):
    section = models.ForeignKey(
        TeamSectionSettings,
        on_delete=models.CASCADE,
        related_name="members",
        blank=True,
        null=True,
    )

    full_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    designation = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to="home/team/",
        blank=True,
        null=True,
    )

    alt_text = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return self.full_name or "Team Member"

    def save(self, *args, **kwargs):
        if self.image:
            self.image = optimize_uploaded_image(self.image)

        super().save(*args, **kwargs)


class ClientTestimonial(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    designation = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    company = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True
    )

    quote = models.TextField(
        blank=True,
        null=True
    )

    order = models.IntegerField(
        default=0,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name if self.name else f"Testimonial {self.id}"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1

            while ClientTestimonial.objects.filter(
                slug=unique_slug
            ).exclude(id=self.id).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Client Testimonial"
        verbose_name_plural = "Client Testimonials"