import datetime
from decimal import Decimal

from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from budgetweb.apps.structure.models import (
    DomaineFonctionnel, NatureComptableDepense, NatureComptableRecette,
    PlanFinancement)
from budgetweb.forms import DepenseForm, PlanFinancementPluriForm, RecetteForm
from budgetweb.models import Depense, PeriodeBudget, Recette


class RecetteFormTest(TestCase):

    fixtures = ['tests/periodebudgets', 'tests/structures',
                'tests/planfinancements', 'tests/naturecomptablerecettes']

    def setUp(self):
        self.periode = PeriodeBudget.objects.first()
        self.pfi = PlanFinancement.objects.get(structure__code='ECP')
        self.naturecomptable = NatureComptableRecette.objects.get(
            code_nature_comptable='9RSCS', is_fleche=self.pfi.is_fleche)
        self.natures = {n.pk: n for n in NatureComptableRecette.objects
                        .filter(is_fleche=self.pfi.is_fleche)}
        self.user1 = User.objects.create_user('user1')

    def test_add_recette(self):
        post_data = {
            'annee': self.periode.annee,
            'naturecomptablerecette': self.naturecomptable.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'periodebudget': self.periode.pk,
            'montant_ar': Decimal(1),
            'montant_re': Decimal(2),
            'montant_dc': Decimal(3),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': True,
            'natures': self.natures,
            'user': self.user1
        }

        form = RecetteForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

        recette = form.save()
        self.assertIsNotNone(recette)
        self.assertEqual(recette.creepar, 'user1')
        self.assertEqual(recette.modifiepar, 'user1')

    def test_add_recette_admin_ar_and_re(self):
        naturecomptable = NatureComptableRecette.objects.get(
            code_nature_comptable='9RDRN', is_fleche=self.pfi.is_fleche)
        post_data = {
            'annee': self.periode.annee,
            'naturecomptablerecette': naturecomptable.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'periodebudget': self.periode.pk,
            'montant_ar': Decimal(1),
            'montant_re': Decimal(2),
            'montant_dc': Decimal(3),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': True,
            'natures': self.natures,
            'user': self.user1
        }

        form = RecetteForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

        recette = form.save()
        self.assertIsNotNone(recette)
        self.assertEqual(recette.creepar, 'user1')
        self.assertEqual(recette.modifiepar, 'user1')

    def test_add_recette_no_admin_ar_and_re(self):
        naturecomptable = NatureComptableRecette.objects.get(
            code_nature_comptable='9RDRN', is_fleche=self.pfi.is_fleche)
        post_data = {
            'annee': self.periode.annee,
            'naturecomptablerecette': naturecomptable.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'periodebudget': self.periode.pk,
            'montant_ar': Decimal(1),
            'montant_re': Decimal(2),
            'montant_dc': Decimal(3),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'user': self.user1
        }

        form = RecetteForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        with self.assertRaises(forms.ValidationError) as e:
            form.is_valid()
            form.clean()
        self.assertRegexpMatches(
            e.exception.message,
            'Le montant AR et RE ne peuvent pas être différent')

    def test_add_recette_no_admin_non_budgetaire_ae_not_null(self):
        naturecomptable = NatureComptableRecette.objects.get(
            code_nature_comptable='9RCFG', is_fleche=self.pfi.is_fleche)
        post_data = {
            'annee': self.periode.annee,
            'naturecomptablerecette': naturecomptable.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'periodebudget': self.periode.pk,
            'montant_ar': Decimal(1),
            'montant_re': Decimal(2),
            'montant_dc': Decimal(3),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'user': self.user1
        }

        form = RecetteForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        with self.assertRaises(forms.ValidationError) as e:
            form.is_valid()
            form.clean()
        self.assertRegexpMatches(
            e.exception.message,
            'Le montant AR ne peut être différent de 0')

    def test_add_recette_no_admin_non_budgetaire_ar_not_null(self):
        naturecomptable = NatureComptableRecette.objects.get(
            code_nature_comptable='9RCFG', is_fleche=self.pfi.is_fleche)
        post_data = {
            'annee': self.periode.annee,
            'naturecomptablerecette': naturecomptable.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'periodebudget': self.periode.pk,
            'montant_ar': Decimal(0),
            'montant_re': Decimal(2),
            'montant_dc': Decimal(3),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'user': self.user1
        }

        form = RecetteForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        with self.assertRaises(forms.ValidationError) as e:
            form.is_valid()
            form.clean()
        self.assertRegexpMatches(
            e.exception.message,
            'Le montant RE ne peut être différent de 0')

    def test_add_recette_no_admin_non_budgetaire_ok(self):
        naturecomptable = NatureComptableRecette.objects.get(
            code_nature_comptable='9RCFG', is_fleche=self.pfi.is_fleche)
        post_data = {
            'annee': self.periode.annee,
            'naturecomptablerecette': naturecomptable.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'periodebudget': self.periode.pk,
            'montant_ar': Decimal(0),
            'montant_re': Decimal(0),
            'montant_dc': Decimal(3),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'user': self.user1
        }

        form = RecetteForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

        recette = form.save()
        self.assertIsNotNone(recette)
        self.assertEqual(recette.creepar, 'user1')
        self.assertEqual(recette.modifiepar, 'user1')

    def test_add_recette_no_admin_without_naturecomptable(self):
        post_data = {
            'annee': self.periode.annee,
            'pfi': self.pfi.pk,
            'enveloppe': 'Fonctionnement',
            'naturecomptablerecette': list(self.natures.keys())[0],
            'structure': self.pfi.structure.pk,
            'periodebudget': self.periode.pk,
            'montant_ae': Decimal(20),
            'montant_cp': Decimal(20),
            'montant_dc': Decimal(10),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'user': self.user1
        }

        form = RecetteForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_add_recette_admin_without_naturecomptable(self):
        post_data = {
            'annee': self.periode.annee,
            'pfi': self.pfi.pk,
            'enveloppe': 'Fonctionnement',
            'naturecomptablerecette': list(self.natures.keys())[0],
            'structure': self.pfi.structure.pk,
            'periodebudget': self.periode.pk,
            'montant_ae': Decimal(20),
            'montant_cp': Decimal(20),
            'montant_dc': Decimal(10),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': True,
            'natures': self.natures,
            'user': self.user1
        }

        form = RecetteForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_edit_recette(self):
        recette = Recette.objects.create(
            naturecomptablerecette=self.naturecomptable, pfi=self.pfi,
            annee=self.periode.annee,
            periodebudget=self.periode, montant_ar=Decimal(1),
            montant_re=Decimal(2), montant_dc=Decimal(3), creepar='user2'
        )
        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': True,
            'natures': self.natures,
            'user': self.user1
        }

        form = RecetteForm(instance=recette, **form_kwargs)
        self.assertEqual(
            form.fields['naturecomptablerecette'].initial.pk,
            self.naturecomptable.pk
        )

        recette = form.save()
        self.assertIsNotNone(recette)
        self.assertEqual(recette.creepar, 'user2')
        self.assertEqual(recette.modifiepar, 'user1')

    def test_edit_recette_no_admin_ar_re(self):
        naturecomptable = NatureComptableRecette.objects.get(
            code_nature_comptable='9RCFG', is_fleche=self.pfi.is_fleche)
        recette = Recette.objects.create(
            naturecomptablerecette=self.naturecomptable, pfi=self.pfi,
            annee=self.periode.annee,
            periodebudget=self.periode, montant_ar=Decimal(10),
            montant_re=Decimal(10), montant_dc=Decimal(30), creepar='user2'
        )
        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'user': self.user1
        }

        form = RecetteForm(instance=recette, **form_kwargs)
        self.assertEqual(
            form.fields['naturecomptablerecette'].initial.pk,
            self.naturecomptable.pk
        )

        recette = form.save()
        self.assertIsNotNone(recette)
        self.assertEqual(recette.creepar, 'user2')
        self.assertEqual(recette.modifiepar, 'user1')

    def test_edit_recette_no_admin_budgetaire(self):
        naturecomptable = NatureComptableRecette.objects.get(
            code_nature_comptable='9RCFG', is_fleche=self.pfi.is_fleche)
        recette = Recette.objects.create(
            naturecomptablerecette=naturecomptable, pfi=self.pfi,
            annee=self.periode.annee,
            periodebudget=self.periode, montant_ar=Decimal(10),
            montant_re=Decimal(10), montant_dc=Decimal(30), creepar='user2'
        )
        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'user': self.user1
        }

        form = RecetteForm(instance=recette, **form_kwargs)
        self.assertEqual(
            form.fields['naturecomptablerecette'].initial.pk,
            naturecomptable.pk
        )

        recette = form.save()
        self.assertIsNotNone(recette)
        self.assertEqual(recette.creepar, 'user2')
        self.assertEqual(recette.modifiepar, 'user1')


