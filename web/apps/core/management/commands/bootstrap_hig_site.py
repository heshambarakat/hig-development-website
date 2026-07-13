from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Backward-compatible alias for seed_hig_content."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite editable seeded content.")

    def handle(self, *args, **options):
        call_command("seed_hig_content", force=options["force"])
