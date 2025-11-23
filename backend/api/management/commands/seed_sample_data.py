from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from api.services import create_dataset_from_file


class Command(BaseCommand):
    help = "Seed the database with the provided sample CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            help="Optional path to a CSV file. Defaults to the repository sample.",
        )
        parser.add_argument(
            "--username",
            type=str,
            help="Existing Django username that will own the seeded dataset. Defaults to the first superuser.",
        )

    def handle(self, *args, **options):
        csv_path = options.get("path")
        if csv_path:
            path = Path(csv_path)
        else:
            path = Path(settings.BASE_DIR).parent / "sample_equipment_data.csv"

        if not path.exists():
            raise CommandError(f"CSV file not found at {path}")

        username = options.get("username")
        User = get_user_model()
        owner = None
        if username:
            owner = User.objects.filter(username=username).first()
        else:
            owner = User.objects.filter(is_superuser=True).order_by("id").first()

        if not owner:
            raise CommandError(
                "No suitable user found. Create a superuser or specify --username before seeding."
            )

        with path.open("rb") as file_obj:
            dataset = create_dataset_from_file(
                file_obj=file_obj,
                owner=owner,
                name="Sample Equipment Data",
            )

        self.stdout.write(self.style.SUCCESS(f"Seeded dataset '{dataset.name}'"))
