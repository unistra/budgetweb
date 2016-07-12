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
                created = 0
                for row in reader:
                    if row[3]=='oui':
                        pfi_is_fleche = True
                    else:
                        pfi_is_fleche = False
                    if row[4]=='oui':
                        pluri = True
                    else:
                        pluri = False
                    struct_code = row[0]
                    print("#"+struct_code+"#")
                    struct = Structure.objects.filter(code=struct_code)
                    print(struct)
                    PlanFinancement.objects.update_or_create(
                        structure=struct, code=row[1],
                        label=row[2], eotp=row[5],centrecoutderive=row[6],
                        centreprofitderive=row[7],
                        is_fleche=pfi_is_fleche,
                        is_pluriannuel=pluri,
                        defaults={'is_active': True}
                    )
                    created += 1
                print('Financials Plans created with %s : %s' % (filename, created, ))
