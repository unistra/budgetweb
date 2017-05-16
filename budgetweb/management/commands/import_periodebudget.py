import csv

from django.core.management.base import BaseCommand

from budgetweb.models import Period, PeriodeBudget


class Command(BaseCommand):
    help = 'Import the Financial Plan from a csv file'

    def handle(self, *args, **options):
        initial_period = Period.objects.get(code='BI')
        created = PeriodeBudget.objects.update_or_create(
            period=initial_period,
            annee="2017",
            defaults={'is_active': True}
            )[1]
        print('PeriodeBudget created : %s' % (int(created)))
