import csv

from django.core.management.base import BaseCommand

from budgetweb.models import PlanFinancement, Structure


class Command(BaseCommand):
    help = 'Import the Financial Plan from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

    def handle(self, *args, **options):
        struct_probleme = []
        for filename in options.get('filename'):
            with open(filename) as h:
                reader = csv.reader(h, delimiter=';', quotechar='"')
                total = 0
                for row in reader:
                    pfi_is_fleche = (row[3] == 'oui' or  row[3] == 'Oui')
                    pluri = (row[4] == 'oui' or row[4] == 'Oui')
                    struct_code = row[0]
                    try:
                        struct = Structure.objects.get(code=struct_code)
                        created = PlanFinancement.objects.update_or_create(
                            structure=struct,
                            code=row[1],
                            label=row[2],
                            eotp=row[5],
                            centrecoutderive=row[6],
                            centreprofitderive=row[7],
                            groupe1=row[8],
                            groupe2=row[9],
                            is_fleche=pfi_is_fleche,
                            is_pluriannuel=pluri,
                            defaults={'is_active': True}
                        )[1]
                        total += int(created)
                    except Structure.DoesNotExist:
                        struct_probleme.append(struct_code)
                        pass
                print('Financials Plans created with %s : %s\n\tMissing: %s' %
                      (filename, total, ', '.join(struct_probleme)))
