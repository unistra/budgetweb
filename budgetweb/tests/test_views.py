import datetime
from decimal import Decimal
import json

from django.contrib.auth.models import User
from django.test import TestCase

from budgetweb.apps.structure.models import (
    DomaineFonctionnel, NatureComptableDepense, NatureComptableRecette,
    PlanFinancement, Structure)
from budgetweb.exceptions import StructureUnauthorizedException
from budgetweb.models import Depense, PeriodeBudget, Recette


class APIViewsTest(TestCase):

    fixtures = [
        'tests/structures', 'tests/planfinancements',
        'tests/naturecomptabledepenses', 'tests/naturecomptablerecettes'
    ]

    def setUp(self):
        self.pfi_ecp = PlanFinancement.objects.get(
            code='NA', structure__code='ECP')
        self.naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi_ecp.is_fleche)
        self.naturecomptablerecette = NatureComptableRecette.objects.get(
            code_nature_comptable='9RIIA', is_fleche=self.pfi_ecp.is_fleche)

    def test_api_fund_designation_by_nature_and_enveloppe_recette(self):
        nature = 'Investissement'
        view_api = '/api/naturecomptablerecette/enveloppe/%s/%s' % (
            nature, self.pfi_ecp.pk)
        response = self.client.get(
            view_api, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
        json_response = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 7)
        self.assertDictEqual(json_response[0], {
            "id": 65,
            "label": "9RIET - Financement d'actifs par l\'Etat"
        })

    def test_api_fund_designation_by_nature_and_enveloppe_depense(self):
        nature = 'Personnel'
        view_api = '/api/naturecomptabledepense/enveloppe/%s/%s' % (
            nature, self.pfi_ecp.pk)
        response = self.client.get(
            view_api, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
        json_response = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 4)
        self.assertDictEqual(json_response[0], {
            "id": 61, "label": "9DREM - Rémunérations principales et accessoires"})

    def test_api_get_details_nature_by_code_recette(self):
        view_api = '/api/naturecomptablerecette/%s/' % (
            self.naturecomptablerecette.pk,)
        response = self.client.get(
            view_api, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
        json_response = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(json_response, {
            'code_compte_budgetaire': 'RG_ETAT',
            'label_compte_budgetaire': 'Autres financements de l\'Etat ',
            'code_fonds': 'FD070',
            'label_fonds': 'ANR investissements d\'avenir'
        })

    def test_api_get_details_nature_by_code_depense(self):
        view_api = '/api/naturecomptabledepense/%s/' % (
            self.naturecomptabledepense.pk,)
        response = self.client.get(
            view_api, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
        json_response = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(json_response, {
            'code_compte_budgetaire': 'FG',
            'label_compte_budgetaire': 'Fonctionnement Globalisé'
        })

    def test_api_get_managment_rules_depense_by_id(self):
        view_api = '/api/naturecomptabledepense/rules/%s/' % (
            self.naturecomptabledepense.pk,)
        response = self.client.get(
            view_api, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
        json_response = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(json_response, {'is_decalage_tresorerie': True,
                                             'is_non_budgetaire': False,
                                             'is_pi_cfg': False})

    def test_api_get_managment_rules_recette_by_id(self):
        view_api = '/api/naturecomptablerecette/rules/%s/' % (
            self.naturecomptablerecette.pk,)
        response = self.client.get(
            view_api, {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
        json_response = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(json_response, {'is_non_budgetaire': False,
                                             'is_ar_and_re': True})


class ViewsTest(TestCase):

    fixtures = [
        'tests/periodebudgets', 'tests/structures',
        'tests/domainefonctionnels', 'tests/planfinancements',
        'tests/naturecomptabledepenses',
        'tests/naturecomptablerecettes'
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
        view_url = '/showtree/gbcp/1/'
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
        # self.assertEqual(len(response.context['rangeYear']), 3)

    def test_depense_unauthorized(self):
        view_url = '/depense/26/2017/'
        self.client.login(username='user1', password='pass')
        self.assertRaises(
            StructureUnauthorizedException, self.client.get, view_url)

    def test_depense_add_valid(self):
        # https://github.com/django/django/blob/1.8.14/tests/model_formsets/tests.py
        view_url = '/depense/26/2017/'

        naturecomptable = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi_ecp.is_fleche)

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

    def test_depense_redirect(self):
        view_url = '/depense/26/2017/'

        today = datetime.date.today()
        PeriodeBudget.objects.update(is_active=False)
        PeriodeBudget.objects.create(
            period_id=1, annee=2018, date_debut_saisie=today,
            date_fin_saisie=today, date_debut_retardataire=today,
            date_fin_retardataire=today, date_debut_dfi=today,
            date_fin_dfi=today, date_debut_admin=today, date_fin_admin=today)

        self.client.login(username='admin', password='pass')
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 302)

    def test_recette_unauthorized(self):
        view_url = '/recette/26/2017/'
        self.client.login(username='user1', password='pass')
        self.assertRaises(
            StructureUnauthorizedException, self.client.get, view_url)

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

    def test_recette_redirect(self):
        view_url = '/recette/26/2017/'

        today = datetime.date.today()
        PeriodeBudget.objects.update(is_active=False)
        PeriodeBudget.objects.create(
            period_id=1, annee=2018, date_debut_saisie=today,
            date_fin_saisie=today, date_debut_retardataire=today,
            date_fin_retardataire=today, date_debut_dfi=today,
            date_fin_dfi=today, date_debut_admin=today, date_fin_admin=today)

        self.client.login(username='admin', password='pass')
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 302)

    def test_detailspfi(self):
        view_url = '/detailspfi/%s/' % self.pfi_ecp.pk

        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi_ecp.is_fleche)
        naturecomptablerecette = NatureComptableRecette.objects.get(
            code_nature_comptable='9RSCS', is_fleche=self.pfi_ecp.is_fleche)
        Depense.objects.create(
            pfi=self.pfi_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=naturecomptabledepense,
            montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
        )
        Depense.objects.create(
            pfi=self.pfi_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=naturecomptabledepense,
            montant_dc=Decimal(10), montant_cp=Decimal(20),
            montant_ae=Decimal(30)
        )

        Recette.objects.create(
            pfi=self.pfi_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=naturecomptablerecette,
            montant_dc=Decimal(4), montant_re=Decimal(5), montant_ar=Decimal(6)
        )
        Recette.objects.create(
            pfi=self.pfi_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=naturecomptablerecette,
            montant_dc=Decimal(40), montant_re=Decimal(50),
            montant_ar=Decimal(60)
        )

        self.client.login(username='admin', password='pass')
        response = self.client.get(view_url)
        depense_sum = response.context['sommeDepense'][self.annee][0]
        recette_sum = response.context['sommeRecette'][self.annee][0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(depense_sum['sum_dc'], Decimal(11))
        self.assertEqual(depense_sum['sum_cp'], Decimal(22))
        self.assertEqual(depense_sum['sum_ae'], Decimal(33))
        self.assertEqual(recette_sum['sum_dc'], Decimal(44))
        self.assertEqual(recette_sum['sum_re'], Decimal(55))
        self.assertEqual(recette_sum['sum_ar'], Decimal(66))

    def test_detailscf(self):
        view_url = '/detailscf/%s/' % self.structure_ecp.pk

        naturecomptabledepense = NatureComptableDepense.objects.get(
            code_nature_comptable='9DLOC', is_fleche=self.pfi_ecp.is_fleche)
        naturecomptablerecette = NatureComptableRecette.objects.get(
            code_nature_comptable='9RSCS', is_fleche=self.pfi_ecp.is_fleche)
        Depense.objects.create(
            pfi=self.pfi_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=naturecomptabledepense,
            montant_dc=Decimal(1), montant_cp=Decimal(2), montant_ae=Decimal(3)
        )
        Depense.objects.create(
            pfi=self.pfi_ecp, annee=self.annee,
            periodebudget=self.periode, domainefonctionnel=self.domaine,
            naturecomptabledepense=naturecomptabledepense,
            montant_dc=Decimal(10), montant_cp=Decimal(20),
            montant_ae=Decimal(30)
        )

        Recette.objects.create(
            pfi=self.pfi_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=naturecomptablerecette,
            montant_dc=Decimal(4), montant_re=Decimal(5), montant_ar=Decimal(6)
        )
        Recette.objects.create(
            pfi=self.pfi_ecp, annee=self.annee,
            periodebudget=self.periode,
            naturecomptablerecette=naturecomptablerecette,
            montant_dc=Decimal(40), montant_re=Decimal(50),
            montant_ar=Decimal(60)
        )

        self.client.login(username='admin', password='pass')
        response = self.client.get(view_url)
        self.assertEqual(response.status_code, 200)
