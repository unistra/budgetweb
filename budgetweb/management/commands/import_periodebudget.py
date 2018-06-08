from datetime import date

from django.core.management.base import BaseCommand

from budgetweb.models import Period, PeriodeBudget


class Command(BaseCommand):
    help = 'Import the Financial Plan from a csv file'

    def handle(self, *args, **options):
        # Current school year
        today = date.today()
        year = today.year
        current_year = year + 1 if today.month >= 9 else year

        initial_period = Period.objects.get(code='BI')
        created = PeriodeBudget.objects.update_or_create(
            period=initial_period,
            annee=current_year,
            defaults={'is_active': True}
        )[1]
        print('PeriodeBudget created : %s' % (int(created)))
