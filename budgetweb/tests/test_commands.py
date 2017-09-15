from decimal import Decimal
from io import StringIO
import random

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from budgetweb.apps.structure.models import (
    DomaineFonctionnel, NatureComptableDepense, NatureComptableRecette,
    PlanFinancement, Structure)
from budgetweb.models import Depense, PeriodeBudget, Recette, StructureMontant


class CheckStructureMontantsTest(TestCase):

    fixtures = [
        'tests/periodebudgets', 'tests/structures',
        'tests/domainefonctionnels', 'tests/planfinancements',
        'tests/naturecomptabledepenses', 'tests/naturecomptablerecettes'
    ]

    def setUp(self):
        self.period = PeriodeBudget.objects.first()
        self.domain = DomaineFonctionnel.objects.first()
        self.structure_ecp = Structure.objects.get(code='ECP')
        self.pfi_ecp = PlanFinancement.objects.get(
            code='NA', structure=self.structure_ecp)
        self.naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi_ecp.is_fleche)
        self.naturecomptablerecette = NatureComptableRecette.objects.get(
            code_nature_comptable='9RSCS', is_fleche=self.pfi_ecp.is_fleche)

    def test_comparison_without_structure_montants(self):
        # Create Depense and Recette objects without triggering the save method
        depenses = [Depense(
            structure=self.structure_ecp, pfi=self.pfi_ecp,
            periodebudget=self.period, annee=self.period.annee,
            naturecomptabledepense=self.naturecomptabledepense,
            domainefonctionnel=self.domain, montant_ae=Decimal(1),
            montant_cp=Decimal(2), montant_dc=Decimal(3))]

        recettes = [Recette(
            structure=self.structure_ecp, pfi=self.pfi_ecp,
            periodebudget=self.period, annee=self.period.annee,
            naturecomptablerecette=self.naturecomptablerecette,
            montant_ar=Decimal(10), montant_re=Decimal(20),
            montant_dc=Decimal(20))]

        Depense.objects.bulk_create(depenses)
        Recette.objects.bulk_create(recettes)

        out = StringIO()
        call_command('check_structuremontants', stdout=out)
        value = out.getvalue().strip()
        self.assertIn('ERRORS', value)
        for amount in ('depense_montant_cp', 'depense_montant_dc',
                       'depense_montant_ae', 'recette_montant_dc',
                       'recette_montant_ar', 'recette_montant_re'):
            self.assertIn(amount, value)


