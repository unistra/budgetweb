import csv

from django.core.management.base import BaseCommand

from budgetweb.models import NatureComptableDepense


class Command(BaseCommand):
    help = 'Import the NatureComptableDepense from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

    def handle(self, *args, **options):
        for filename in options.get('filename'):
            with open(filename) as h:
                reader = csv.reader(h, delimiter=';', quotechar='"')
                total = 0
                for row in reader:
                    pfi_is_fleche = (row[0] == 'PFI fléché')
                    decalage = (row[6] == 'oui')
                    if row[1] == "Fonctionnement":
                        priority_nc = 1
                    elif row[1] == "Personnel":
                        priority_nc = 2
                    else:
                        priority_nc = 3
                    created = NatureComptableDepense.objects.update_or_create(
                        enveloppe=row[1],
                        label_nature_comptable=row[2],
                        code_nature_comptable=row[3],
                        code_compte_budgetaire=row[4],
                        label_compte_budgetaire=row[5],
                        is_fleche=pfi_is_fleche,
                        is_decalage_tresorerie=decalage,
                        priority=priority_nc,
                        defaults={'is_active': True}
                    )[1]
                    total += int(created)
                print('NatureComptableDepense created with %s : %s' % (filename, total))
