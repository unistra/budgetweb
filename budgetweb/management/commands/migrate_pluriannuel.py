from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import Q, Sum

from budgetweb.apps.structure.models import PlanFinancement
from budgetweb.models import Depense, PeriodeBudget, Recette


class Command(BaseCommand):
    help = 'Check if the StructureMontant objects are correct'

    def add_arguments(self, parser):
        parser.add_argument('year', nargs=1, metavar='YEAR', type=int)

    def create_depenses(self, pfi, *args, **kwargs):
        year = kwargs.pop('year', None)
        extra_values = kwargs.pop('extra_values', [])
        values = ['structure', 'naturecomptabledepense',
                  'domainefonctionnel'] + extra_values
        depenses = pfi.depense_set\
            .filter(*args, **kwargs)\
            .values(*values)\
            .annotate(Sum('montant_ae'), Sum('montant_cp'), Sum('montant_dc'))

        depenses_list = [
            Depense(
                structure_id=depense['structure'], pfi=pfi,
                periodebudget=self.period, annee=year or depense['annee'],
                naturecomptabledepense_id=depense['naturecomptabledepense'],
                domainefonctionnel_id=depense['domainefonctionnel'],
                montant_ae=depense['montant_ae__sum'],
                montant_cp=depense['montant_cp__sum'],
                montant_dc=depense['montant_dc__sum'])
            for depense in depenses
        ]
        return depenses_list

    def create_recettes(self, pfi, *args, **kwargs):
        year = kwargs.pop('year', None)
        extra_values = kwargs.pop('extra_values', [])
        values = ['structure', 'naturecomptablerecette'] + extra_values
        recettes = pfi.recette_set\
            .filter(*args, **kwargs)\
            .values(*values)\
            .annotate(Sum('montant_ar'), Sum('montant_re'), Sum('montant_dc'))

        recettes_list = [
            Recette(
                structure_id=recette['structure'], pfi=pfi,
                periodebudget=self.period, annee=year or recette['annee'],
                naturecomptablerecette_id=recette['naturecomptablerecette'],
                montant_ar=recette['montant_ar__sum'],
                montant_re=recette['montant_re__sum'],
                montant_dc=recette['montant_dc__sum'])
            for recette in recettes
        ]
        return recettes_list

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')

        for year in options.get('year'):
            try:
                self.period = PeriodeBudget.objects.get(
                    annee=year, period__code='BI')
            except PeriodeBudget.DoesNotExist:
                raise Exception('Erreur : Période BI %s inexistante' % year)

            if self.period.has_entries():
                raise Exception('Erreur : Entrées déjà existantes pour la '
                                'période BI %s ' % year)

            depenses = []
            recettes = []
            for pfi in pfis:
                # Budget antérieur
                depenses.extend(self.create_depenses(
                    pfi,
                    (Q(annee=year - 2) | Q(annee=year - 1)),
                    year=year - 1, periodebudget__annee=year - 1))
                recettes.extend(self.create_recettes(
                    pfi,
                    (Q(annee=year - 2) | Q(annee=year - 1)),
                    year=year - 1, periodebudget__annee=year - 1))

                # Budgets futurs
                depenses.extend(self.create_depenses(
                    pfi, extra_values=['annee'], annee__gte=year,
                    periodebudget__annee=year - 1))
                recettes.extend(self.create_recettes(
                    pfi, extra_values=['annee'], annee__gte=year,
                    periodebudget__annee=year - 1))

            # bulk_create is faster but it does not trigger the save method.
            # Therefore, this script needs to launch check_structuremontants
            Depense.objects.bulk_create(depenses)
            Recette.objects.bulk_create(recettes)

            check_structuremontants_parameters = filter(
                bool, ('-v %s' % verbosity,))

            call_command('check_structuremontants', '-u', '-y %s' % year ,
                         *check_structuremontants_parameters, stdout=self.stdout)
