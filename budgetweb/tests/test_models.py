import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from budgetweb.models import (Depense, DomaineFonctionnel,
                              NatureComptableDepense, NatureComptableRecette,
                              PeriodeBudget, PlanFinancement, Recette,
                              Structure, StructureAuthorizations,
                              StructureMontant)


class StructureAuthorizationsModelTest(TestCase):

    fixtures = ['tests/structures.json', 'tests/structureauthorizations.json']

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


class PeriodeBudgetModelTest(TestCase):

    fixtures = ['tests/periodebudgets.json']

    def test_str(self):
        periode = PeriodeBudget.objects.get(pk=1)
        self.assertEqual(str(periode), 'BI -- Budget initial -- 2017')


class DomaineFonctionnelModelTest(TestCase):

    fixtures = ['tests/domainefonctionnels.json']

    def test_str(self):
        domaine = DomaineFonctionnel.objects.get(pk=1)
        self.assertEqual(
            str(domaine), 'D101 - Form. Initial et continue Licence')


class StructureModelTest(TestCase):

    fixtures = ['tests/structures.json']

    def setUp(self):
        """ Tree :
            ETAB
            +-- PAIE
                +-- PAIE7DIN
                +-- PAIE7ECP
            +-- SCX
        """
        self.etab = Structure.objects.get(code='ETAB')
        self.paie = Structure.objects.get(code='PAIE')
        self.paie7din = Structure.objects.get(code='PAIE7DIN')
        self.paie7ecp = Structure.objects.get(code='PAIE7ECP')
        self.scx = Structure.objects.get(code='SCX')

        # Delete the other structures
        Structure.objects.all().exclude(
            code__in=['ETAB', 'PAIE', 'PAIE7DIN', 'PAIE7ECP', 'SCX']).delete()

    def test_str(self):
        self.assertEqual(
            str(self.etab), 'ETAB - Université de Strasbourg')

    def test_save(self):
        structure = Structure.objects.create(
            groupe1='Recherche',
            code='PAIE7DIN1',
            label='Paie 7 Din 1',
            parent=self.paie7din)
        self.assertEqual(structure.depth, 4)
        self.assertEqual(
            structure.path,
            '/%s/%s/%s' % (self.etab.pk, self.paie.pk, self.paie7din.pk))

    def test_get_ancestors(self):
        self.assertListEqual(self.etab.get_ancestors(), [])
        self.assertListEqual(self.paie.get_ancestors(), [self.etab])
        self.assertListEqual(
            self.paie7din.get_ancestors(), [self.paie, self.etab])
        self.assertListEqual(
            self.paie7ecp.get_ancestors(), [self.paie, self.etab])
        self.assertListEqual(self.scx.get_ancestors(), [self.etab])

    def test_get_children(self):
        self.assertListEqual(self.etab.get_children(),
            [self.paie, self.paie7din, self.paie7ecp, self.scx])
        self.assertListEqual(
            self.paie.get_children(), [self.paie7din, self.paie7ecp])
        self.assertListEqual(self.paie7din.get_children(), [])
        self.assertListEqual(self.paie7ecp.get_children(), [])
        self.assertListEqual(self.scx.get_children(), [])

    def test_get_unordered_children(self):
        etab_children = self.etab.get_unordered_children()
        self.assertIn(self.paie, etab_children)
        self.assertIn(self.paie7din, etab_children)
        self.assertIn(self.paie7ecp, etab_children)
        self.assertIn(self.scx, etab_children)

        paie_children = self.paie.get_unordered_children()
        self.assertIn(self.paie7din, paie_children)
        self.assertIn(self.paie7ecp, paie_children)

        self.assertFalse(self.paie7din.get_unordered_children())
        self.assertFalse(self.paie7ecp.get_unordered_children())
        self.assertFalse(self.scx.get_unordered_children())

    def test_get_sons(self):
        self.assertListEqual(list(self.etab.get_sons()), [self.paie, self.scx])
        self.assertListEqual(
            list(self.paie.get_sons()), [self.paie7din, self.paie7ecp])
        self.assertEqual(self.paie7din.get_sons().count(), 0)
        self.assertEqual(self.paie7ecp.get_sons().count(), 0)
        self.assertEqual(self.scx.get_sons().count(), 0)

    def test_full_path(self):
        self.assertEqual(self.etab.full_path, '/%s' % self.etab.pk)
        self.assertEqual(
            self.paie.full_path, '/%s/%s' % (self.etab.pk, self.paie.pk))
        self.assertEqual(
            self.paie7din.full_path,
            '/%s/%s/%s' % (self.etab.pk, self.paie.pk, self.paie7din.pk))
        self.assertEqual(
            self.paie7ecp.full_path,
            '/%s/%s/%s' % (self.etab.pk, self.paie.pk, self.paie7ecp.pk))
        self.assertEqual(
            self.scx.full_path, '/%s/%s' % (self.etab.pk, self.scx.pk))

    def test_get_full_path(self):
        self.assertListEqual(self.etab.get_full_path(), [self.etab])
        self.assertListEqual(self.paie.get_full_path(), [self.etab, self.paie])
        self.assertListEqual(self.paie7din.get_full_path(),
            [self.etab, self.paie, self.paie7din])
        self.assertListEqual(self.paie7ecp.get_full_path(),
            [self.etab, self.paie, self.paie7ecp])
        self.assertListEqual(self.scx.get_full_path(), [self.etab, self.scx])


