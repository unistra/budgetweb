import json
import django

from django.db import IntegrityError, transaction
from django.utils.dateparse import parse_datetime
from britney.middleware import auth

from budgetweb.models import *
from budgetweb.utils import get_current_year

from datetime import datetime
from decimal import Decimal

import britney_utils
django.setup()

list_pfi_error = []
list_cf_error = []


class CreationVirementException(BaseException):
    pass


def parseItemData(item_data, virement, type):
    cf_code = item_data['FUNDS_CTR']
    try:
        cf = Structure.objects.get(code=cf_code)
    except (Structure.DoesNotExist, Structure.MultipleObjectsReturned) as e:
        print("Something wrong with CF %s (%s)" % (cf_code, e))
        list_cf_error.append(cf_code)
        raise CreationVirementException()

    pfi_code = item_data['MEASURE']
    try:
        pfi = PlanFinancement.objects.get(code=pfi_code, structure=cf)
    except (PlanFinancement.DoesNotExist,
            PlanFinancement.MultipleObjectsReturned) as e:
        print("Something wrong with PFI %s on CF %s (%s)" % (pfi_code,
              cf_code, e))
        list_pfi_error.append(pfi_code)
        raise CreationVirementException()

    try:
        period = PeriodeBudget.activevirement.get(annee=get_current_year())
    except (PeriodeBudget.DoesNotExist,
            PeriodeBudget.MultipleObjectsReturned) as e:
        print("Something wrong with Periode %s (%s)", get_current_year(), e)
        raise CreationVirementException()

    type_budget = item_data['BUDCAT']

    if item_data['CTEM_CATEGORY'] == '3':
        # On est en dépense.
        montant_ae = montant_cp = montant_dc = Decimal('0.00')
        montant = abs(item_data['TOTAL_AMOUNT_LCUR'])
        if type == "sender":
            montant = montant * -1

        if type_budget == '9F':
            montant_cp = Decimal(montant)
        if type_budget == '9G':
            montant_ae = Decimal(montant)

        code_compte_budgetaire = item_data['CMMT_ITEM']
        try:
            naturecomptabledep = NatureComptableDepense.active.get(
                            code_compte_budgetaire=code_compte_budgetaire)
        except (NatureComptableDepense.DoesNotExist,
                NatureComptableDepense.MultipleObjectsReturned) as e:
            print("Something wrong with NCD %s (%s)",
                  code_compte_budgetaire, e)
            raise CreationVirementException()

        try:
            domaine = DomaineFonctionnel.active.get(
                                            code=item_data['FUNC_AREA'])
        except (DomaineFonctionnel.DoesNotExist,
                DomaineFonctionnel.MultipleObjectsReturned) as e:
            print("Something wrong with DF %s (%s)", item_data['FUNC_AREA'], e)
            raise CreationVirementException()

        commentaire = item_data['ITEM_TEXT'] + " (%s)" % vir.document_number
        fonds = item_data['FUND']
        dep = Depense.objects.create(
            structure=cf, pfi=pfi, periodebudget=period,
            naturecomptabledepense=naturecomptabledep,
            domainefonctionnel=domaine, annee=period.annee, fonds=fonds,
            montant_ae=montant_ae, montant_cp=montant_cp,
            montant_dc=montant_dc, commentaire=commentaire, virement=vir)

        return True

    if item_data['CTEM_CATEGORY'] == '2':
        montant_ar = montant_re = montant_dc = Decimal('0.00')
        montant = abs(item_data['TOTAL_AMOUNT_LCUR'])
        if type == "sender":
            montant = montant * -1

        if type_budget == '9F':
            montant_re = Decimal(montant)
        if type_budget == '9G':
            montant_ar = Decimal(montant)

        code_compte_budgetaire = item_data['CMMT_ITEM']
        try:
            naturecomptablerecette = NatureComptableRecette.active.get(
                            code_compte_budgetaire=code_compte_budgetaire)
        except (NatureComptableRecette.DoesNotExist,
                NatureComptableRecette.MultipleObjectsReturned) as e:
            print("Something wrong with NCR %s (%s)",
                  code_compte_budgetaire, e)
            raise CreationVirementException()

        commentaire = item_data['ITEM_TEXT'] + " (%s)" % vir.document_number
        fonds = item_data['FUND']
        rec = Recette.objects.create(
            structure=cf, pfi=pfi, periodebudget=period,
            naturecomptablerecette=naturecomptablerecette,
            annee=period.annee,
            montant_ar=montant_ar, montant_re=montant_re,
            montant_dc=montant_dc, commentaire=commentaire, virement=vir)

        return True


if __name__ == '__main__':
    client = britney_utils.get_client(
        'test',
        'https://rest-api-test.u-strasbg.fr/sifacws/description.json',
        middlewares=(
           (auth.ApiKey, {
               'key_name': 'Authorization',
               'key_value': 'Token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
           }),
        ),
        base_url='https://sifacws-test.u-strasbg.fr/',
    )
    params = {'format': 'json'}
    ct = client.list_transfers(creation_date='20170101', **params)
    data = json.loads(ct.content.decode('utf-8'))
    # print('RESULT : {}'.format(data))

    # Traitement des résultats un par un.
    for virement_info in data:
        # try:
        vir_header = virement_info['header']
        vir_item_data = virement_info['item_data']
        vir_sender = virement_info['sender_item_date']

        doc_number = vir_header['DOCUMENT']
        datestring = vir_header['CRTDATE'] + " " + vir_header['CRTTIME'] + \
                                             " +0200"
        vir_date = datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S %z')
        vir = 0

        with transaction.atomic():
            try:
                # Creation du virement.
                if not Virement.objects.filter(
                                        document_number=doc_number).count():
                    print("Création du Virement %s", doc_number)
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
                        parseItemData(item_data, vir, "receiver")

                    for item_data in vir_sender:
                        parseItemData(item_data, vir, "sender")

                else:
                    print("Le virement %s docnumber existe déjà."
                          % (doc_number))
            except CreationVirementException:
                if vir:
                    print("Suppression du virement en erreur %s"
                          % vir.document_number)
                    vir.delete()
    print('Missing Structure : %s' % (', '.join(list_cf_error)))
    print('Missing PFI : %s' % (', '.join(list_pfi_error)))
