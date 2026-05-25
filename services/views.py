from django.shortcuts import render

from .models import (
    Service,
    ServicesHeroSection,
    WhyChooseSection,
    ServicesExtraSection,
)

# =========================================================
# SERVICES PAGE VIEW (FULL CMS DRIVEN)
# =========================================================
def services_page(request):

    # =====================================================
    # SERVICES
    # =====================================================
    services = (
        Service.objects
        .filter(is_active=True)
        .order_by("order", "id")
    )

    home_services = services.filter(
        show_on_home=True
    )

    # =====================================================
    # HERO SECTION
    # =====================================================
    hero = (
        ServicesHeroSection.objects
        .filter(is_active=True)
        .first()
    )

    hero_image = hero.hero_image if hero and hero.hero_image else None

    # =====================================================
    # WHY CHOOSE SECTION
    # =====================================================
    why_choose = (
        WhyChooseSection.objects
        .prefetch_related("features")
        .first()
    )

    why_choose_features = []

    if why_choose:
        why_choose_features = (
            why_choose.features
            .all()
            .order_by("id")
        )

    # =====================================================
    # SERVICES EXTRA SECTION
    # =====================================================
    extra_section = (
        ServicesExtraSection.objects
        .select_related(
            "spotlight",
            "cta",
        )
        .prefetch_related(
            "spotlight_items",
            "process_steps",
            "metrics",
            "faqs",
        )
        .first()
    )

    # =====================================================
    # DEFAULTS
    # =====================================================
    extra_spotlight = None
    extra_spotlight_items = []
    extra_process_steps = []
    extra_metrics = []
    extra_faqs = []
    extra_cta = None

    # =====================================================
    # RELATED DATA
    # =====================================================
    if extra_section:

        # ---------------- SPOTLIGHT ----------------
        try:
            extra_spotlight = extra_section.spotlight
        except Exception:
            extra_spotlight = None

        # ---------------- SPOTLIGHT ITEMS ----------------
        extra_spotlight_items = (
            extra_section.spotlight_items
            .all()
            .order_by("id")
        )

        # ---------------- PROCESS STEPS ----------------
        extra_process_steps = (
            extra_section.process_steps
            .all()
            .order_by("number", "id")
        )

        # ---------------- METRICS ----------------
        extra_metrics = (
            extra_section.metrics
            .all()
            .order_by("id")
        )

        # ---------------- FAQS ----------------
        extra_faqs = (
            extra_section.faqs
            .all()
            .order_by("id")
        )

        # ---------------- CTA ----------------
        try:
            extra_cta = extra_section.cta
        except Exception:
            extra_cta = None

    # =====================================================
    # CONTEXT
    # =====================================================
    context = {

        # SERVICES
        "services": services,
        "home_services": home_services,

        # HERO
        "hero": hero,
        "hero_image": hero_image,

        # WHY CHOOSE
        "why_choose": why_choose,
        "why_choose_features": why_choose_features,

        # EXTRA SECTION
        "extra_section": extra_section,

        # SPOTLIGHT
        "extra_spotlight": extra_spotlight,
        "extra_spotlight_items": extra_spotlight_items,

        # PROCESS
        "extra_process_steps": extra_process_steps,

        # METRICS
        "extra_metrics": extra_metrics,

        # FAQ
        "extra_faqs": extra_faqs,

        # CTA
        "extra_cta": extra_cta,
    }

    return render(
        request,
        "services/services.html",
        context
    )