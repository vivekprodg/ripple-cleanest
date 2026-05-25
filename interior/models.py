from django.db import models
from django.core.files.base import ContentFile
from django.utils.text import slugify

from core.utils.image_optimizer import optimize_uploaded_image


class InteriorHeroSection(models.Model):
    # ================= IMAGE =================
    background_image = models.ImageField(
        upload_to="interior/hero/",
        blank=True,
        null=True,
    )

    # ================= CONTENT =================
    eyebrow = models.CharField(
        max_length=120,
        blank=True,
        null=True,
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    subtitle = models.TextField(
        blank=True,
        null=True,
    )

    # ================= META =================
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Interior Hero Section"
        verbose_name_plural = "Interior Hero Sections"

    def __str__(self):
        return self.title if self.title else "Interior Hero (Empty)"


class InteriorPhilosophySection(models.Model):
    eyebrow = models.CharField(
        max_length=120,
        blank=True,
    )

    heading = models.CharField(
        max_length=255,
        blank=True,
    )

    paragraph_one = models.TextField(
        blank=True,
    )

    paragraph_two = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Interior Philosophy Section"
        verbose_name_plural = "Interior Philosophy Sections"

    def __str__(self):
        return self.heading or "Interior Philosophy Section"


class InteriorPhilosophyImage(models.Model):
    section = models.ForeignKey(
        InteriorPhilosophySection,
        on_delete=models.CASCADE,
        related_name="images",
        blank=True,
        null=True,
    )

    image = models.ImageField(
        upload_to="interior/philosophy/images/",
        blank=True,
        null=True,
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Interior Philosophy Image"
        verbose_name_plural = "Interior Philosophy Images"

    def __str__(self):
        return self.alt_text or f"Philosophy Image {self.id}"

    def save(self, *args, **kwargs):
        if self.image:
            try:
                optimized_image = optimize_uploaded_image(self.image)
                self.image.save(
                    optimized_image.name,
                    ContentFile(optimized_image.read()),
                    save=False,
                )
            except Exception:
                pass

        super().save(*args, **kwargs)


class InteriorPhilosophyPoint(models.Model):
    section = models.ForeignKey(
        InteriorPhilosophySection,
        on_delete=models.CASCADE,
        related_name="points",
        blank=True,
        null=True,
    )

    number = models.CharField(
        max_length=10,
        blank=True,
    )

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Interior Philosophy Point"
        verbose_name_plural = "Interior Philosophy Points"

    def __str__(self):
        return self.title or f"Point {self.id}"


class InteriorService(models.Model):
    icon = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Interior Service"
        verbose_name_plural = "Interior Services"

    def __str__(self):
        return self.title or "Unnamed Service"


class InteriorSelectedWork(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    main_image = models.ImageField(upload_to="interior/selected_work/main/", blank=True, null=True)
    side_image_1 = models.ImageField(upload_to="interior/selected_work/side/", blank=True, null=True)
    side_image_2 = models.ImageField(upload_to="interior/selected_work/side/", blank=True, null=True)

    main_title = models.CharField(max_length=255, blank=True, null=True)
    main_subtitle = models.CharField(max_length=255, blank=True, null=True)

    side_title_1 = models.CharField(max_length=255, blank=True, null=True)
    side_subtitle_1 = models.CharField(max_length=255, blank=True, null=True)

    side_title_2 = models.CharField(max_length=255, blank=True, null=True)
    side_subtitle_2 = models.CharField(max_length=255, blank=True, null=True)

    main_desc = models.TextField(blank=True, null=True)
    side_desc_1 = models.TextField(blank=True, null=True)
    side_desc_2 = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Interior Selected Work"
        verbose_name_plural = "Interior Selected Works"

    def __str__(self):
        return self.title or "Selected Work Entry"


class InteriorGalleryCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Interior Gallery Category"
        verbose_name_plural = "Interior Gallery Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while InteriorGalleryCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class InteriorGalleryItem(models.Model):
    # ================= BASIC INFO =================
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=220, blank=True, null=True, unique=True)

    # ================= CMS-DRIVEN CATEGORY =================
    gallery_category = models.ForeignKey(
    InteriorGalleryCategory,
    on_delete=models.SET_NULL,
    related_name="gallery_items",
    blank=True,
    null=True,
)

    # ================= MEDIA =================
    image = models.ImageField(upload_to="interior/gallery/", blank=True, null=True)

    # ================= CONTENT =================
    description = models.TextField(blank=True, null=True)

    # ================= META DATA =================
    location = models.CharField(max_length=200, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    client = models.CharField(max_length=200, blank=True, null=True)

    # ================= DISPLAY CONTROL =================
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    # ================= TIMESTAMPS =================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ================= SAVE OVERRIDE (AUTO SLUG) =================
    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while InteriorGalleryItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    # ================= STRING REPRESENTATION =================
    def __str__(self):
        return self.title or "Untitled Gallery Item"

    # ================= META =================
    class Meta:
        verbose_name = "Interior Gallery Item"
        verbose_name_plural = "Interior Gallery Items"
        ordering = ["order", "-created_at"]