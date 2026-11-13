from django.core.management.base import BaseCommand, CommandError

from local_pages.models import Page
from local_pages.publishing import PublishError, refresh


class Command(BaseCommand):
    help = "Check published Pages for updates and publish new revisions."

    def handle(self, *args, **options):
        failed = 0
        for page in Page.objects.order_by("pk").iterator():
            try:
                updated = refresh(page)
            except PublishError as exc:
                failed += 1
                self.stderr.write(f"{page.slug}: {exc}")
            else:
                status = f"published {page.revision[:8]}" if updated else "already current"
                self.stdout.write(f"{page.slug}: {status}")
        if failed:
            raise CommandError(f"{failed} Page(s) could not be refreshed.")
