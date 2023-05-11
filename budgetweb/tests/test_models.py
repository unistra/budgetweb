from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from budgetweb.apps.structure.models import (
    DomaineFonctionnel, NatureComptableDepense, NatureComptableRecette,
    PlanFinancement, Structure)
from ..models import (Depense, PeriodeBudget, Recette, StructureAuthorizations,
                      StructureMontant)
from ..utils import get_current_year


class StructureAuthorizationsModelTest(TestCase):

    fixtures = ['tests/structures', 'tests/structureauthorizations']

    def test_str(self):
        auth = StructureAuthorizations.objects.get(pk=1)
        self.assertEqual(str(auth), 'user100')

    def test_save(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        structure_paie = Structure.objects.get(code='PAIE')
        authorizations = StructureAuthorizations(user=user1)
        authorizations.save()
        authorizations.structures.add(structure_paie)
        authorizations.save()

        authorizations = user1.structureauthorizations.structures.all()\
            .order_by('code')
        self.assertEqual(len(authorizations), 4)
        self.assertListEqual(
            [a.code for a in authorizations],
            ['PAIE', 'PAIE7DIN', 'PAIE7ECP', 'PAIE7R101'])

    def test_add_child_structure(self):
        user100 = User.objects.get(pk=100)
        Structure.objects.create(
            groupe1='Recherche',
            code='PAIE_NEW',
            label='Paie New',
            parent_id=4)
        authorization = user100.structureauthorizations.structures\
            .get(code='PAIE_NEW')
        self.assertIsNotNone(authorization)


class PeriodeBudgetModelTest(TestCase):

    fixtures = ['tests/periodebudgets']

    def test_str(self):
        periode = PeriodeBudget.objects.get(pk=1)
        self.assertEqual(str(periode), 'BI - Budget initial - 2017')


class ComptabiliteModelTest(TestCase):

    fixtures = [
        'tests/periodebudgets', 'tests/structures', 'tests/planfinancements',
        'tests/domainefonctionnels', 'tests/naturecomptabledepenses',
        'tests/naturecomptablerecettes'
    ]

    def setUp(self):
        self.structure_ecp = Structure.objects.get(code='ECP')
        self.structure_ecp1 = Structure.objects.get(code='ECP1')
        self.pfi_ecp = PlanFinancement.objects.get(
            code='NA', structure=self.structure_ecp)
        self.pfi_ecp1 = PlanFinancement.objects.get(
            code='NA', structure=self.structure_ecp1)
        self.periode = PeriodeBudget.objects.first()
        self.annee = self.periode.annee
        self.naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi_ecp.is_fleche)
        self.naturecomptablerecette = NatureComptableRecette.objects.get(
            code_nature_comptable='9RSCS', is_fleche=self.pfi_ecp.is_fleche)
        self.domaine = DomaineFonctionnel.objects.get(pk=1)
        self.depense_ecp = Depense.objects.create(
            pfi=self.pfi_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=self.naturecomptabledepense,
            montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
        )
        self.recette_ecp = Recette.objects.create(
            pfi=self.pfi_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=self.naturecomptablerecette,
            montant_dc=Decimal(4), montant_re=Decimal(5), montant_ar=Decimal(6)
        )
        self.depense_ecp1 = Depense(
            pfi=self.pfi_ecp1, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=self.naturecomptabledepense,
            montant_dc=Decimal(10), montant_cp=Decimal(20),
            montant_ae=Decimal(30)
        )
        self.recette_ecp1 = Recette(
            pfi=self.pfi_ecp1,
            annee=self.annee, periodebudget=self.periode,
            naturecomptablerecette=self.naturecomptablerecette,
            montant_dc=Decimal(40), montant_re=Decimal(50),
            montant_ar=Decimal(60)
        )

    def test_montants_ecp(self):
        montants_ecp = StructureMontant.objects.get(
            structure=self.structure_ecp)
        montants_etab = StructureMontant.objects.get(
            structure=self.structure_ecp.parent)

        self.assertEqual(montants_ecp.depense_montant_dc, Decimal(1))
        self.assertEqual(montants_ecp.depense_montant_cp, Decimal(2))
        self.assertEqual(montants_ecp.depense_montant_ae, Decimal(3))
        self.assertEqual(montants_ecp.recette_montant_dc, Decimal(4))
        self.assertEqual(montants_ecp.recette_montant_re, Decimal(5))
        self.assertEqual(montants_ecp.recette_montant_ar, Decimal(6))
        self.assertEqual(montants_etab.depense_montant_dc, Decimal(1))
        self.assertEqual(montants_etab.depense_montant_cp, Decimal(2))
        self.assertEqual(montants_etab.depense_montant_ae, Decimal(3))
        self.assertEqual(montants_etab.recette_montant_dc, Decimal(4))
        self.assertEqual(montants_etab.recette_montant_re, Decimal(5))
        self.assertEqual(montants_etab.recette_montant_ar, Decimal(6))

    def test_montants_ecp_and_ecp1(self):
        self.depense_ecp1.save()
        self.recette_ecp1.save()
        montants_ecp1 = StructureMontant.objects.get(
            structure=self.structure_ecp1)
        montants_ecp = StructureMontant.objects.get(
            structure=self.structure_ecp1.parent)
        montants_etab = StructureMontant.objects.get(
            structure=self.structure_ecp1.parent.parent)

        self.assertEqual(montants_ecp1.depense_montant_dc, Decimal(10))
        self.assertEqual(montants_ecp1.depense_montant_cp, Decimal(20))
        self.assertEqual(montants_ecp1.depense_montant_ae, Decimal(30))
        self.assertEqual(montants_ecp1.recette_montant_dc, Decimal(40))
        self.assertEqual(montants_ecp1.recette_montant_re, Decimal(50))
        self.assertEqual(montants_ecp1.recette_montant_ar, Decimal(60))
        self.assertEqual(montants_ecp.depense_montant_dc, Decimal(11))
        self.assertEqual(montants_ecp.depense_montant_cp, Decimal(22))
        self.assertEqual(montants_ecp.depense_montant_ae, Decimal(33))
        self.assertEqual(montants_ecp.recette_montant_dc, Decimal(44))
        self.assertEqual(montants_ecp.recette_montant_re, Decimal(55))
        self.assertEqual(montants_ecp.recette_montant_ar, Decimal(66))
        self.assertEqual(montants_etab.depense_montant_dc, Decimal(11))
        self.assertEqual(montants_etab.depense_montant_cp, Decimal(22))
        self.assertEqual(montants_etab.depense_montant_ae, Decimal(33))
        self.assertEqual(montants_etab.recette_montant_dc, Decimal(44))
        self.assertEqual(montants_etab.recette_montant_re, Decimal(55))
        self.assertEqual(montants_etab.recette_montant_ar, Decimal(66))

    def test_montants_ecp_and_ecp1_and_delete_ecp(self):
        self.depense_ecp1.save()
        self.recette_ecp1.save()
        self.depense_ecp.delete()
        self.recette_ecp.delete()
        montants_ecp1 = StructureMontant.objects.get(
            structure=self.structure_ecp1)
        montants_ecp = StructureMontant.objects.get(
            structure=self.structure_ecp1.parent)
        montants_etab = StructureMontant.objects.get(
            structure=self.structure_ecp1.parent.parent)

        self.assertEqual(montants_ecp1.depense_montant_dc, Decimal(10))
        self.assertEqual(montants_ecp1.depense_montant_cp, Decimal(20))
        self.assertEqual(montants_ecp1.depense_montant_ae, Decimal(30))
        self.assertEqual(montants_ecp1.recette_montant_dc, Decimal(40))
        self.assertEqual(montants_ecp1.recette_montant_re, Decimal(50))
        self.assertEqual(montants_ecp1.recette_montant_ar, Decimal(60))
        self.assertEqual(montants_ecp.depense_montant_dc, Decimal(10))
        self.assertEqual(montants_ecp.depense_montant_cp, Decimal(20))
        self.assertEqual(montants_ecp.depense_montant_ae, Decimal(30))
        self.assertEqual(montants_ecp.recette_montant_dc, Decimal(40))
        self.assertEqual(montants_ecp.recette_montant_re, Decimal(50))
        self.assertEqual(montants_ecp.recette_montant_ar, Decimal(60))
        self.assertEqual(montants_etab.depense_montant_dc, Decimal(10))
        self.assertEqual(montants_etab.depense_montant_cp, Decimal(20))
        self.assertEqual(montants_etab.depense_montant_ae, Decimal(30))
        self.assertEqual(montants_etab.recette_montant_dc, Decimal(40))
        self.assertEqual(montants_etab.recette_montant_re, Decimal(50))
        self.assertEqual(montants_etab.recette_montant_ar, Decimal(60))


