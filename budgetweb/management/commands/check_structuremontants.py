from decimal import Decimal

from django.core.management.base import NoArgsCommand
from django.core.management import call_command
from django.db import transaction

from budgetweb.models import Depense, Recette, Structure, StructureMontant


class Command(NoArgsCommand):
    help = 'Check if the StructureMontant objects are correct'


    def get_structure_ancestors(self, structure_id):
        parent = self.structures[structure_id]
        return [parent] + self.get_structure_ancestors(parent) if parent else []


    def handle_noargs(self, **options):
        self.structures = {s.pk : s.parent_id for s in Structure.active.all()}
        montants = []
        comptabilites = {}
        errors = []

        with transaction.atomic():
            structure_montants = list(StructureMontant.active_period.filter(
                structure__is_active=True))

            comptabilites = {
                'depense': {
                    'model': Depense,
                    'values': list(Depense.active_period.all())
                },
                'recette': {
                    'model': Recette,
                    'values': list(Recette.active_period.all()),
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
                    error_str = 'StructureMontant (pk={0.pk}). {1} : {2} - Calculated : {3}'.format(
                        structure_montant, montant, result1, result2)
                    errors.append(error_str)

        if errors:
            print('ERRORS : \n{}'.format('\n'.join(errors)))
        else:
            print('No calculation errors')
