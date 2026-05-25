from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

from core.utils.image_optimizer import optimize_uploaded_image

# =========================================================
# PROJECT HERO SECTION (CMS)
# =========================================================
class ProjectHeroSection(models.Model):

    # ================= CONTENT =================
    title = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        default="",
        help_text="Main hero heading displayed on the Projects page."
    )

    description = models.TextField(
        blank=True,
        null=True,
        default="",
        help_text="Short descriptive paragraph below the hero title."
    )

    # ================= MEDIA =================
    background_image = models.ImageField(
        upload_to="projects/hero/",
        blank=True,
        null=True,
        help_text="Background image for the Projects hero section."
    )

    # ================= VISUAL SETTINGS =================
    overlay_opacity = models.FloatField(
        blank=True,
        null=True,
        default=0.58,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0)
        ],
        help_text=(
            "Controls dark overlay opacity. "
            "Use values between 0.0 and 1.0."
        )
    )

    # ================= STATE =================
    is_active = models.BooleanField(
        default=True,
        blank=True,
        help_text="Enable or disable the Projects hero section."
    )

    # ================= TIMESTAMPS =================
    updated_at = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =========================================================
    # MODEL META
    # =========================================================
    class Meta:
        verbose_name = "Project Hero Section"
        verbose_name_plural = "Project Hero Section"

    # =========================================================
    # STRING REPRESENTATION
    # =========================================================
    def __str__(self):

        if self.title:
            return self.title

        return "Project Hero Section"

    # =========================================================
    # SINGLETON ENFORCEMENT
    # =========================================================
    def save(self, *args, **kwargs):

        if not self.pk and ProjectHeroSection.objects.exists():

            existing = ProjectHeroSection.objects.first()

            self.pk = existing.pk

        super().save(*args, **kwargs)

        if self.background_image:
            optimize_uploaded_image(self.background_image)

# =========================================================
# PROJECT STATUS
# =========================================================
class ProjectStatus(models.Model):

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Project Status"
        verbose_name_plural = "Project Status"

    def __str__(self):

        if self.name:
            return self.name

        return "Project Status"

    def save(self, *args, **kwargs):

        if self.name and not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

# =========================================================
# PROJECT CATEGORY
# =========================================================
class ProjectCategory(models.Model):

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    def __str__(self):

        if self.name:
            return self.name

        return "Project Category"

    def save(self, *args, **kwargs):

        if self.name and not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

# =========================================================
# PROJECT SUBCATEGORY
# =========================================================
class ProjectSubCategory(models.Model):

    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="subcategories"
    )

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    slug = models.SlugField(
        blank=True,
        null=True,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Project Subcategory"
        verbose_name_plural = "Project Subcategories"

    def __str__(self):

        if self.name:
            return self.name

        return "Project Subcategory"

    def save(self, *args, **kwargs):

        if self.name and not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

# =========================================================
# PROJECT
# =========================================================
class Project(models.Model):

    # ================= BASIC INFO =================

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )

    client = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    date = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # ================= RELATIONS =================
    status = models.ForeignKey(
        ProjectStatus,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="projects"
    )

    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="projects"
    )

    subcategory = models.ForeignKey(
        ProjectSubCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="projects"
    )

    # ================= CONTENT =================
    description = models.TextField(
        blank=True,
        null=True
    )

    # ================= MEDIA =================
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True
    )

    # ================= SETTINGS =================
    is_active = models.BooleanField(
        default=True,
        blank=True
    )

    # ================= TIMESTAMPS =================
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):

        if self.title:
            return self.title

        return "Untitled Project"

    def save(self, *args, **kwargs):

        if self.title and not self.slug:
            base_slug = slugify(self.title)
            slug_value = base_slug
            counter = 1

            while Project.objects.filter(slug=slug_value).exclude(pk=self.pk).exists():
                slug_value = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug_value

        super().save(*args, **kwargs)

        if self.image:
            optimize_uploaded_image(self.image)

# =========================================================
# PROJECT GALLERY
# =========================================================
class ProjectGallery(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="gallery_images"
    )

    image = models.ImageField(
        upload_to="projects/gallery/",
        blank=True,
        null=True
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    display_order = models.PositiveIntegerField(
        default=0,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Project Gallery Image"
        verbose_name_plural = "Project Gallery Images"

    def __str__(self):

        if self.project and self.title:
            return f"{self.project.title} - {self.title}"

        if self.project:
            return f"{self.project.title} Gallery"

        return "Project Gallery Image"

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.image:
            optimize_uploaded_image(self.image)