from .models import (
    NavItem,
    SiteLogo,
    FooterSettings,
    NavbarSettings,
    HeroTypographySettings,
    WhatsAppSettings,
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
    whatsapp_settings, _ = WhatsAppSettings.objects.get_or_create(pk=1)

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

        # WHATSAPP
        "whatsapp_settings": whatsapp_settings,
        "whatsapp_phone_number": whatsapp_settings.phone_number,
        "whatsapp_prefilled_text": whatsapp_settings.prefilled_text,
        "whatsapp_is_active": whatsapp_settings.is_active,

        # HERO TYPOGRAPHY
        "hero_typography": hero_typography,
    }