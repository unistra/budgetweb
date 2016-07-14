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
            code='ETAB', type='Etablissement',
            label='Université de Strasbourg', defaults={'is_active': True}
        )[0]
        Structure.objects.update_or_create(
            code='RCH', type='Recherche', label='Recherche', parent=node,
            defaults={'is_active': True}
        )
        Structure.objects.update_or_create(
            code='SCX', type='Services Centraux', label='Services Centraux',
            parent=node, defaults={'is_active': True}
        )
        Structure.objects.update_or_create(
            code='PAIE', type='Paie', label='Paie',
            parent=node, defaults={'is_active': True}
        )

        for filename in options.get('filename'):
            with open(filename) as h:
                reader = csv.DictReader(h, delimiter=';', quotechar='"')
                total = 0
                structures = {}
                for row in reader:
                    code = row['CF']
                    structures[code] = {
                        'code': code,
                        'type': row['Groupe1'],
                        'label': row['Désignation  CF'],
                        'parent': row['CF Sup. sifac']
                    }

                iteration = 0
                while structures and iteration < max_iterations:
                    treated = []
                    for code, structure in structures.items():
                        try:
                            parent = Structure.objects.get(code=structure['parent'])
                            structure['parent'] = parent
                            created = Structure.objects.update_or_create(**structure)[1]
                            treated.append(code)
                            total += int(created)
                        except Structure.DoesNotExist:
                            pass
                    structures = {k: v for k, v in structures.items()\
                                  if k not in treated}
                    iteration += 1

            print('Stuctures created with %s : %s\n\tMissing: %s' %
                  (filename, total, ', '.join(structures.keys())))
