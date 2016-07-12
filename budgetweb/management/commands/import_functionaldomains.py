import csv

from django.core.management.base import BaseCommand

from budgetweb.models import DomaineFonctionnel


class Command(BaseCommand):
    help = 'Import the functional domains from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

    def handle(self, *args, **options):
        for filename in options.get('filename'):
            with open(filename) as h:
                reader = csv.reader(h, delimiter=';', quotechar='"')
                for row in reader:
                    DomaineFonctionnel.objects.update_or_create(
                        code=row[0], label=row[1], defaults={'is_active': True}
                    )
