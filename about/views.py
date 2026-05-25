from django.shortcuts import render
from django.http import HttpResponse

from .models import (
    AboutPageSettings,
    AboutHeroSection,
    AboutOverviewSection,
    VisionMissionValues,
    KeyStatsSection,
    AssociatedWithSection,
    AssociatedPartner,
    OurTeamSection,
)

# =========================================
# ABOUT PAGE VIEW (CMS DRIVEN)
# =========================================
def about_page(request):

    # =====================================
    # LOAD SINGLETON CMS SECTIONS
    # =====================================
    page_settings = AboutPageSettings.load()
    hero = AboutHeroSection.load()
    overview = AboutOverviewSection.load()
    vision_mission_values = VisionMissionValues.objects.first()
    key_stats = KeyStatsSection.objects.prefetch_related("items").first()
    associated_with = AssociatedWithSection.load()

    # =====================================
    # LOAD OUR TEAM CMS SECTION
    # =====================================
    our_team = OurTeamSection.objects.prefetch_related("members").first()

    # =====================================
    # HERO DATA
    # =====================================
    hero_data = {
        "is_active": getattr(hero, "is_active", True),

        "eyebrow": getattr(hero, "eyebrow", ""),
        "title": getattr(hero, "title", ""),
        "description": getattr(hero, "description", ""),

        "background_image": getattr(hero, "background_image", None),

        "primary_button_text": getattr(
            hero,
            "primary_button_text",
            ""
        ),

        "primary_button_url": getattr(
            hero,
            "primary_button_url",
            "#"
        ),

        "secondary_button_text": getattr(
            hero,
            "secondary_button_text",
            ""
        ),

        "secondary_button_url": getattr(
            hero,
            "secondary_button_url",
            "#"
        ),
    }

    # =====================================
    # PAGE SETTINGS DATA
    # =====================================
    page_data = {
        "page_title": getattr(
            page_settings,
            "page_title",
            "About"
        ),

        "meta_description": getattr(
            page_settings,
            "meta_description",
            ""
        ),

        "is_active": getattr(
            page_settings,
            "is_active",
            True
        ),
    }

    # =====================================
    # OVERVIEW SECTION DATA
    # =====================================
    overview_data = {
        "is_active": getattr(
            overview,
            "is_active",
            True
        ),

        # ---------------------------------
        # CONTENT
        # ---------------------------------
        "subtitle": getattr(
            overview,
            "subtitle",
            ""
        ),

        "title": getattr(
            overview,
            "title",
            ""
        ),

        "description": getattr(
            overview,
            "description",
            ""
        ),

        # ---------------------------------
        # BUTTON
        # ---------------------------------
        "button_text": getattr(
            overview,
            "button_text",
            ""
        ),

        "button_link": getattr(
            overview,
            "button_link",
            "#"
        ),

        # ---------------------------------
        # IMAGES
        # ---------------------------------
        "main_image": getattr(
            overview,
            "main_image",
            None
        ),

        "secondary_image": getattr(
            overview,
            "secondary_image",
            None
        ),

        # ---------------------------------
        # IMAGE ALT TEXT
        # ---------------------------------
        "main_image_alt": getattr(
            overview,
            "main_image_alt",
            ""
        ),

        "secondary_image_alt": getattr(
            overview,
            "secondary_image_alt",
            ""
        ),
    }

    # =====================================
    # VISION / MISSION / VALUES DATA
    # =====================================
    vision_mission_values_data = None

    if vision_mission_values:
        vision_mission_values_data = {
            "is_active": getattr(vision_mission_values, "is_active", True),
            "section_title": getattr(
                vision_mission_values,
                "section_title",
                "Vision, Mission & Values"
            ),

            # VISION
            "vision_title": getattr(vision_mission_values, "vision_title", ""),
            "vision_text": getattr(vision_mission_values, "vision_text", ""),
            "vision_icon": getattr(vision_mission_values, "vision_icon", ""),

            # MISSION
            "mission_title": getattr(vision_mission_values, "mission_title", ""),
            "mission_text": getattr(vision_mission_values, "mission_text", ""),
            "mission_icon": getattr(vision_mission_values, "mission_icon", ""),

            # VALUES
            "values_title": getattr(vision_mission_values, "values_title", ""),
            "values_text": getattr(vision_mission_values, "values_text", ""),
            "values_icon": getattr(vision_mission_values, "values_icon", ""),
        }

    # =====================================
    # KEY STATS DATA
    # =====================================
    key_stats_data = None

    if key_stats:
        key_stats_data = key_stats

    # =====================================
    # OUR TEAM DATA
    # =====================================
    our_team_data = None

    if our_team:
        our_team_data = our_team

    # =====================================
    # ASSOCIATED WITH DATA
    # =====================================
    associated_with_data = {
        "is_active": getattr(associated_with, "is_active", True),
        "kicker": getattr(associated_with, "kicker", "We collaborate with"),
        "heading": getattr(associated_with, "heading", "We are associated with"),
        "description": getattr(
            associated_with,
            "description",
            "Trusted partners and global platforms that contribute to our design, technology, and execution excellence."
        ),
        "section_padding_top": getattr(associated_with, "section_padding_top", 110),
        "section_padding_bottom": getattr(associated_with, "section_padding_bottom", 110),
        "marquee_speed": getattr(associated_with, "marquee_speed", 22),
    }

    associated_partners = associated_with.partners.filter(is_active=True).order_by(
        "display_order",
        "id"
    )

    # =====================================
    # TEMPLATE CONTEXT
    # =====================================
    context = {
        "page": page_data,
        "hero": hero_data,
        "overview": overview_data,
        "vision_mission_values": vision_mission_values_data,
        "key_stats": key_stats_data,
        "our_team": our_team_data,
        "associated_with": associated_with_data,
        "associated_partners": associated_partners,
    }

    return render(
        request,
        "about/about.html",
        context
    )


# =========================================
# CMS / DASHBOARD ROUTES
# =========================================
def about_dashboard(request):
    return HttpResponse(
        "About CMS Dashboard (Coming Soon)"
    )


def about_hero_edit(request):
    return HttpResponse(
        "About Hero Edit Page (Coming Soon)"
    )


def about_hero_preview(request):
    return HttpResponse(
        "About Hero Preview (Coming Soon)"
    )


def about_page_preview(request):
    return HttpResponse(
        "About Page Preview (Coming Soon)"
    )