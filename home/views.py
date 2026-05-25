from django.shortcuts import render

from .models import (
    HomePageSettings,
    RippleDifferenceSection,
    TeamSectionSettings,
    TeamMember,
    MaterialStackSection,
    ClientTestimonial,   # ✅ ADDED
)

from services.models import Service
from blogs.models import BlogPost


# =========================================================
# HOME PAGE VIEW (FULL CMS DRIVEN)
# =========================================================
def home_view(request):
    """
    Homepage view:
    - Hero CMS
    - Material Stack CMS
    - Ripple Difference CMS
    - Services CMS
    - Team CMS
    - Client Testimonials CMS (NEW)
    - Blog Journal
    """

    # ---------------------------
    # HERO / GLOBAL SETTINGS
    # ---------------------------
    homepage = HomePageSettings.objects.first()

    if homepage is None:
        homepage = HomePageSettings.objects.create()

    # ---------------------------
    # RIPPLE DIFFERENCE SECTION
    # ---------------------------
    ripple_difference = RippleDifferenceSection.objects.first()

    # ---------------------------
    # TEAM SECTION
    # ---------------------------
    team_section = (
        TeamSectionSettings.objects
        .prefetch_related("members")
        .filter(is_active=True)
        .first()
    )

    team_members = []

    if team_section:
        team_members = (
            team_section.members
            .filter(is_active=True)
            .order_by("display_order", "id")
        )

    # ---------------------------
    # SERVICES
    # ---------------------------
    services = (
        Service.objects
        .filter(is_active=True)
        .order_by("order", "id")
    )

    home_services = (
        Service.objects
        .filter(
            is_active=True,
            show_on_home=True
        )
        .order_by("order", "id")
    )

    # =========================================================
    # MATERIAL STACK CMS
    # =========================================================
    material_stack = (
        MaterialStackSection.objects
        .prefetch_related("cards")
        .first()
    )

    material_cards = []

    if material_stack:
        material_cards = (
            material_stack.cards
            .filter(is_active=True)
            .order_by("order", "id")
        )

    # =========================================================
    # 🟢 CLIENT TESTIMONIALS CMS (NEW)
    # =========================================================
    testimonials = (
        ClientTestimonial.objects
        .filter(is_active=True)
        .order_by("order", "created_at")
    )

    # ---------------------------
    # BLOGS (JOURNAL SECTION)
    # ---------------------------
    homepage_blogs = (
        BlogPost.objects.filter(
            is_published=True,
            show_on_homepage=True
        )
        .select_related("category", "author")
        .order_by("-published_date", "-created_at")[:3]
    )

    # ---------------------------
    # CONTEXT
    # ---------------------------
    context = {
        # Global CMS
        "page": homepage,
        "homepage": homepage,
        "home_settings": homepage,

        # Ripple Difference
        "ripple_difference": ripple_difference,

        # Services
        "services": services,
        "home_services": home_services,

        # Team
        "team_section": team_section,
        "team_members": team_members,

        # Material Stack
        "material_stack": material_stack,
        "material_cards": material_cards,

        # 🟢 Testimonials (NEW CMS PIPELINE)
        "testimonials": testimonials,

        # Blogs
        "homepage_blogs": homepage_blogs,
    }

    return render(
        request,
        "home/home.html",
        context
    )


# =========================================================
# SERVICES PAGE
# =========================================================
def services_page(request):

    services = (
        Service.objects
        .filter(is_active=True)
        .order_by("order", "id")
    )

    home_services = services.filter(
        show_on_home=True
    )

    context = {
        "services": services,
        "home_services": home_services,
    }

    return render(
        request,
        "services/services.html",
        context
    )