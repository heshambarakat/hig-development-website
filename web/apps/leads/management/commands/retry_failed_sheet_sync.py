from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Alias for retry_failed_google_sheets_syncs."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        call_command("retry_failed_google_sheets_syncs", limit=options["limit"])
