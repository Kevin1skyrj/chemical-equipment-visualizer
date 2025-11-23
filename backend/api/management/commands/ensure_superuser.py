import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Ensure a specific superuser exists with the desired password."""

    help = "Create or update a superuser using env variables or CLI flags."

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Superuser username")
        parser.add_argument("--password", type=str, help="Superuser password")
        parser.add_argument("--email", type=str, help="Superuser email")

    def handle(self, *args, **options):
        username = options.get("username") or os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = options.get("password") or os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = options.get("email") or os.environ.get("DJANGO_SUPERUSER_EMAIL")

        if not username or not password or not email:
            self.stdout.write(self.style.WARNING("Missing credentials; skipping ensure_superuser."))
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )

        updated = False
        if user.email != email:
            user.email = email
            updated = True

        if not user.is_superuser or not user.is_staff:
            user.is_superuser = True
            user.is_staff = True
            updated = True

        if not user.check_password(password):
            user.set_password(password)
            updated = True

        if updated:
            user.save()

        status = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' {status} successfully."))
