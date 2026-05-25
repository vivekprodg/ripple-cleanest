from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"
    verbose_name = "Homepage"

    def ready(self):
        """
        App initialization hook.

        Used for:
        - Initializing utilities like image optimization
        """

        try:
            from core.utils.image_optimizer import initialize_image_optimizer
            initialize_image_optimizer()
        except Exception:
            # Prevent startup crash if optimizer fails
            pass