class CheckMigratePluriannuelTest(TestCase):

    fixtures = [
        'tests/periodebudgets', 'tests/structures',
        'tests/domainefonctionnels', 'tests/planfinancements',
        'tests/naturecomptabledepenses', 'tests/naturecomptablerecettes'
    ]

    def setUp(self):
        self.period_bi = PeriodeBudget.objects.get(pk=1)
        self.period_vir1 = PeriodeBudget.objects.create(period_id=2, annee=2017)
        self.period_br1 = PeriodeBudget.objects.create(period_id=3, annee=2017)
        self.domain = DomaineFonctionnel.objects.first()
        self.structure = Structure.objects.get(code='ECP3')
        self.pfi = PlanFinancement.objects.get(
            code='SA5ECP01', structure=self.structure)

        # NatureComptableDepense
        self.nature_9dloc = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi.is_fleche)
        self.nature_9dmai = NatureComptableDepense.objects.get(
            code_nature_comptable='9DMAI', is_fleche=self.pfi.is_fleche)
        self.nature_9ddoc = NatureComptableDepense.objects.get(
            code_nature_comptable='9DDOC', is_fleche=self.pfi.is_fleche)

        self.nature_9rscs = NatureComptableRecette.objects.get(
            code_nature_comptable='9RSCS', is_fleche=self.pfi.is_fleche)
        self.nature_9rfia = NatureComptableRecette.objects.get(
            code_nature_comptable='9RFIA', is_fleche=self.pfi.is_fleche)
        self.nature_9ranr = NatureComptableRecette.objects.get(
            code_nature_comptable='9RANR', is_fleche=self.pfi.is_fleche)

    def _create_depense(self, period, year, nature, ae, cp, dc):
        depense_values = {
            'structure': self.structure, 'pfi': self.pfi,
            'domainefonctionnel': self.domain}
        Depense.objects.create(
            periodebudget=period, annee=year, naturecomptabledepense=nature,
            montant_ae=ae, montant_cp=cp, montant_dc=dc, **depense_values)

    def _create_recette(self, period, year, nature, ar, re, dc):
        recette_values = {'structure': self.structure, 'pfi': self.pfi}
        Recette.objects.create(
            periodebudget=period, annee=year, naturecomptablerecette=nature,
            montant_ar=ar, montant_re=re, montant_dc=dc, **recette_values)

    def assertAmountsEqual(self, obj, **amounts):
        self.assertTrue(
            all(
                getattr(obj, name) == amount
                for name, amount in amounts.items()
            ),
            "The {0._meta.model}(pk={0.pk}) object does not have the "
            "values {1}".format(obj, amounts)
        )

    def test_migrate_pluriannuel_depenses(self):
        PeriodeBudget.objects.update(is_active=False)
        period_bi2018 = PeriodeBudget.objects.create(period_id=1, annee=2018) 

        # Depenses
        # BI 2017 - year 2016
        self._create_depense(self.period_bi, 2016, self.nature_9dloc,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_depense(self.period_bi, 2016, self.nature_9dmai,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_depense(self.period_bi, 2016, self.nature_9ddoc,
                             Decimal(31), Decimal(32), Decimal(33))
        # BI 2017 - year 2017
        self._create_depense(self.period_bi, 2017, self.nature_9dloc,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_depense(self.period_bi, 2017, self.nature_9dmai,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_depense(self.period_bi, 2017, self.nature_9ddoc,
                             Decimal(31), Decimal(32), Decimal(33))
        # BI 2017 - year 2018
        self._create_depense(self.period_bi, 2018, self.nature_9dloc,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_depense(self.period_bi, 2018, self.nature_9dmai,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_depense(self.period_bi, 2018, self.nature_9ddoc,
                             Decimal(31), Decimal(32), Decimal(33))
        # VIR1 2017 - year 2017
        self._create_depense(self.period_vir1, 2017, self.nature_9dloc,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_depense(self.period_vir1, 2017, self.nature_9dmai,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_depense(self.period_vir1, 2017, self.nature_9ddoc,
                             Decimal(31), Decimal(32), Decimal(33))
        # BR1 2017 - year 2017
        self._create_depense(self.period_br1, 2017, self.nature_9dloc,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_depense(self.period_br1, 2017, self.nature_9dmai,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_depense(self.period_br1, 2017, self.nature_9ddoc,
                             Decimal(31), Decimal(32), Decimal(33))
        # VIR1 2017 - year 2018
        self._create_depense(self.period_br1, 2018, self.nature_9dloc,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_depense(self.period_br1, 2018, self.nature_9dmai,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_depense(self.period_br1, 2018, self.nature_9ddoc,
                             Decimal(31), Decimal(32), Decimal(33))

        out = StringIO()
        call_command('migrate_pluriannuel', '2018', stdout=out)
        self.assertIn('ERRORS', out.getvalue().strip())

        # 2017
        self.assertAmountsEqual(
            Depense.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2017, naturecomptabledepense=self.nature_9dloc),
            montant_ae=Decimal(44), montant_cp=Decimal(48),
            montant_dc=Decimal(52))
        self.assertAmountsEqual(
            Depense.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2017, naturecomptabledepense=self.nature_9dmai),
            montant_ae=Decimal(84), montant_cp=Decimal(88),
            montant_dc=Decimal(92))
        self.assertAmountsEqual(
            Depense.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2017, naturecomptabledepense=self.nature_9ddoc),
            montant_ae=Decimal(124), montant_cp=Decimal(128),
            montant_dc=Decimal(132))

        # 2018
        self.assertAmountsEqual(
            Depense.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2018, naturecomptabledepense=self.nature_9dloc),
            montant_ae=Decimal(22), montant_cp=Decimal(24),
            montant_dc=Decimal(26))
        self.assertAmountsEqual(
            Depense.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2018, naturecomptabledepense=self.nature_9dmai),
            montant_ae=Decimal(42), montant_cp=Decimal(44),
            montant_dc=Decimal(46))
        self.assertAmountsEqual(
            Depense.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2018, naturecomptabledepense=self.nature_9ddoc),
            montant_ae=Decimal(62), montant_cp=Decimal(64),
            montant_dc=Decimal(66))

    def test_migrate_pluriannuel_recettes(self):
        PeriodeBudget.objects.update(is_active=False)
        period_bi2018 = PeriodeBudget.objects.create(period_id=1, annee=2018) 

        # Depenses
        # BI 2017 - year 2016
        self._create_recette(self.period_bi, 2016, self.nature_9rscs,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_recette(self.period_bi, 2016, self.nature_9rfia,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_recette(self.period_bi, 2016, self.nature_9ranr,
                             Decimal(31), Decimal(32), Decimal(33))
        # BI 2017 - year 2017
        self._create_recette(self.period_bi, 2017, self.nature_9rscs,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_recette(self.period_bi, 2017, self.nature_9rfia,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_recette(self.period_bi, 2017, self.nature_9ranr,
                             Decimal(31), Decimal(32), Decimal(33))
        # BI 2017 - year 2018
        self._create_recette(self.period_bi, 2018, self.nature_9rscs,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_recette(self.period_bi, 2018, self.nature_9rfia,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_recette(self.period_bi, 2018, self.nature_9ranr,
                             Decimal(31), Decimal(32), Decimal(33))
        # VIR1 2017 - year 2017
        self._create_recette(self.period_vir1, 2017, self.nature_9rscs,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_recette(self.period_vir1, 2017, self.nature_9rfia,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_recette(self.period_vir1, 2017, self.nature_9ranr,
                             Decimal(31), Decimal(32), Decimal(33))
        # BR1 2017 - year 2017
        self._create_recette(self.period_br1, 2017, self.nature_9rscs,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_recette(self.period_br1, 2017, self.nature_9rfia,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_recette(self.period_br1, 2017, self.nature_9ranr,
                             Decimal(31), Decimal(32), Decimal(33))
        # VIR1 2017 - year 2018
        self._create_recette(self.period_br1, 2018, self.nature_9rscs,
                             Decimal(11), Decimal(12), Decimal(13))
        self._create_recette(self.period_br1, 2018, self.nature_9rfia,
                             Decimal(21), Decimal(22), Decimal(23))
        self._create_recette(self.period_br1, 2018, self.nature_9ranr,
                             Decimal(31), Decimal(32), Decimal(33))

        out = StringIO()
        call_command('migrate_pluriannuel', '2018', stdout=out)
        self.assertIn('ERRORS', out.getvalue().strip())

        # 2017
        self.assertAmountsEqual(
            Recette.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2017, naturecomptablerecette=self.nature_9rscs),
            montant_ar=Decimal(44), montant_re=Decimal(48),
            montant_dc=Decimal(52))
        self.assertAmountsEqual(
            Recette.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2017, naturecomptablerecette=self.nature_9rfia),
            montant_ar=Decimal(84), montant_re=Decimal(88),
            montant_dc=Decimal(92))
        self.assertAmountsEqual(
            Recette.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2017, naturecomptablerecette=self.nature_9ranr),
            montant_ar=Decimal(124), montant_re=Decimal(128),
            montant_dc=Decimal(132))

        # 2018
        self.assertAmountsEqual(
            Recette.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2018, naturecomptablerecette=self.nature_9rscs),
            montant_ar=Decimal(22), montant_re=Decimal(24),
            montant_dc=Decimal(26))
        self.assertAmountsEqual(
            Recette.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2018, naturecomptablerecette=self.nature_9rfia),
            montant_ar=Decimal(42), montant_re=Decimal(44),
            montant_dc=Decimal(46))
        self.assertAmountsEqual(
            Recette.objects.get(
                periodebudget__period__code='BI', periodebudget__annee=2018,
                annee=2018, naturecomptablerecette=self.nature_9ranr),
            montant_ar=Decimal(62), montant_re=Decimal(64),
            montant_dc=Decimal(66))
