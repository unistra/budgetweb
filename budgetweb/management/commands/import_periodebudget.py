import csv

from django.core.management.base import BaseCommand

from budgetweb.models import PeriodeBudget


class Command(BaseCommand):
    help = 'Import the Financial Plan from a csv file'

    def handle(self, *args, **options):
        PeriodeBudget.objects.update_or_create(
            code="BI",
            label="Budget initial",
            annee="2017",
            defaults={'is_active': True}
            )
        created = 1
        print('PeriodeBudget created : %s' % ( created, ))