class DepenseFormTest(TestCase):

    fixtures = ['tests/periodebudgets', 'tests/structures',
                'tests/domainefonctionnels', 'tests/planfinancements',
                'tests/naturecomptabledepenses']

    def setUp(self):
        self.periode = PeriodeBudget.objects.first()
        self.domaine = DomaineFonctionnel.objects.first()
        self.pfi = PlanFinancement.objects.get(structure__code='ECP')
        # 9DLOC : Décalage trésorerie
        # 9DAMO : Non budgétaire
        # 9DCFG : PI CFG
        self.liste_nature_code = ['9DLOC', '9DAMO', '9DCFG']
        self.natures = {n.pk: n for n in NatureComptableDepense.objects
                        .filter(is_fleche=self.pfi.is_fleche)}
        self.domaines = [
            (d.pk, str(d)) for d in DomaineFonctionnel.active.all()]
        self.user1 = User.objects.create_user('user1')

    def test_add_depense(self):
        for code_nature in self.liste_nature_code:
            naturecomptabledepense = NatureComptableDepense.objects.get(
                code_nature_comptable=code_nature,
                is_fleche=self.pfi.is_fleche)
            for is_admin_or_not in [True, False]:
                form = self.add_depense(naturecomptabledepense,
                                        is_admin_or_not)
                self.assertTrue(form.is_bound)
                if code_nature == '9DLOC' and not is_admin_or_not:
                    with self.assertRaises(forms.ValidationError) as e:
                        form.is_valid()
                        form.clean()
                        self.assertRegexpMatches(
                            e.exception.message,
                            'Le montant CP et DC ne peuvent pas être')
                elif code_nature == '9DAMO' and not is_admin_or_not:
                    with self.assertRaises(forms.ValidationError) as e:
                        form.is_valid()
                        form.clean()
                    self.assertRegexpMatches(
                        e.exception.message,
                        'Le montant AE ne peut être différent de 0')
                elif code_nature == '9DCFG' and not is_admin_or_not:
                    with self.assertRaises(forms.ValidationError) as e:
                        form.is_valid()
                        form.clean()
                    self.assertRegexpMatches(
                        e.exception.message,
                        'Le montant CP ne peut être différent de 0')
                else:
                    self.assertTrue(form.is_bound)
                    self.assertTrue(form.is_valid())
                    depense = form.save()
                    self.assertIsNotNone(depense)
                    self.assertEqual(depense.creepar, 'user1')
                    self.assertEqual(depense.modifiepar, 'user1')

    def add_depense(self, naturecomptabledepense, is_admin_or_not):
        post_data = {
            'annee': self.periode.annee,
            'naturecomptabledepense': naturecomptabledepense.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'domainefonctionnel': self.domaine.pk,
            'periodebudget': self.periode.pk,
            'montant_ae': Decimal(1),
            'montant_cp': Decimal(2),
            'montant_dc': Decimal(3),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': is_admin_or_not,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(data=post_data, **form_kwargs)
        return form

    def test_add_depense_all_no_with_error_ae_cp(self):
        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DTAX',
            is_fleche=self.pfi.is_fleche)
        post_data = {
            'annee': self.periode.annee,
            'naturecomptabledepense': naturecomptabledepense.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'domainefonctionnel': self.domaine.pk,
            'periodebudget': self.periode.pk,
            'montant_ae': Decimal(10),
            'montant_cp': Decimal(20),
            'montant_dc': Decimal(10),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        with self.assertRaises(forms.ValidationError) as e:
            form.is_valid()
            form.clean()
        self.assertRegexpMatches(
            e.exception.message,
            'Le montant AE et CP ne peuvent pas être différent')

    def test_add_depense_all_no_with_error_cp_dc(self):
        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DTAX',
            is_fleche=self.pfi.is_fleche)
        post_data = {
            'annee': self.periode.annee,
            'naturecomptabledepense': naturecomptabledepense.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'domainefonctionnel': self.domaine.pk,
            'periodebudget': self.periode.pk,
            'montant_ae': Decimal(20),
            'montant_cp': Decimal(20),
            'montant_dc': Decimal(10),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        with self.assertRaises(forms.ValidationError) as e:
            form.is_valid()
            form.clean()
        self.assertRegexpMatches(
            e.exception.message,
            'Le montant CP et DC ne peuvent pas être différent')

    def test_add_depense_all_without_error_ae_cp_dc(self):
        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DTAX',
            is_fleche=self.pfi.is_fleche)
        post_data = {
            'annee': self.periode.annee,
            'naturecomptabledepense': naturecomptabledepense.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'domainefonctionnel': self.domaine.pk,
            'periodebudget': self.periode.pk,
            'montant_ae': Decimal(20),
            'montant_cp': Decimal(20),
            'montant_dc': Decimal(20),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        depense = form.save()
        self.assertIsNotNone(depense)
        self.assertEqual(depense.creepar, 'user1')
        self.assertEqual(depense.modifiepar, 'user1')

    def test_add_depense_pi_cfg_ae_dc(self):
        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DCFG',
            is_fleche=self.pfi.is_fleche)
        post_data = {
            'annee': self.periode.annee,
            'naturecomptabledepense': naturecomptabledepense.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'domainefonctionnel': self.domaine.pk,
            'periodebudget': self.periode.pk,
            'montant_ae': Decimal(10),
            'montant_cp': Decimal(0),
            'montant_dc': Decimal(20),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        with self.assertRaises(forms.ValidationError) as e:
            form.is_valid()
            form.clean()
        self.assertRegexpMatches(
            e.exception.message,
            'Le montant AE doit être identique au montant DC')

    def test_add_depense_non_budgetaire_cp_not_null(self):
        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DAMO',
            is_fleche=self.pfi.is_fleche)
        post_data = {
            'annee': self.periode.annee,
            'naturecomptabledepense': naturecomptabledepense.pk,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'domainefonctionnel': self.domaine.pk,
            'periodebudget': self.periode.pk,
            'montant_ae': Decimal(0),
            'montant_cp': Decimal(10),
            'montant_dc': Decimal(20),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        with self.assertRaises(forms.ValidationError) as e:
            form.is_valid()
            form.clean()
        self.assertRegexpMatches(
            e.exception.message,
            'Le montant CP ne peut être différent de 0')

    def test_add_depense_no_admin_without_naturecomptable(self):
        post_data = {
            'annee': self.periode.annee,
            'pfi': self.pfi.pk,
            'enveloppe': 'Fonctionnement',
            'naturecomptabledepense': list(self.natures.keys())[0],
            'structure': self.pfi.structure.pk,
            'domainefonctionnel': self.domaine.pk,
            'periodebudget': self.periode.pk,
            'montant_ae': Decimal(20),
            'montant_cp': Decimal(20),
            'montant_dc': Decimal(10),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_add_depense_admin_without_naturecomptable(self):
        post_data = {
            'annee': self.periode.annee,
            'pfi': self.pfi.pk,
            'structure': self.pfi.structure.pk,
            'enveloppe': 'Fonctionnement',
            'naturecomptabledepense': list(self.natures.keys())[0],
            'domainefonctionnel': self.domaine.pk,
            'periodebudget': self.periode.pk,
            'montant_ae': Decimal(20),
            'montant_cp': Decimal(20),
            'montant_dc': Decimal(10),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': True,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_edit_depense(self):
        for code_nature in self.liste_nature_code:
            naturecomptabledepense = NatureComptableDepense.objects.get(
                code_nature_comptable=code_nature,
                is_fleche=self.pfi.is_fleche)
            self.edit_depense(naturecomptabledepense)

    def edit_depense(self, naturecomptabledepense):
        depense = Depense.objects.create(
            naturecomptabledepense=naturecomptabledepense, pfi=self.pfi,
            domainefonctionnel=self.domaine,
            annee=self.periode.annee, periodebudget=self.periode,
            montant_ae=Decimal(1), montant_cp=Decimal(2),
            montant_dc=Decimal(3), creepar='user2'
        )
        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': True,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(instance=depense, **form_kwargs)
        self.assertEqual(
            form.fields['naturecomptabledepense'].initial.pk,
            naturecomptabledepense.pk
        )

        depense = form.save()
        self.assertIsNotNone(depense)
        self.assertEqual(depense.creepar, 'user2')
        self.assertEqual(depense.modifiepar, 'user1')

    def test_edit_depense_decalage_treso(self):
        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC',
            is_fleche=self.pfi.is_fleche)
        depense = Depense.objects.create(
            naturecomptabledepense=naturecomptabledepense, pfi=self.pfi,
            domainefonctionnel=self.domaine,
            annee=self.periode.annee, periodebudget=self.periode,
            montant_ae=Decimal(1), montant_cp=Decimal(2),
            montant_dc=Decimal(3), creepar='user2'
        )
        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(instance=depense, **form_kwargs)
        self.assertEqual(
            form.fields['naturecomptabledepense'].initial.pk,
            naturecomptabledepense.pk
        )

        depense = form.save()
        self.assertIsNotNone(depense)
        self.assertEqual(depense.creepar, 'user2')
        self.assertEqual(depense.modifiepar, 'user1')

    def test_edit_depense_not_decalage_treso(self):
        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DCFG',
            is_fleche=self.pfi.is_fleche)
        depense = Depense.objects.create(
            naturecomptabledepense=naturecomptabledepense, pfi=self.pfi,
            domainefonctionnel=self.domaine,
            annee=self.periode.annee, periodebudget=self.periode,
            montant_ae=Decimal(20), montant_cp=Decimal(20),
            montant_dc=Decimal(0), creepar='user2'
        )
        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': False,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(instance=depense, **form_kwargs)
        self.assertEqual(
            form.fields['naturecomptabledepense'].initial.pk,
            naturecomptabledepense.pk
        )

        depense = form.save()
        self.assertIsNotNone(depense)
        self.assertEqual(depense.creepar, 'user2')
        self.assertEqual(depense.modifiepar, 'user1')

    def test_depense_without_naturecomptable_with_enveloppe(self):
        post_data = {
            'annee': self.periode.annee,
            'pfi': self.pfi.pk,
            'naturecomptabledepense': list(self.natures.keys())[0],
            'enveloppe': 'Fonctionnement',
            'structure': self.pfi.structure.pk,
            'domainefonctionnel': self.domaine.pk,
            'periodebudget': self.periode.pk,
            'montant_ae': Decimal(0),
            'montant_cp': Decimal(0),
            'montant_dc': Decimal(0),
        }

        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi': True,
            'natures': self.natures,
            'domaines': self.domaines,
            'user': self.user1
        }

        form = DepenseForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        form.is_valid()
        form.clean()


