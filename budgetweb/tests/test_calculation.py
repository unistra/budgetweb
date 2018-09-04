from decimal import Decimal
from io import StringIO
import random

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from budgetweb.apps.structure.models import (
    DomaineFonctionnel, NatureComptableDepense, NatureComptableRecette,
    PlanFinancement, Structure)
from budgetweb.models import Depense, PeriodeBudget, Recette


def get_random_object(object_list):
    obj = object_list[random.randint(0, len(object_list) - 1)]
    return obj


def generate_montant(max_montant):
    return Decimal(random.randrange(max_montant * 100)) / 100


class CalculationTest(TestCase):

    fixtures = [
        'tests/periodebudgets', 'tests/structures',
        'tests/domainefonctionnels', 'tests/planfinancements',
        'tests/naturecomptabledepenses', 'tests/naturecomptablerecettes'
    ]

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            'admin', email='admin@unistra.fr', password='pass')
        self.user1 = User.objects.create_user('user1', password='pass')

        self.periode = PeriodeBudget.objects.first()
        self.annee = self.periode.annee
        self.domaine = DomaineFonctionnel.objects.first()
        self.structure_ecp = Structure.objects.get(code='ECP')
        self.pfi_ecp = PlanFinancement.objects.get(
            code='NA', structure=self.structure_ecp)
        self.naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi_ecp.is_fleche)
        self.naturecomptablerecette = NatureComptableRecette.objects.get(
            code_nature_comptable='9RSCS', is_fleche=self.pfi_ecp.is_fleche)

        self.client.login(username='admin', password='pass')

    def tearDown(self):
        self.client.logout()

    def test_comptabilite_views(self):
        max_montant = 1000
        max_form = 50

        # Dépenses
        view_url = '/depense/%s/2017/' % self.structure_ecp.pk
        data = {
            'form-TOTAL_FORMS': str(max_form),
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
        for i in range(max_form):
            value = generate_montant(max_montant)
            data.update({
                'form-%s-annee' % i: self.annee,
                'form-%s-naturecomptabledepense' % i: self.naturecomptabledepense.pk,
                'form-%s-pfi' % i: self.pfi_ecp.pk,
                'form-%s-structure' % i: self.structure_ecp.pk,
                'form-%s-domainefonctionnel' % i: self.domaine.pk,
                'form-%s-periodebudget' % i: self.periode.pk,
                'form-%s-montant_ae' % i: value,
                'form-%s-montant_cp' % i: value,
                'form-%s-montant_dc' % i: value,
            })

        response = self.client.post(view_url, data=data)
        depenses = Depense.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(depenses), max_form)

        # Recettes
        view_url = '/recette/%s/2017/' % self.structure_ecp.pk
        data = {
            'form-TOTAL_FORMS': str(max_form),
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
        for i in range(max_form):
            value = Decimal(random.randrange(max_montant * 100)) / 100
            data.update({
                'form-%s-annee' % i: self.annee,
                'form-%s-naturecomptablerecette' % i: self.naturecomptablerecette.pk,
                'form-%s-pfi' % i: self.pfi_ecp.pk,
                'form-%s-structure' % i: self.structure_ecp.pk,
                'form-%s-periodebudget' % i: self.periode.pk,
                'form-%s-montant_ar' % i: value,
                'form-%s-montant_re' % i: value,
                'form-%s-montant_dc' % i: value,
            })

        response = self.client.post(view_url, data=data)
        recettes = Recette.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(recettes), max_form)

        # Check
        out = StringIO()
        call_command('check_structuremontants', stdout=out)
        self.assertEquals(out.getvalue().strip(), 'No calculation errors')

    def test_random_actions_on_comptabilite_models(self):
        max_montant = 1000
        insertions_number = 100
        updates_number = 50
        deletions_number = 30

        # Insertions
        for i in range(insertions_number):
            value = generate_montant(max_montant)
            depense = Depense(
                pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
                periodebudget=self.periode, domainefonctionnel=self.domaine,
                naturecomptabledepense=self.naturecomptabledepense,
                montant_dc=value, montant_cp=value, montant_ae=value
            )
            recette = Recette(
                pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
                periodebudget=self.periode,
                naturecomptablerecette=self.naturecomptablerecette,
                montant_dc=value, montant_re=value, montant_ar=value
            )
            depense.save()
            recette.save()

        # Check
        out = StringIO()
        call_command('check_structuremontants', stdout=out)
        self.assertEquals(out.getvalue().strip(), 'No calculation errors')

        # Updates
        depenses = Depense.objects.all()
        recettes = Recette.objects.all()
        for i in range(updates_number):
            value = generate_montant(max_montant)
            depense = get_random_object(depenses)
            recette = get_random_object(recettes)
            depense.montant_dc = value
            depense.montant_cp = value
            depense.montant_ae = value
            depense.save()
            recette.montant_dc = value
            recette.montant_re = value
            recette.montant_ar = value
            recette.save()

        # Check
        out = StringIO()
        call_command('check_structuremontants', stdout=out)

        # Deletions
        random_index = lambda lst: random.randint(0, len(lst) - 1)
        depenses = list(Depense.objects.all())
        recettes = list(Recette.objects.all())
        for i in range(deletions_number):
            depense = depenses.pop(random_index(depenses))
            depense.delete()
            recette = recettes.pop(random_index(recettes))
            recette.delete()

        # Check
        out = StringIO()
        call_command('check_structuremontants', stdout=out)
        self.assertEquals(out.getvalue().strip(), 'No calculation errors')
