import datetime
from decimal import Decimal
import json

from django.contrib.auth.models import User
from django.test import TestCase

from budgetweb.models import (Depense, DomaineFonctionnel,
                              NatureComptableDepense, NatureComptableRecette,
                              PeriodeBudget, PlanFinancement, Recette,
                              Structure)


class APIViewsTest(TestCase):

    fixtures = [
        'tests/structures.json', 'tests/planfinancements.json',
        'tests/naturecomptabledepenses.json',
        'tests/naturecomptablerecettes.json'
    ]

    def setUp(self):
        self.pfi_ecp_ecp = PlanFinancement.objects.get(
            code='NA', structure__code='ECP')

    def test_api_fund_designation_by_nature_and_enveloppe_recette(self):
        nature = 'Investissement'
        view_api = '/api/naturecomptablerecette/enveloppe/%s/%s' % (
            nature, self.pfi_ecp_ecp.pk)
        response = self.client.get(
            view_api, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
        json_response = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 7)
        self.assertDictEqual(json_response[0], {
            "id": 59,
            "label": "9RIAU - Financement d'actifs par les autres collectivités et organismes"
        })

    def test_api_fund_designation_by_nature_and_enveloppe_depense(self):
        nature = 'Personnel'
        view_api = '/api/naturecomptabledepense/enveloppe/%s/%s' % (
            nature, self.pfi_ecp_ecp.pk)
        response = self.client.get(
            view_api, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
        json_response = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 4)
        self.assertDictEqual(json_response[0], {
            "id": 50, "label": "9DCAS - Cotisation CAS"})


class ViewsTest(TestCase):

    fixtures = [
        'tests/periodebudgets.json', 'tests/structures.json',
        'tests/domainefonctionnels.json', 'tests/planfinancements.json',
        'tests/naturecomptabledepenses.json',
        'tests/naturecomptablerecettes.json'
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

    def tearDown(self):
        self.client.logout()

    def test_home(self):
        view_url = '/'
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 302)

    def test_show_tree(self):
        view_url = '/showtree/gbcp/'
        self.client.login(username='admin', password='pass')
        response = self.client.get(view_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['structures']), 1)

    def test_show_subtree(self):
        view_url = '/showtree/gbcp/ETAB/'
        self.client.login(username='admin', password='pass')
        response = self.client.get(
            view_url, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['structures']), 4)

    def test_pluriannuel(self):
        view_url = '/pluriannuel/%s/' % self.pfi_ecp.pk
        data = {
            'date_debut': datetime.date(2016, 9, 1),
            'date_fin': datetime.date(2017, 8, 31),
        }

        self.client.login(username='admin', password='pass')
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(view_url, data=data)
        pfi_ecp = PlanFinancement.objects.get(
            code='NA', structure=self.structure_ecp)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(pfi_ecp.date_debut, datetime.date(2016, 9, 1))
        self.assertEqual(pfi_ecp.date_fin, datetime.date(2017, 8, 31))

    def test_pluriannuel_several_years(self):
        view_url = '/pluriannuel/%s/' % self.pfi_ecp.pk
        self.pfi_ecp.date_debut = datetime.date(2016, 9, 1)
        self.pfi_ecp.date_fin = datetime.date(2018, 8, 31)
        self.pfi_ecp.save()

        self.client.login(username='admin', password='pass')
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['rangeYear']), 3)

    def test_depense_unauthorized(self):
        view_url = '/depense/26/2017/'
        self.client.login(username='user1', password='pass')
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 403)

    def test_depense_add_valid(self):
        # https://github.com/django/django/blob/1.8.14/tests/model_formsets/tests.py
        view_url = '/depense/26/2017/'

        naturecomptable = NatureComptableDepense.objects.get(
            code_nature_comptable='9DFLU', is_fleche=self.pfi_ecp.is_fleche)

        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-annee': self.periode.annee,
            'form-0-naturecomptabledepense': naturecomptable.pk,
            'form-0-pfi': self.pfi_ecp.pk,
            'form-0-structure': self.structure_ecp.pk,
            'form-0-domainefonctionnel': self.domaine.pk,
            'form-0-periodebudget': self.periode.pk,
            'form-0-montant_ae': Decimal(1),
            'form-0-montant_cp': Decimal(2),
            'form-0-montant_dc': Decimal(3),
            # 'form-0-DELETE': 'on'  # Deletes the entry
        }

        self.client.login(username='admin', password='pass')
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(view_url, data=data)
        depenses = Depense.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(depenses), 1)

    def test_recette_unauthorized(self):
        view_url = '/recette/26/2017/'
        self.client.login(username='user1', password='pass')
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 403)

    def test_recette_add_valid(self):
        # https://github.com/django/django/blob/1.8.14/tests/model_formsets/tests.py
        view_url = '/recette/26/2017/'

        naturecomptable = NatureComptableRecette.objects.get(
            code_nature_comptable='9RSCS', is_fleche=self.pfi_ecp.is_fleche)

        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-annee': self.periode.annee,
            'form-0-naturecomptablerecette': naturecomptable.pk,
            'form-0-pfi': self.pfi_ecp.pk,
            'form-0-structure': self.structure_ecp.pk,
            'form-0-periodebudget': self.periode.pk,
            'form-0-montant_ar': Decimal(1),
            'form-0-montant_re': Decimal(2),
            'form-0-montant_dc': Decimal(3),
            # 'form-0-DELETE': 'on'  # Deletes the entry
        }

        self.client.login(username='admin', password='pass')
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(view_url, data=data)
        recettes = Recette.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(recettes), 1)

    def test_detailspfi(self):
        view_url = '/detailspfi/%s/' % self.pfi_ecp.pk

        naturecomptabledepense = NatureComptableDepense.objects.get(pk=30)
        naturecomptablerecette = NatureComptableRecette.objects.get(pk=30)
        Depense.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=naturecomptabledepense,
            montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
        )
        Depense.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=naturecomptabledepense,
            montant_dc=Decimal(10), montant_cp=Decimal(20),
            montant_ae=Decimal(30)
        )

        Recette.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=naturecomptablerecette,
            montant_dc=Decimal(4), montant_re=Decimal(5), montant_ar=Decimal(6)
        )
        Recette.objects.create(
            pfi=self.pfi_ecp, structure=self.structure_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=naturecomptablerecette,
            montant_dc=Decimal(40), montant_re=Decimal(50),
            montant_ar=Decimal(60)
        )

        self.client.login(username='admin', password='pass')
        response = self.client.get(view_url)
        depense_sum = response.context['sommeDepense']
        recette_sum = response.context['sommeRecette']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(depense_sum['sommeDC'], Decimal(11))
        self.assertEqual(depense_sum['sommeCP'], Decimal(22))
        self.assertEqual(depense_sum['sommeAE'], Decimal(33))
        self.assertEqual(recette_sum['sommeDC'], Decimal(44))
        self.assertEqual(recette_sum['sommeRE'], Decimal(55))
        self.assertEqual(recette_sum['sommeAR'], Decimal(66))
