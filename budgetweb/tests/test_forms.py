from collections import OrderedDict
import datetime
from decimal import Decimal

from django.test import TestCase

from budgetweb.forms import DepenseForm, PlanFinancementPluriForm, RecetteForm
from budgetweb.models import (Depense, DomaineFonctionnel,
                              NatureComptableDepense, NatureComptableRecette,
                              PeriodeBudget, PlanFinancement, Recette)


class RecetteFormTest(TestCase):

    fixtures = ['tests/periodebudgets.json', 'tests/structures.json',
                'tests/planfinancements.json',
                'tests/naturecomptablerecettes.json']

    def setUp(self):
        self.periode = PeriodeBudget.objects.first()
        self.pfi = PlanFinancement.objects.get(structure__code='ECP')
        self.naturecomptable = NatureComptableRecette.objects.get(
            code_nature_comptable='9RSCS', is_fleche=self.pfi.is_fleche)
        self.natures = OrderedDict(((n.pk, n) for n in\
            NatureComptableRecette.objects.filter(
                is_fleche=self.pfi.is_fleche)))

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
            'is_dfi_member_or_admin': True,
            'natures': self.natures,
        }

        form = RecetteForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_edit_recette(self):
        recette = Recette.objects.create(
            naturecomptablerecette=self.naturecomptable, pfi=self.pfi,
            structure=self.pfi.structure, annee=self.periode.annee,
            periodebudget=self.periode, montant_ar=Decimal(1),
            montant_re=Decimal(2), montant_dc=Decimal(3)
        )
        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi_member_or_admin': True,
            'natures': self.natures,
        }

        form = RecetteForm(instance=recette, **form_kwargs)
        self.assertEqual(
            form.fields['naturecomptablerecette'].initial.pk,
            self.naturecomptable.pk
        )


class DepenseFormTest(TestCase):

    fixtures = ['tests/periodebudgets.json', 'tests/structures.json',
                'tests/domainefonctionnels.json',
                'tests/planfinancements.json',
                'tests/naturecomptabledepenses.json']

    def setUp(self):
        self.periode = PeriodeBudget.objects.first()
        self.domaine = DomaineFonctionnel.objects.first()
        self.pfi = PlanFinancement.objects.get(structure__code='ECP')
        self.naturecomptable = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi.is_fleche)
        self.natures = OrderedDict(((n.pk, n) for n in\
            NatureComptableDepense.objects.filter(
                is_fleche=self.pfi.is_fleche)))
        self.domaines = [
            (d.pk, str(d)) for d in DomaineFonctionnel.active.all()]

    def test_add_depense(self):
        post_data = {
            'annee': self.periode.annee,
            'naturecomptabledepense': self.naturecomptable.pk,
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
            'is_dfi_member_or_admin': True,
            'natures': self.natures,
            'domaines': self.domaines,
        }

        form = DepenseForm(data=post_data, **form_kwargs)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_edit_depense(self):
        depense = Depense.objects.create(
            naturecomptabledepense=self.naturecomptable, pfi=self.pfi,
            structure=self.pfi.structure, domainefonctionnel=self.domaine,
            annee=self.periode.annee, periodebudget=self.periode,
            montant_ae=Decimal(1), montant_cp=Decimal(2), montant_dc=Decimal(3)
        )
        form_kwargs = {
            'annee': self.periode.annee,
            'periodebudget': self.periode,
            'pfi': self.pfi,
            'is_dfi_member_or_admin': True,
            'natures': self.natures,
            'domaines': self.domaines
        }

        form = DepenseForm(instance=depense, **form_kwargs)
        self.assertEqual(
            form.fields['naturecomptabledepense'].initial.pk,
            self.naturecomptable.pk
        )


class PlanFinancementPluriFormTest(TestCase):

    def test_is_valid(self):
        post_data = {
            'date_debut': datetime.date(2016, 9, 1),
            'date_fin': datetime.date(2017, 8, 31),
        }
        form = PlanFinancementPluriForm(data=post_data)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_is_not_valid(self):
        from django import forms
        post_data = {
            'date_debut': datetime.date(2016, 9, 1),
            'date_fin': datetime.date(2016, 8, 31),
        }
        form = PlanFinancementPluriForm(data=post_data)
        self.assertTrue(form.is_bound)
        with self.assertRaises(forms.ValidationError) as e:
            form.is_valid()
            form.clean()
        self.assertEqual(
            e.exception.message,
            'La date de début est inférieure à la date de fin !')
