from .models import (
    NavItem,
    SiteLogo,
    FooterSettings,
    NavbarSettings,
    HeroTypographySettings,
)


def global_context(request):
    # =====================================================
    # NAV ITEMS
    # =====================================================
    nav_items = (
        NavItem.objects
        .filter(is_active=True, type="link")
        .order_by("order", "id")
    )

    nav_cta_items = (
        NavItem.objects
        .filter(is_active=True, type="cta")
        .order_by("order", "id")
    )

    nav_cta = nav_cta_items.first()

    # =====================================================
    # GLOBAL SITE ELEMENTS
    # =====================================================
    logo = SiteLogo.objects.last()
    navbar_settings, _ = NavbarSettings.objects.get_or_create(pk=1)
    footer_settings, _ = FooterSettings.objects.get_or_create(pk=1)

    # =====================================================
    # FOOTER LINKS
    # =====================================================
    footer_projects_links = (
        footer_settings.project_links
        .filter(is_active=True)
        .order_by("order", "id")
    )

    footer_practice_links = (
        footer_settings.practice_links
        .filter(is_active=True)
        .order_by("order", "id")
    )

    footer_social_links = (
        footer_settings.social_links
        .filter(is_active=True)
        .order_by("order", "id")
    )

    # =====================================================
    # HERO TYPOGRAPHY
    # =====================================================
    hero_typography = {
        item.page_type: item
        for item in HeroTypographySettings.objects.filter(is_active=True)
    }

    return {
        # NAVBAR
        "nav_items": nav_items,
        "nav_cta": nav_cta,
        "nav_cta_items": nav_cta_items,
        "logo": logo,
        "navbar_settings": navbar_settings,

        # FOOTER
        "footer_settings": footer_settings,
        "footer_projects_links": footer_projects_links,
        "footer_practice_links": footer_practice_links,
        "footer_social_links": footer_social_links,

        # HERO TYPOGRAPHY
        "hero_typography": hero_typography,
    }