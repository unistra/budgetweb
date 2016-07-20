import csv
import re

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from budgetweb.models import Structure, StructureAuthorizations


class Command(BaseCommand):
    help = 'Import the functional domains from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

    def handle(self, *args, **options):
        for filename in options.get('filename'):
            total = 0
            missing_structures = set()
            with open(filename) as h:
                reader = csv.reader(h, delimiter=';', quotechar='"')
                users = {}
                for row in reader:
                    try:
                        username = row[0]
                        structure = re.findall('^[a-zA-Z0-9]*', row[1])[0]
                        try:
                            User.objects.get(username=username)
                        except User.DoesNotExist:
                            User.objects.create_user(username, password='!')

                        try:
                            structure = Structure.objects.get(code=structure)
                            users.setdefault(username, []).append(structure)
                        except Structure.DoesNotExist:
                            missing_structures.update([structure])
                            continue
                    except IndexError:
                        pass

                for username, structures in users.items():
                    user = User.objects.get(username=username)
                    authorizations = None
                    try:
                        authorizations = user.structureauthorizations
                    except StructureAuthorizations.DoesNotExist:
                        authorizations = StructureAuthorizations(user=user)
                        authorizations.save()
                    for structure in structures:
                        authorizations.structures.add(structure)
                    authorizations.save()

            print('Authorizations created with %s : %s'
                  '\n\tMissing structures : %s'
                  % (filename, total, missing_structures))
