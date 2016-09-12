import csv

from django.core.management.base import BaseCommand

from budgetweb.models import Structure


class Command(BaseCommand):
    help = 'Import the structures from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

    def handle(self, *args, **options):
        max_iterations = 10

        # Parent nodes
        node = Structure.objects.update_or_create(
            code='1010', groupe1='Etablissement',
            label='Etablissement principal', depth=1,
            defaults={'is_active': True}
        )[0]
        node = Structure.objects.update_or_create(
            code='1020', groupe1='Etablissement',
            label='Valorisation de la recherche', depth=1,
            defaults={'is_active': True}
        )[0]
        node = Structure.objects.update_or_create(
            code='1030', groupe1='Etablissement',
            label='Presse universitaire', depth=1,
            defaults={'is_active': True}
        )[0]
        node = Structure.objects.update_or_create(
            code='1040', groupe1='Etablissement',
            label='Université Ouverte des Humanités', depth=1,
            defaults={'is_active': True}
        )[0]

        for filename in options.get('filename'):
            with open(filename) as h:
                reader = csv.DictReader(h, delimiter=';', quotechar='"')
                total = 0
                structures = {}
                for row in reader:
                    code = row['CF']
                    structures[code] = {
                        'code': code,
                        'groupe1': row['Groupe1'],
                        'groupe2': row['Groupe2'],
                        'label': row['Label'],
                        'parent': row['CFParent']
                    }

                iteration = 0
                while structures and iteration < max_iterations:
                    treated = []
                    for code, structure in structures.items():
                        try:
                            parent = Structure.objects.get(code=structure['parent'])
                            structure['parent'] = parent
                            structure['depth'] = parent.depth + 1
                            created = Structure.objects.update_or_create(**structure)[1]
                            treated.append(code)
                            total += int(created)
                        except Structure.DoesNotExist:
                            pass
                    structures = {k: v for k, v in structures.items()
                                  if k not in treated}
                    iteration += 1

            print('Stuctures created with %s : %s\n\tMissing: %s' %
                  (filename, total, ', '.join(structures.keys())))