class DepenseModelTest(TestCase):

    fixtures = [
        'tests/periodebudgets', 'tests/structures', 'tests/planfinancements',
        'tests/domainefonctionnels', 'tests/naturecomptabledepenses',
    ]

    def setUp(self):
        self.structure_ecp = Structure.objects.get(code='ECP')
        self.pfi_ecp = PlanFinancement.objects.get(
            code='NA', structure=self.structure_ecp)
        self.periode = PeriodeBudget.objects.first()
        self.annee = self.periode.annee
        self.domaine = DomaineFonctionnel.objects.get(pk=1)

    def test_save(self):
        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi_ecp.is_fleche)

        depense = Depense(
            pfi=self.pfi_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=naturecomptabledepense,
            montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
        )
        depense.save()
        self.assertIsNotNone(depense.pk)

    # def test_save_with_validation_error(self):
    #    naturecomptabledepense = NatureComptableDepense.objects.get(
    #        code_nature_comptable='9DFLU', is_fleche=self.pfi_ecp.is_fleche)
    #    depense = Depense(
    #        pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
    #        periodebudget=self.periode, domainefonctionnel=self.domaine,
    #        naturecomptabledepense=naturecomptabledepense,
    #        montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
    #    )
    #
    #    with self.assertRaises(ValidationError) as ve:
    #        depense.save()
    #    self.assertEqual(
    #        ve.exception.message_dict['montant_ae'][0],
    #        "Le décalagage de trésorerie n'est pas possible sur cette nature "
    #        "comptable.")

    # def test_save_without_montant_dc(self):
    #    naturecomptabledepense = NatureComptableDepense.objects.get(
    #        code_nature_comptable='9DLOC', is_fleche=self.pfi_ecp.is_fleche)

    #    depense = Depense(
    #        pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
    #        periodebudget=self.periode, domainefonctionnel=self.domaine,
    #        naturecomptabledepense=naturecomptabledepense,
    #        montant_cp=Decimal(2), montant_ae=Decimal(3)
    #    )
    #    depense.save()
    #    self.assertIsNotNone(depense.pk)
    #    self.assertEqual(depense.montant_dc, Decimal(3))


