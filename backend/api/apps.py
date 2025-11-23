import logging

from django.apps import AppConfig
from django.core.management import call_command


logger = logging.getLogger(__name__)


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        super().ready()
        self._ensure_superuser()

    @staticmethod
    def _ensure_superuser():
        """Ensure the reviewer superuser exists each time the app boots."""
        try:
            call_command("ensure_superuser")
        except Exception as exc:  # pragma: no cover - best-effort bootstrap
            logger.warning("Skipping ensure_superuser bootstrap: %s", exc)
