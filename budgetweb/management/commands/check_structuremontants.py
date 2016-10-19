from decimal import Decimal

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction

from budgetweb.models import Depense, Recette, Structure, StructureMontant
from budgetweb.utils import get_current_year


class Command(BaseCommand):
    help = 'Check if the StructureMontant objects are correct'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '-u', '--update',
            action='store_true',
            dest='update',
            default=False,
            help='StructureMontant objects are updated if a difference in the '
                 'calculation is found'
        )

    def get_structure_ancestors(self, structure_id):
        parent = self.structures[structure_id]
        return [parent] + self.get_structure_ancestors(parent) if parent else []

    def handle(self, *args, **options):
        self.structures = {s.pk: s.parent_id for s in Structure.active.all()}
        comptabilites = {}
        errors = []

        with transaction.atomic():
            structure_montants = list(StructureMontant.active_period\
                .filter(structure__is_active=True, annee=get_current_year())\
                .select_related('structure'))

            comptabilites = {
                'depense': {
                    'model': Depense,
                    'values': list(Depense.active_period.filter(
                                           annee=get_current_year()).all()),
                },
                'recette': {
                    'model': Recette,
                    'values': list(Recette.active_period.filter(
                                           annee=get_current_year()).all()),
                },
            }

        # Recalculation of the StructureMontant objects
        check_results = {s: {} for s in self.structures.keys()}
        for comptabilite, infos in comptabilites.items():
            montant_name = lambda x: '%s_%s' % (comptabilite, x)
            model = infos['model']
            values = infos['values']
            intial_montants = model().initial_montants
            for value in values:
                structures = [value.structure.pk] +\
                    self.get_structure_ancestors(value.structure.pk)
                for structure in structures:
                    montants_dict = check_results.setdefault(structure, {})
                    for montant in intial_montants:
                        key = montant_name(montant)
                        old_value = montants_dict.get(key, Decimal(0))
                        montants_dict[key] = old_value + getattr(value, montant)

        # Check the differences
        for structure_montant in structure_montants:
            check_result = check_results[structure_montant.structure.pk]
            comptabilite_montants = []
            for comptabilite, infos in comptabilites.items():
                montant_name = lambda x: '%s_%s' % (comptabilite, x)
                comptabilite_montants += list(map(montant_name, infos['model']().initial_montants))
            for montant in comptabilite_montants:
                result1 = check_result.get(montant, Decimal(0))
                result2 = getattr(structure_montant, montant) or Decimal(0)
                if result1 != result2:
                    error_str = 'StructureMontant (pk={0.pk}) : {0.structure.code}. {1} : {2} - Calculated : {3}'.format(
                        structure_montant, montant, result1, result2)
                    # If we find a diff, we update them !
                    if options['update']:
                        sm = StructureMontant.objects.get(pk=structure_montant.pk)
                        setattr(sm, montant, result1)
                        sm.save()
                    errors.append(error_str)

        if errors:
            self.stdout.write('ERRORS : \n{}'.format('\n'.join(errors)))
        else:
            self.stdout.write('No calculation errors')
