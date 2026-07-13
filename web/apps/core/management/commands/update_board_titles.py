from django.core.management.base import BaseCommand
from wagtail.models import Page


class Command(BaseCommand):
    help = "Update current Wagtail board-member titles without changing other content."

    def handle(self, *args, **options):
        updated = 0
        for base_page in Page.objects.all():
            page = base_page.specific
            if not hasattr(page, "body"):
                continue
            body_data = list(page.body.raw_data)
            changed = False
            for block in body_data:
                if block.get("type") != "board_members":
                    continue
                for member in block["value"].get("members", []):
                    if member.get("name_en") == "Eng. Ahmed Ashour":
                        member["title_ar"] = "الرئيس التنفيذي"
                        member["title_en"] = "Chief Executive Officer"
                        changed = True
                    elif member.get("name_en") == "Eng. Islam Senousi":
                        member["title_ar"] = "عضو مجلس الإدارة"
                        member["title_en"] = "Board Member"
                        changed = True
            if changed:
                page.body = body_data
                page.save_revision().publish()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"Updated: {page.title}"))
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} page(s)."))
