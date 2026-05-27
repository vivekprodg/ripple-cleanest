from django.urls import path

from . import views

app_name = "lead"

urlpatterns = [
    # =========================================================
    # LEAD DASHBOARD / LIST
    # =========================================================
    path(
        "",
        views.lead_list,
        name="lead_list",
    ),

    # =========================================================
    # LEAD DETAIL
    # =========================================================
    path(
        "<int:pk>/",
        views.lead_detail,
        name="lead_detail",
    ),

    # =========================================================
    # CREATE / UPDATE
    # =========================================================
    path(
        "create/",
        views.lead_create,
        name="lead_create",
    ),

    path(
        "<int:pk>/update/",
        views.lead_update,
        name="lead_update",
    ),

    # =========================================================
    # FOOTER SUBSCRIPTION
    # =========================================================
    path(
        "subscription/create/",
        views.subscription_create,
        name="subscription_create",
    ),

    # =========================================================
    # STATUS / PRIORITY / SOURCE
    # =========================================================
    path(
        "<int:pk>/set-status/",
        views.lead_set_status,
        name="lead_set_status",
    ),

    path(
        "<int:pk>/set-priority/",
        views.lead_set_priority,
        name="lead_set_priority",
    ),

    path(
        "<int:pk>/set-source/",
        views.lead_set_source,
        name="lead_set_source",
    ),

    # =========================================================
    # NOTES / TAGS
    # =========================================================
    path(
        "<int:pk>/update-notes/",
        views.lead_update_notes,
        name="lead_update_notes",
    ),

    path(
        "<int:pk>/update-tags/",
        views.lead_update_tags,
        name="lead_update_tags",
    ),

    # =========================================================
    # ARCHIVE / DELETE
    # =========================================================
    path(
        "<int:pk>/archive/",
        views.lead_archive,
        name="lead_archive",
    ),

    path(
        "<int:pk>/unarchive/",
        views.lead_unarchive,
        name="lead_unarchive",
    ),

    path(
        "<int:pk>/delete/",
        views.lead_delete,
        name="lead_delete",
    ),

    path(
        "<int:pk>/restore/",
        views.lead_restore,
        name="lead_restore",
    ),

    # =========================================================
    # API ENDPOINTS
    # =========================================================
    path(
        "api/stats/",
        views.lead_stats_api,
        name="lead_stats_api",
    ),

    path(
        "api/board/",
        views.lead_board_api,
        name="lead_board_api",
    ),
]