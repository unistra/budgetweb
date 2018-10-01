
from django.test import TestCase

from ..models import (DomaineFonctionnel, NatureComptableDepense,
                      NatureComptableRecette, PlanFinancement, Structure)


class DomaineFonctionnelModelTest(TestCase):

    fixtures = ['tests/domainefonctionnels']

    def test_str(self):
        domaine = DomaineFonctionnel.objects.get(pk=1)
        self.assertEqual(
            str(domaine), 'D101 - Form. Initial et continue Licence')


class StructureModelTest(TestCase):

    fixtures = ['tests/structures']

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

    fixtures = ['tests/planfinancements']

    def test_str(self):
        plan = PlanFinancement.objects.get(pk=1)
        self.assertEqual(str(plan), 'NA')


class NatureComptableDepenseModelTest(TestCase):

    fixtures = ['tests/naturecomptabledepenses']

    def test_str(self):
        nature = NatureComptableDepense.objects.get(pk=1)
        self.assertEqual(str(nature), '9DFLU - Fluides')


class NatureComptableRecetteModelTest(TestCase):

    fixtures = ['tests/naturecomptablerecettes']

    def test_str(self):
        nature = NatureComptableRecette.objects.get(pk=1)
        self.assertEqual(
            str(nature), '9RDRN - Droits de scolarité nationaux et redevances')