class RecetteModelTest(TestCase):

    fixtures = [
        'tests/periodebudgets', 'tests/structures', 'tests/planfinancements',
        'tests/domainefonctionnels', 'tests/naturecomptablerecettes',
    ]

    def setUp(self):
        self.structure_ecp = Structure.objects.get(code='ECP')
        self.pfi_ecp = PlanFinancement.objects.get(
            code='NA', structure=self.structure_ecp)
        self.periode = PeriodeBudget.objects.first()
        self.annee = self.periode.annee
        self.domaine = DomaineFonctionnel.objects.get(pk=1)
        self.naturecomptablerecette = NatureComptableRecette.objects.get(
            code_nature_comptable='9RSCS', is_fleche=self.pfi_ecp.is_fleche)

    def test_save(self):
        recette = Recette(
            pfi=self.pfi_ecp, annee=self.annee, periodebudget=self.periode,
            naturecomptablerecette=self.naturecomptablerecette,
            montant_dc=Decimal(4), montant_re=Decimal(5), montant_ar=Decimal(6)
        )
        recette.save()
        self.assertIsNotNone(recette.pk)

    # def test_save_without_montant_dc(self):
    #    recette = Recette.objects.create(
    #        pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
    #        periodebudget=self.periode,
    #        naturecomptablerecette=self.naturecomptablerecette,
    #        montant_re=Decimal(5), montant_ar=Decimal(6)
    #    )
    #    recette.save()
    #    self.assertIsNotNone(recette.pk)
    #    self.assertEqual(recette.montant_dc, Decimal(6))


class ManagersTest(TestCase):

    fixtures = ['tests/periodebudgets', 'tests/structures']

    def test_active_manager(self):
        DomaineFonctionnel.objects.create(
            code='D1', label='Domaine1', label_court='Dom1', is_active=True)
        DomaineFonctionnel.objects.create(
            code='D2', label='Domaine2', label_court='Dom2', is_active=False)

        domaines = DomaineFonctionnel.active.all()
        self.assertEqual(len(domaines), 1)
        self.assertEqual(domaines[0].code, 'D1')

    def test_active_period_manager(self):
        StructureMontant.objects.create(structure_id=1, periodebudget_id=1,
                                        annee=get_current_year())
        period_budget = PeriodeBudget.objects.create(
            period_id=1, annee=get_current_year(), is_active =False)
        StructureMontant.objects.create(structure_id=1, periodebudget=period_budget,
                                        annee=get_current_year())

        montants = StructureMontant.active_period.all()
        self.assertEqual(len(montants), 1)
        self.assertEqual(montants[0].periodebudget.pk, 1)
