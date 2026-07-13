from django.core.management.base import BaseCommand

from apps.integrations.sheets import sync_lead_to_google_sheet
from apps.leads.models import Lead


class Command(BaseCommand):
    help = "Retry failed Google Sheets syncs for saved leads."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        limit = options["limit"]
        leads = Lead.objects.filter(google_sheet_status="sync_failed").order_by("created_at")[:limit]
        synced = 0
        failed = 0
        for lead in leads:
            if sync_lead_to_google_sheet(lead):
                synced += 1
            else:
                failed += 1
        self.stdout.write(self.style.SUCCESS(f"Retried {synced + failed} leads. Synced: {synced}. Failed: {failed}."))
