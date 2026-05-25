from django.shortcuts import render

from .models import (
    InteriorHeroSection,
    InteriorPhilosophySection,
    InteriorService,
    InteriorSelectedWork,
    InteriorGalleryCategory,
    InteriorGalleryItem,
)


def interior_page(request):

    # ================= HERO SECTION =================
    hero = (
        InteriorHeroSection.objects
        .filter(is_active=True)
        .order_by("-updated_at")
        .first()
    )

    # ================= PHILOSOPHY SECTION =================
    philosophy = (
        InteriorPhilosophySection.objects
        .filter(is_active=True)
        .prefetch_related(
            "images",
            "points",
        )
        .order_by("-updated_at")
        .first()
    )

    # ================= PHILOSOPHY IMAGES =================
    philosophy_images = []

    if philosophy:
        philosophy_images = (
            philosophy.images
            .filter(is_active=True)
            .order_by("display_order", "id")
        )

    # ================= PHILOSOPHY POINTS =================
    philosophy_points = []

    if philosophy:
        philosophy_points = (
            philosophy.points
            .filter(is_active=True)
            .order_by("display_order", "id")
        )

    # ================= SERVICES SECTION =================
    services = (
        InteriorService.objects
        .filter(is_active=True)
        .order_by("order", "id")
    )

    # ================= SELECTED WORK =================
    selected_work = (
        InteriorSelectedWork.objects
        .order_by("-updated_at", "-created_at")
        .first()
    )

    # ================= GALLERY SECTION =================
    gallery_categories = (
        InteriorGalleryCategory.objects
        .filter(is_active=True)
        .order_by("order", "name")
    )

    gallery_items = (
        InteriorGalleryItem.objects
        .filter(is_active=True)
        .select_related("gallery_category")
        .order_by("order", "-created_at")
    )

    # ================= CONTEXT =================
    context = {
        "hero": hero,
        "philosophy": philosophy,
        "philosophy_images": philosophy_images,
        "philosophy_points": philosophy_points,
        "services": services,
        "selected_work": selected_work,
        "gallery_categories": gallery_categories,
        "gallery_items": gallery_items,
    }

    return render(
        request,
        "interior/interior.html",
        context,
    )