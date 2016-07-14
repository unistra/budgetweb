import csv

from django.core.management.base import BaseCommand

from budgetweb.models import PlanFinancement, Structure


class Command(BaseCommand):
    help = 'Import the Financial Plan from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

    def handle(self, *args, **options):
        for filename in options.get('filename'):
            with open(filename) as h:
                reader = csv.reader(h, delimiter=';', quotechar='"')
                total = 0
                for row in reader:
                    pfi_is_fleche = (row[3] == 'oui')
                    pluri = (row[4] == 'oui')
                    struct_code = row[0]

                    struct = Structure.objects.get(code=struct_code)
                    created = PlanFinancement.objects.update_or_create(
                        structure=struct,
                        code=row[1],
                        label=row[2],
                        eotp=row[5],
                        centrecoutderive=row[6],
                        centreprofitderive=row[7],
                        is_fleche=pfi_is_fleche,
                        is_pluriannuel=pluri,
                        defaults={'is_active': True}
                    )[1]
                    total += int(created)
                print('Financials Plans created with %s : %s' % (filename, total))
