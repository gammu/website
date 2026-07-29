from django.core.management.base import BaseCommand

from phonedb.charts import get_phone_records_chart


class Command(BaseCommand):
    help = "updates cached phone records summary chart"

    def handle(self, *args, **options):
        get_phone_records_chart(force=True)
