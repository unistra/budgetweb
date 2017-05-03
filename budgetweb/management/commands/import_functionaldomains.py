import csv

from django.core.management.base import BaseCommand

from budgetweb.apps.structure.models import DomaineFonctionnel


class Command(BaseCommand):
    help = 'Import the functional domains from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

    def handle(self, *args, **options):
        for filename in options.get('filename'):
            with open(filename) as h:
                reader = csv.reader(h, delimiter=';', quotechar='"')
                total = 0
                for row in reader:
                    created = DomaineFonctionnel.objects.update_or_create(
                        code=row[0], defaults={'is_active': True,
                                               'label': row[1],
                                               'label_court': row[2]}
                    )[1]
                    total += int(created)
                print('Functional Domains created with %s : %s'
                      % (filename, total))
