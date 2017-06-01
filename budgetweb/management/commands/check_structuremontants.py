from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from budgetweb.models import Depense, PeriodeBudget, Recette, StructureMontant
from budgetweb.utils import get_current_year
from budgetweb.apps.structure.models import Structure


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
        parser.add_argument(
            '-p', dest='periods', nargs='+', help='Periods', metavar='PERIOD')
        parser.add_argument(
            '-y', dest='years', nargs='+', help='Years', type=int,
            metavar='YEAR')

    def get_structure_ancestors(self, structure_id):
        parent = self.structures[structure_id]
        return [parent] + self.get_structure_ancestors(parent) if parent else []

    def handle(self, *args, **options):
        self.structures = {s.pk: s.parent_id for s in Structure.active.all()}
        comptabilites = {}
        errors = []

        periods = PeriodeBudget.active.all()
        active_periods = options.get('periods', [])\
            or periods.values_list('period__code', flat=True)
        active_years = options.get('years', [])\
            or set(periods.values_list('annee', flat=True))
        default_filters = {
            'annee__in': active_years,
            'periodebudget__period__code__in': active_periods,
        }

        with transaction.atomic():
            structure_montants = list(StructureMontant.objects\
                .filter(structure__is_active=True, **default_filters)\
                .select_related('structure', 'periodebudget__period'))

            comptabilites = {
                'depense': {
                    'model': Depense,
                    'values': list(
                        Depense.objects.filter(**default_filters)\
                            .select_related(
                                'structure', 'periodebudget__period').all()),
                },
                'recette': {
                    'model': Recette,
                    'values': list(
                        Recette.objects.filter(**default_filters)\
                            .select_related(
                                'structure', 'periodebudget__period').all()),
                },
            }

        # Recalculation of the StructureMontant objects
        # check_results = {s: {} for s in self.structures.keys()}
        check_results = {}
        for comptabilite, infos in comptabilites.items():
            montant_name = lambda x: '%s_%s' % (comptabilite, x)
            model = infos['model']
            values = infos['values']
            intial_montants = model().initial_montants
            for value in values:
                structures = [value.structure.pk] +\
                    self.get_structure_ancestors(value.structure.pk)
                for structure in structures:
                    montant_key = (structure,
                         value.periodebudget.period.code,
                         value.annee)
                    montants_dict = check_results.setdefault(montant_key, {})
                    for montant in intial_montants:
                        key = montant_name(montant)
                        old_value = montants_dict.get(key, Decimal(0))
                        montants_dict[key] = old_value + getattr(value, montant)

        # Check the differences
        for structure_montant in structure_montants:
            key = (
                structure_montant.structure.pk,
                structure_montant.periodebudget.period.code,
                structure_montant.annee,
            )
            check_result = check_results.get(key, {})
            comptabilite_montants = []
            for comptabilite, infos in comptabilites.items():
                montant_name = lambda x: '%s_%s' % (comptabilite, x)
                comptabilite_montants += list(map(montant_name, infos['model']().initial_montants))
            for montant in comptabilite_montants:
                result1 = getattr(structure_montant, montant) or Decimal(0)
                result2 = check_result.get(montant, Decimal(0))
                if result1 != result2:
                    error_str = 'StructureMontant (pk={0.pk}) : {0.structure.code}. {1} : {2} - Calculated : {3}'.format(
                        structure_montant, montant, result1, result2)
                    # If we find a difference, we update it !
                    if options['update']:
                        sm = StructureMontant.objects.get(pk=structure_montant.pk)
                        setattr(sm, montant, result2)
                        sm.save()
                    errors.append(error_str)

        if errors:
            self.stdout.write('ERRORS : \n{}'.format('\n'.join(errors)))
        else:
            self.stdout.write('No calculation errors')
