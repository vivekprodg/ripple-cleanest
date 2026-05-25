from django.shortcuts import render

from .models import (
    ProjectHeroSection,
    Project,
    ProjectCategory,
    ProjectStatus,
)

# =========================================================
# PROJECTS PAGE
# =========================================================
def projects_page(request):

    # =====================================================
    # HERO SECTION
    # =====================================================
    hero_section = (
        ProjectHeroSection.objects
        .filter(is_active=True)
        .first()
    )

    # =====================================================
    # PROJECTS
    # =====================================================
    projects = (
        Project.objects
        .filter(is_active=True)
        .select_related(
            "status",
            "category",
            "subcategory",
        )
        .prefetch_related(
            "gallery_images",
        )
        .all()
    )

    # =====================================================
    # CATEGORIES
    # =====================================================
    categories = (
        ProjectCategory.objects
        .all()
    )

    # =====================================================
    # STATUSES
    # =====================================================
    statuses = (
        ProjectStatus.objects
        .all()
    )

    # =====================================================
    # CONTEXT
    # =====================================================
    context = {

        # HERO
        "project_hero": hero_section,

        # PROJECTS
        "projects": projects,

        # FILTERS
        "categories": categories,
        "statuses": statuses,
    }

    # =====================================================
    # RENDER
    # =====================================================
    return render(
        request,
        "projects/projects.html",
        context
    )