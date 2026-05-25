from django.shortcuts import render, get_object_or_404

from .models import (
    BlogHeaderSection,
    BlogPageIntro,
    BlogPost,
)

# -----------------------------
# BLOG LISTING PAGE (CMS DRIVEN)
# -----------------------------
def blog_page(request):
    blog_header = (
        BlogHeaderSection.objects.filter(is_active=True)
        .order_by("-updated_at")
        .first()
    )

    blog_intro = (
        BlogPageIntro.objects.filter(is_active=True)
        .order_by("-updated_at")
        .first()
    )

    featured_post = (
        BlogPost.objects.filter(
            is_featured=True,
            is_published=True
        )
        .select_related("category", "author")
        .prefetch_related("tags")
        .first()
    )

    blog_posts = (
        BlogPost.objects.filter(is_published=True)
        .select_related("category", "author")
        .prefetch_related("tags")
        .order_by("-published_date", "-created_at")
    )

    if featured_post:
        blog_posts = blog_posts.exclude(id=featured_post.id)

    return render(
        request,
        "blogs/blog_page.html",
        {
            "blog_header": blog_header,
            "blog_intro": blog_intro,
            "featured_post": featured_post,
            "blog_posts": blog_posts,
        },
    )


# -----------------------------
# BLOG DETAIL PAGE (CMS DRIVEN)
# -----------------------------
def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost.objects.select_related(
            "category",
            "author"
        ).prefetch_related("tags"),
        slug=slug,
        is_published=True,
    )

    # --------------------------------
    # HERO SECTION DATA (FIX)
    # REQUIRED FOR blog_header.html
    # --------------------------------
    blog_header = (
        BlogHeaderSection.objects.filter(is_active=True)
        .order_by("-updated_at")
        .first()
    )

    blog_intro = (
        BlogPageIntro.objects.filter(is_active=True)
        .order_by("-updated_at")
        .first()
    )

    related_posts = (
        BlogPost.objects.filter(
            is_published=True,
            category=post.category,
        )
        .exclude(id=post.id)
        .select_related("category", "author")
        .prefetch_related("tags")
        .order_by("-published_date")[:3]
    )

    previous_post = (
        BlogPost.objects.filter(
            is_published=True,
            published_date__lt=post.published_date,
        )
        .order_by("-published_date")
        .first()
    )

    next_post = (
        BlogPost.objects.filter(
            is_published=True,
            published_date__gt=post.published_date,
        )
        .order_by("published_date")
        .first()
    )

    return render(
        request,
        "blogs/blog_detail.html",
        {
            # BLOG DETAIL DATA
            "blog": post,
            "post": post,

            # HERO SECTION DATA (FIX)
            "blog_header": blog_header,
            "blog_intro": blog_intro,

            # EXTRA DATA
            "related_posts": related_posts,
            "previous_post": previous_post,
            "next_post": next_post,
        },
    )