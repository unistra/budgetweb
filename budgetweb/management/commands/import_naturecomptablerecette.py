import csv

from django.core.management.base import BaseCommand

from budgetweb.models import NatureComptableRecette


class Command(BaseCommand):
    help = 'Import the NatureComptableRecette from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

    def handle(self, *args, **options):
        for filename in options.get('filename'):
            with open(filename) as h:
                reader = csv.reader(h, delimiter=';', quotechar='"')
                total = 0
                for row in reader:
                    pfi_is_fleche = (row[0] == 'PFI fléché')

                    created = NatureComptableRecette.objects.update_or_create(
                        enveloppe=row[1],
                        label_fonds=row[2],
                        code_fonds=row[3],
                        code_nature_comptable=row[5],
                        label_nature_comptable=row[4],
                        code_compte_budgetaire=row[7],
                        label_compte_budgetaire=row[6],
                        is_fleche=pfi_is_fleche,
                        defaults={'is_active': True}
                    )[1]
                    total += int(created)
                print('NatureComptableRecette created with %s : %s' %
                    (filename, total))
