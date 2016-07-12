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
                created = 0
                for row in reader:
                    if row[0]=='PFI fléché':
                        pfi_is_fleche = True
                    else:
                        pfi_is_fleche = False
                    if row[6]=='oui':
                        decalage = True
                    else:
                        decalage = False

                    NatureComptableDepense.objects.update_or_create(
                        enveloppe=row[1], label_nature_comptable=row[2],
                        code_nature_comptable=row[3], code_compte_budgetaire=row[4],
                        label_compte_budgetaire=row[5],is_fleche=pfi_is_fleche,
                        is_decalage_tresorerie=decalage,
                        defaults={'is_active': True}
                    )
                    created += 1
                print('NatureComptableDepense created with %s : %s' % (filename, created, ))
