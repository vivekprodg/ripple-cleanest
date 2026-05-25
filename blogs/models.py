from django.db import models

from core.utils.image_optimizer import optimize_uploaded_image


class BlogHeaderSection(models.Model):
    eyebrow = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Small uppercase label above the main heading.",
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Main hero heading text.",
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Hero section description text.",
    )
    background_image = models.ImageField(
        upload_to="blogs/header/",
        blank=True,
        null=True,
        help_text="Hero background image for the blog header section.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Enable this header section on the blog page.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Header Section"
        verbose_name_plural = "Blog Header Sections"

    def __str__(self):
        return self.title or "Blog Header Section"


class BlogPageIntro(models.Model):
    volume_label = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Small volume label above the blog page intro heading.",
    )
    heading = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Main blog listing heading.",
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Intro description shown on the blog listing page.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Enable this intro section on the blog page.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Page Intro"
        verbose_name_plural = "Blog Page Intros"

    def __str__(self):
        return self.heading or "Blog Page Intro"


class BlogCategory(models.Model):
    name = models.CharField(
        max_length=120,
        blank=True,
        default="",
        help_text="Category name shown on blog posts.",
    )
    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
        null=True,
        help_text="URL-friendly category slug.",
    )

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name or "Blog Category"


class BlogAuthor(models.Model):
    name = models.CharField(
        max_length=150,
        blank=True,
        default="",
        help_text="Author name shown in the sidebar and post meta.",
    )
    designation = models.CharField(
        max_length=150,
        blank=True,
        default="",
        help_text="Author role or designation.",
    )
    bio = models.TextField(
        blank=True,
        default="",
        help_text="Short author bio.",
    )
    profile_image = models.ImageField(
        upload_to="blogs/authors/",
        blank=True,
        null=True,
        help_text="Author profile image.",
    )
    instagram_url = models.URLField(
        blank=True,
        default="",
        help_text="Instagram profile URL.",
    )
    linkedin_url = models.URLField(
        blank=True,
        default="",
        help_text="LinkedIn profile URL.",
    )
    twitter_url = models.URLField(
        blank=True,
        default="",
        help_text="Twitter/X profile URL.",
    )

    class Meta:
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"
        ordering = ["name"]

    def __str__(self):
        return self.name or "Blog Author"


class BlogTag(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Tag name shown in the post sidebar.",
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        null=True,
        help_text="URL-friendly tag slug.",
    )

    class Meta:
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name or "Blog Tag"


class BlogPost(models.Model):
    title = models.CharField(
        max_length=250,
        blank=True,
        default="",
        help_text="Blog post title.",
    )
    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True,
        null=True,
        help_text="URL-friendly blog post slug.",
    )
    excerpt = models.TextField(
        blank=True,
        default="",
        help_text="Short summary shown in listing cards and featured post.",
    )
    content = models.TextField(
        blank=True,
        default="",
        help_text="Full blog post content.",
    )
    featured_image = models.ImageField(
        upload_to="blogs/posts/",
        blank=True,
        null=True,
        help_text="Main featured image for the post.",
    )
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        help_text="Post category.",
    )
    author = models.ForeignKey(
        BlogAuthor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        help_text="Post author.",
    )
    tags = models.ManyToManyField(
        BlogTag,
        blank=True,
        related_name="posts",
        help_text="Tags for this post.",
    )
    read_time = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Read time label such as '8 Min Read'.",
    )
    published_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date shown in the listing and detail pages.",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Marks this post as the featured post on the blog listing page.",
    )
    show_on_homepage = models.BooleanField(
        default=False,
        help_text="If enabled, this post will appear in the homepage blog section.",
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Show this post on the blog page.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ["-published_date", "-created_at"]

    def save(self, *args, **kwargs):
        if self.featured_image:
            self.featured_image = optimize_uploaded_image(self.featured_image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or "Blog Post"