class PlanFinancementModelTest(TestCase):

    fixtures = [
        'tests/periodebudgets.json', 'tests/structures.json',
        'tests/planfinancements.json', 'tests/domainefonctionnels.json',
        'tests/naturecomptabledepenses.json',
        'tests/naturecomptablerecettes.json'
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

    def test_str(self):
        plan = PlanFinancement.objects.get(pk=1)
        self.assertEqual(str(plan), 'NA')

    def test_get_total(self):
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
        total_depense, total_recette = self.pfi_ecp.get_total()

        self.assertEqual(total_depense[0]['sum_depense_dc'], Decimal(11))
        self.assertEqual(total_depense[0]['sum_depense_cp'], Decimal(22))
        self.assertEqual(total_depense[0]['sum_depense_ae'], Decimal(33))
        self.assertEqual(total_recette[0]['sum_recette_dc'], Decimal(44))
        self.assertEqual(total_recette[0]['sum_recette_re'], Decimal(55))
        self.assertEqual(total_recette[0]['sum_recette_ar'], Decimal(66))

    def test_get_total_with_years(self):
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
        total_depense, total_recette = self.pfi_ecp.get_total(
            years=[self.annee])

        self.assertEqual(total_depense[0]['sum_depense_dc'], Decimal(1))
        self.assertEqual(total_depense[0]['sum_depense_cp'], Decimal(2))
        self.assertEqual(total_depense[0]['sum_depense_ae'], Decimal(3))
        self.assertEqual(total_recette[0]['sum_recette_dc'], Decimal(4))
        self.assertEqual(total_recette[0]['sum_recette_re'], Decimal(5))
        self.assertEqual(total_recette[0]['sum_recette_ar'], Decimal(6))

    def test_get_years(self):
        self.pfi_ecp.date_debut = datetime.date(2015, 1, 1)
        self.pfi_ecp.date_fin = datetime.date(2025, 12, 31)
        self.pfi_ecp.save()

        self.assertListEqual(
            self.pfi_ecp.get_years(), [2017, 2018, 2019, 2020, 2021])
        self.assertListEqual(
            self.pfi_ecp.get_years(year_number=2), [2017, 2018, 2019])
        self.assertListEqual(self.pfi_ecp.get_years(
            begin_current_period=False), [2015, 2016, 2017, 2018, 2019])
        self.assertListEqual(
            self.pfi_ecp.get_years(begin_current_period=False, year_number=2),
            [2015, 2016, 2017])


class NatureComptableDepenseModelTest(TestCase):

    fixtures = ['tests/naturecomptabledepenses.json']

    def test_str(self):
        nature = NatureComptableDepense.objects.get(pk=1)
        self.assertEqual(str(nature), '9DFLU - Fluides')


class NatureComptableRecetteModelTest(TestCase):

    fixtures = ['tests/naturecomptablerecettes.json']

    def test_str(self):
        nature = NatureComptableRecette.objects.get(pk=1)
        self.assertEqual(
            str(nature), '9RDRN - Droits de scolarité nationaux et redevances')


class ComptabiliteModelTest(TestCase):

    fixtures = [
        'tests/periodebudgets.json', 'tests/structures.json',
        'tests/planfinancements.json', 'tests/domainefonctionnels.json',
        'tests/naturecomptabledepenses.json',
        'tests/naturecomptablerecettes.json',
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
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=self.naturecomptabledepense,
            montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
        )
        self.recette_ecp = Recette.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=self.naturecomptablerecette,
            montant_dc=Decimal(4), montant_re=Decimal(5), montant_ar=Decimal(6)
        )
        self.depense_ecp1 = Depense(
            pfi=self.pfi_ecp1, structure=self.structure_ecp1, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=self.naturecomptabledepense,
            montant_dc=Decimal(10), montant_cp=Decimal(20),
            montant_ae=Decimal(30)
        )
        self.recette_ecp1 = Recette(
            pfi=self.pfi_ecp1, structure=self.structure_ecp1,
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
        'tests/periodebudgets.json', 'tests/structures.json',
        'tests/planfinancements.json', 'tests/domainefonctionnels.json',
        'tests/naturecomptabledepenses.json',
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
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=naturecomptabledepense,
            montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
        )
        depense.save()
        self.assertIsNotNone(depense.pk)

    def test_save_with_validation_error(self):
        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DFLU', is_fleche=self.pfi_ecp.is_fleche)
        depense = Depense(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=naturecomptabledepense,
            montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
        )

        with self.assertRaises(ValidationError) as ve:
            depense.save()
        self.assertEqual(
            ve.exception.message_dict['montant_ae'][0],
            "Le décalagage de trésorerie n'est pas possible sur cette nature "
            "comptable.")

    def test_save_without_montant_dc(self):
        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi_ecp.is_fleche)

        depense = Depense(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=naturecomptabledepense,
            montant_cp=Decimal(2), montant_ae=Decimal(3)
        )
        depense.save()
        self.assertIsNotNone(depense.pk)
        self.assertEqual(depense.montant_dc, Decimal(3))


