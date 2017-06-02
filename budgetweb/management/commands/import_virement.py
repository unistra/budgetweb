from datetime import datetime
from decimal import Decimal
import json

import britney_utils
from britney.middleware import auth
from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.db import transaction

from budgetweb.apps.structure.models import Structure
from budgetweb.models import (
    Depense, DomaineFonctionnel, NatureComptableDepense,
    NatureComptableRecette, PeriodeBudget, PlanFinancement, Recette, Virement)
from budgetweb.utils import get_current_year


class CreationVirementException(BaseException):
    pass


class Command(NoArgsCommand):

    list_pfi_error = []
    list_cf_error = []

    def handle_noargs(self, **options):
        client = britney_utils.get_client(
            'test',
            settings.SIFACWS_DESC,
            middlewares=(
               (auth.ApiKey, {
                   'key_name': 'Authorization',
                   'key_value': 'Token %s' % settings.SIFACWS_APIKEY
               }),
            ),
            base_url=settings.SIFACWS_URL,
        )
        params = {'format': 'json'}
        ct = client.list_transfers(creation_date='20170101', **params)
        data = json.loads(ct.content.decode('utf-8'))

        # Traitement des résultats un par un.
        for virement_info in data:
            # try:
            vir_header = virement_info['header']
            vir_item_data = virement_info['item_data']
            vir_sender = virement_info['sender_item_date']

            doc_number = vir_header['DOCUMENT']

            datestring = vir_header['CRTDATE'] + " " + vir_header['CRTTIME'] +\
                                                 " +0200"
            if vir_header['PROCESS'] != 'TRAN':
                print('Le process du virement (%s) ne match pas (%s)'
                      % (doc_number, vir_header['PROCESS']))
                continue

            if vir_header['VERSION'] != '000':
                print('Le process du virement (%s) ne match pas (%s)'
                      % (doc_number, vir_header['VERSION']))
                continue

            vir_date = datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S %z')
            vir = 0

            with transaction.atomic():
                try:
                    # Creation du virement.
                    if not Virement.objects.filter(
                            document_number=doc_number).count():
                        print("Création du Virement %s" % doc_number)
                        vir = Virement.objects.create(
                            document_number=doc_number,
                            document_type=vir_header['DOCTYPE'],
                            version=vir_header['VERSION'],
                            perimetre=vir_header['FM_AREA'],
                            process=vir_header['PROCESS'],
                            creator_login=vir_header['CRTUSER'],
                            creation_date=vir_date,
                            value_date=vir_header['DOCDATE'])

                        for item_data in vir_item_data:
                            self.parseItemData(item_data, vir,
                                               "receiver", vir_date)

                        for item_data in vir_sender:
                            self.parseItemData(item_data, vir,
                                               "sender", vir_date)

                    else:
                        print("Le virement %s docnumber existe déjà."
                              % (doc_number))
                except CreationVirementException:
                    if vir:
                        print("Suppression du virement en erreur %s"
                              % vir.document_number)
                        vir.delete()
        print('Missing Structure : %s' % (', '.join(set(self.list_cf_error))))
        print('Missing PFI : %s' % (', '.join(set(self.list_pfi_error))))

    def parseItemData(self, item_data, virement, type, vir_date):
        cf_code = item_data['FUNDS_CTR']
        pfi_code = item_data['MEASURE']
        try:
            cf = Structure.objects.get(code=cf_code)
            pfi = PlanFinancement.objects.get(code=pfi_code, structure=cf)
            period = PeriodeBudget.objects.get(
                annee=get_current_year(),
                period__code__startswith="VIR")
        except (Structure.DoesNotExist,
                Structure.MultipleObjectsReturned) as e:
            print("Something wrong with CF %s (%s)" % (cf_code, e))
            self.list_cf_error.append(cf_code)
            raise CreationVirementException()
        except (PlanFinancement.DoesNotExist,
                PlanFinancement.MultipleObjectsReturned) as e:
            print("Something wrong with PFI %s on CF %s (%s)" % (pfi_code,
                  cf_code, e))
            self.list_pfi_error.append(pfi_code)
            raise CreationVirementException()
        except (PeriodeBudget.DoesNotExist,
                PeriodeBudget.MultipleObjectsReturned) as e:
            print("Something wrong with Periode %s (%s)" % (
                get_current_year(), e))
            raise CreationVirementException()

        type_budget = item_data['BUDCAT']

        # Virement Depense
        if item_data['CTEM_CATEGORY'] == '3':
            # On est en dépense.
            montant_ae = montant_cp = montant_dc = Decimal('0.00')
            montant = round(item_data['TOTAL_AMOUNT_TCUR'], 2)
            if type == "sender":
                if montant < 0:
                    montant = montant * -1
                else:
                    montant = montant * -1


            if type_budget == '9F':
                montant_dc = montant_cp = Decimal(montant)
            if type_budget == '9G':
                montant_ae = Decimal(montant)

            code_compte_budgetaire = item_data['CMMT_ITEM']
            try:
                naturecomptabledep = NatureComptableDepense.active.get(
                                code_compte_budgetaire=code_compte_budgetaire)
                domaine = DomaineFonctionnel.active.get(
                                code=item_data['FUNC_AREA'])
            except (NatureComptableDepense.DoesNotExist,
                    NatureComptableDepense.MultipleObjectsReturned) as e:
                print("Something wrong with NCD %s (%s)" % (
                    code_compte_budgetaire, e))
                raise CreationVirementException()
            except (DomaineFonctionnel.DoesNotExist,
                    DomaineFonctionnel.MultipleObjectsReturned) as e:
                print("Something wrong with DF %s (%s)" % (
                    item_data['FUNC_AREA'], e))
                raise CreationVirementException()

            commentaire = "%s (%s)" % (
                item_data['ITEM_TEXT'], virement.document_number)
            fonds = item_data['FUND']
            dep = Depense.objects.create(
                structure=cf, pfi=pfi, periodebudget=period,
                naturecomptabledepense=naturecomptabledep,
                domainefonctionnel=domaine, annee=period.annee, fonds=fonds,
                montant_ae=montant_ae, montant_cp=montant_cp,
                montant_dc=montant_dc, commentaire=commentaire,
                virement=virement)

            return True

        # Virement Recette
        if item_data['CTEM_CATEGORY'] == '2':
            montant_ar = montant_re = montant_dc = Decimal('0.00')
            montant = round(item_data['TOTAL_AMOUNT_TCUR'], 2)
            if type == "sender":
                if montant < 0:
                    montant = montant * -1
                else:
                    montant = montant * -1

            if type_budget == '9F':
                montant_dc = montant_re = Decimal(montant)
            if type_budget == '9G':
                montant_ar = Decimal(montant)

            code_compte_budgetaire = item_data['CMMT_ITEM']
            try:
                naturecomptablerecette = NatureComptableRecette.active.get(
                                code_compte_budgetaire=code_compte_budgetaire)
            except (NatureComptableRecette.DoesNotExist,
                    NatureComptableRecette.MultipleObjectsReturned) as e:
                print("Something wrong with NCR %s (%s)" % (
                      code_compte_budgetaire, e))
                raise CreationVirementException()

            commentaire = "%s (%s)" % (
                item_data['ITEM_TEXT'], virement.document_number)
            fonds = item_data['FUND']
            rec = Recette.objects.create(
                structure=cf, pfi=pfi, periodebudget=period,
                naturecomptablerecette=naturecomptablerecette,
                annee=period.annee,
                montant_ar=montant_ar, montant_re=montant_re,
                montant_dc=montant_dc, commentaire=commentaire,
                virement=virement)

            return True
