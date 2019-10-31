import datetime
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import TestCase

from budgetweb.apps.structure.models import (
    DomaineFonctionnel, NatureComptableDepense, NatureComptableRecette,
    PlanFinancement, Structure)
from budgetweb.utils import (
    get_authorized_structures_ids, get_current_year, get_pfi_total,
    get_pfi_years, in_groups)
from ..models import Depense, PeriodeBudget, Recette


class UtilsTest(TestCase):

    fixtures = [
        'tests/structures', 'tests/periodebudgets',
        'tests/structureauthorizations'
    ]

    def test_get_current_year(self):
        self.assertEqual(get_current_year(), 2017)

    def test_get_authorized_structures_ids(self):
        user = User.objects.get(pk=100)
        self.assertSetEqual(
            get_authorized_structures_ids(user)[0], {4})

    def test_get_authorized_structures_ids_with_hierarchy(self):
        user = User.objects.get(pk=100)
        self.assertSetEqual(
            get_authorized_structures_ids(user)[1], {4, 1})

    def test_get_authorized_structures_superuser(self):
        admin_user = User.objects.create_superuser(
            'admin', email='admin@unistra.fr', password='pass')
        active_structures = Structure.objects.filter(is_active=True)
        self.assertEqual(
            len(get_authorized_structures_ids(admin_user)[0]),
            len(active_structures)
        )

    def test_in_groups(self):
        admin_user = User.objects.create_superuser(
            'admin', email='admin@unistra.fr', password='pass')
        self.assertTrue(in_groups(admin_user, 'unexisting'))
        self.assertFalse(in_groups(admin_user, 'unexisting', superuser=False))

        user = User.objects.create_user('user_in_groups')
        group = Group.objects.create(name='existing')
        self.assertFalse(in_groups(user, 'existing'))
        user.groups.add(group)
        self.assertTrue(in_groups(user, 'existing'))


class PFIUtilsTest(TestCase):

    fixtures = [
        'tests/periodebudgets', 'tests/structures', 'tests/planfinancements',
        'tests/domainefonctionnels', 'tests/naturecomptabledepenses',
        'tests/naturecomptablerecettes'
    ]

    def setUp(self):
        self.structure_ecp = Structure.objects.get(code='ECP')
        self.pfi_ecp = PlanFinancement.objects.get(
            code='NA', structure__code='ECP')
        self.periode = PeriodeBudget.objects.first()
        self.annee = self.periode.annee
        self.naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi_ecp.is_fleche)
        self.naturecomptablerecette = NatureComptableRecette.objects.get(
            code_nature_comptable='9RSCS', is_fleche=self.pfi_ecp.is_fleche)
        self.domaine = DomaineFonctionnel.objects.get(pk=1)

    def test_get_pfi_total(self):
        Depense.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=self.naturecomptabledepense,
            montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
        )
        Depense.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=self.naturecomptabledepense,
            montant_dc=Decimal(10), montant_cp=Decimal(20),
            montant_ae=Decimal(30)
        )

        Recette.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=self.naturecomptablerecette,
            montant_dc=Decimal(4), montant_re=Decimal(5), montant_ar=Decimal(6)
        )
        Recette.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=self.naturecomptablerecette,
            montant_dc=Decimal(40), montant_re=Decimal(50),
            montant_ar=Decimal(60)
        )
        total_depense, total_recette = get_pfi_total(self.pfi_ecp)

        self.assertEqual(total_depense[0]['sum_depense_dc'], Decimal(11))
        self.assertEqual(total_depense[0]['sum_depense_cp'], Decimal(22))
        self.assertEqual(total_depense[0]['sum_depense_ae'], Decimal(33))
        self.assertEqual(total_recette[0]['sum_recette_dc'], Decimal(44))
        self.assertEqual(total_recette[0]['sum_recette_re'], Decimal(55))
        self.assertEqual(total_recette[0]['sum_recette_ar'], Decimal(66))

    def test_get_pfi_total_with_years(self):
        Depense.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=self.naturecomptabledepense,
            montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
        )
        Depense.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp,
            annee=self.annee - 1, periodebudget=self.periode,
            domainefonctionnel=self.domaine,
            naturecomptabledepense=self.naturecomptabledepense,
            montant_dc=Decimal(10), montant_cp=Decimal(20),
            montant_ae=Decimal(30)
        )

        Recette.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=self.naturecomptablerecette,
            montant_dc=Decimal(4), montant_re=Decimal(5), montant_ar=Decimal(6)
        )
        Recette.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp,
            annee=self.annee - 1, periodebudget=self.periode,
            naturecomptablerecette=self.naturecomptablerecette,
            montant_dc=Decimal(40), montant_re=Decimal(50),
            montant_ar=Decimal(60)
        )
        total_depense, total_recette = get_pfi_total(
            self.pfi_ecp, year=self.annee)

        self.assertEqual(total_depense[0]['sum_depense_dc'], Decimal(10))
        self.assertEqual(total_depense[0]['sum_depense_cp'], Decimal(20))
        self.assertEqual(total_depense[0]['sum_depense_ae'], Decimal(30))
        self.assertEqual(total_recette[0]['sum_recette_dc'], Decimal(40))
        self.assertEqual(total_recette[0]['sum_recette_re'], Decimal(50))
        self.assertEqual(total_recette[0]['sum_recette_ar'], Decimal(60))

    def test_get_pfi_years(self):
        self.pfi_ecp.date_debut = datetime.date(2015, 1, 1)
        self.pfi_ecp.date_fin = datetime.date(2025, 12, 31)
        self.pfi_ecp.save()

        self.assertListEqual(
            get_pfi_years(self.pfi_ecp), [2016, 2017, 2018, 2019, 2020])
        self.assertListEqual(
            get_pfi_years(self.pfi_ecp, year_number=2), [2016, 2017, 2018])
        self.assertListEqual(get_pfi_years(
            self.pfi_ecp, begin_current_period=False),
            [2016, 2017, 2018, 2019, 2020])
        self.assertListEqual(
            get_pfi_years(
                self.pfi_ecp, begin_current_period=False, year_number=2),
            [2016, 2017, 2018])
        self.assertListEqual(
            get_pfi_years(
                self.pfi_ecp, begin_current_period=False, year_number=0),
            [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
        self.assertListEqual(
            get_pfi_years(self.pfi_ecp, year_number=0),
            [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