class RecetteModelTest(TestCase):

    fixtures = [
        'tests/periodebudgets.json', 'tests/structures.json',
        'tests/planfinancements.json', 'tests/domainefonctionnels.json',
        'tests/naturecomptablerecettes.json',
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
        recette = Recette.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=self.naturecomptablerecette,
            montant_dc=Decimal(4), montant_re=Decimal(5), montant_ar=Decimal(6)
        )
        recette.save()
        self.assertIsNotNone(recette.pk)

    def test_save_without_montant_dc(self):
        recette = Recette.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=self.naturecomptablerecette,
            montant_re=Decimal(5), montant_ar=Decimal(6)
        )
        recette.save()
        self.assertIsNotNone(recette.pk)
        self.assertEqual(recette.montant_dc, Decimal(6))


class ManagersTest(TestCase):

    fixtures = ['tests/periodebudgets.json']

    def test_active_manager(self):
        DomaineFonctionnel.objects.create(
            code='D1', label='Domaine1', label_court='Dom1', is_active=True)
        DomaineFonctionnel.objects.create(
            code='D2', label='Domaine2', label_court='Dom2', is_active=False)

        domaines = DomaineFonctionnel.active.all()
        self.assertEqual(len(domaines), 1)
        self.assertEqual(domaines[0].code, 'D1')

    def test_active_period_manager(self):
        StructureMontant.objects.create(structure_id=1, periodebudget_id=1)
        StructureMontant.objects.create(structure_id=1, periodebudget_id=2)

        montants = StructureMontant.active_period.all()
        self.assertEqual(len(montants), 1)
        self.assertEqual(montants[0].periodebudget.pk, 1)