class PlanFinancementPluriFormTest(TestCase):

    fixtures = [
        'tests/periodebudgets', 'tests/structures', 'tests/planfinancements',
        'tests/domainefonctionnels', 'tests/naturecomptabledepenses',
    ]

    def test_is_valid(self):
        post_data = {
            'date_debut': datetime.date(2016, 9, 1),
            'date_fin': datetime.date(2017, 8, 31),
        }
        form = PlanFinancementPluriForm(data=post_data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_is_not_valid_earlier_date_error(self):
        post_data = {
            'date_debut': datetime.date(2016, 9, 1),
            'date_fin': datetime.date(2016, 8, 31),
        }
        form = PlanFinancementPluriForm(data=post_data)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['__all__'][0],
            'La date de début est inférieure à la date de fin !')

    def test_is_not_valid_alreay_existing_entries_error(self):
        periode = PeriodeBudget.objects.first()
        pfi_pluriannuel = PlanFinancement.objects.get(code='SA5ECP01')
        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=pfi_pluriannuel.is_fleche)
        domaine = DomaineFonctionnel.objects.get(pk=1)
        Depense.objects.create(
            pfi=pfi_pluriannuel,
            annee=periode.annee, periodebudget=periode,
            domainefonctionnel=domaine,
            naturecomptabledepense=naturecomptabledepense,
            montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
        )
        post_data = {
            'date_debut': datetime.date(2018, 1, 1),
            'date_fin': datetime.date(2019, 12, 31),
        }
        form = PlanFinancementPluriForm(data=post_data,
                                        instance=pfi_pluriannuel)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['__all__'][0],
            _('There are already entries which are not in the new period'))
