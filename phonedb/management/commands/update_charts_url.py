from django.core.management.base import BaseCommand

from phonedb.views import get_chart_url


class Command(BaseCommand):
    help = "updates chart URL"  # noqa: A003

    def handle(self, *args, **options):
        get_chart_url(force=True)
