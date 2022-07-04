from datetime import datetime
from decimal import Decimal
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from budgetweb.apps.structure.models import (
    DomaineFonctionnel, Structure, PlanFinancement,
    NatureComptableDepense, NatureComptableRecette)
from budgetweb.models import (Depense, PeriodeBudget, Recette, Virement)
from budgetweb.utils import get_current_year


VIR_DATETIME_FORMATS = (
    '%Y-%m-%d %H:%M:%S',
    '%Y%m%d %H%M%S',
)

VIR_DATE_FORMATS = (
    '%Y-%m-%d',
    '%Y%m%d',
)


def vir_date_format(datestring, formats):
    for format_ in formats:
        try:
            return datetime.strptime(datestring, format_)
        except ValueError:
            continue


class CreationVirementException(BaseException):
    pass


class Command(BaseCommand):

    list_pfi_error = []
    list_pfi_created = []
    list_cf_error = []

    def add_arguments(self, parser):
        current_year = get_current_year()
        parser.add_argument('filename', nargs='+')
        parser.add_argument(
            '-p', dest='period', help='Period', metavar='PERIOD')
        parser.add_argument(
            '-y', dest='year', help=f'Year (default: {current_year})',
            type=int, metavar='YEAR', default=current_year)
        parser.add_argument(
            '-r', dest='repo', action='store_true')

    def handle(self, *args, **options):
        self.year = options.get('year')
        self.is_repo = options.get('repo')
        if not self.is_repo:
            assert options.get('period'), "Missing period in parameter"

        try:
            period = 'VIR1' if self.is_repo else options.get('period')
            self.period = PeriodeBudget.objects.get(
                annee=self.year, period__code=period)
        except (PeriodeBudget.DoesNotExist,
                PeriodeBudget.MultipleObjectsReturned) as e:
            print("Something wrong with Periode %s (%s)" % (self.year, e))
            raise CreationVirementException()

        with open(options.get('filename')[0]) as json_data:
            data = json.load(json_data)

        # Traitement des résultats un par un.
        for virement_info in data:            # try:
            vir_header = virement_info['header']
            vir_item_data = virement_info['item_data']
            vir_sender = virement_info['sender_item_data']

            doc_number = vir_header['DOCUMENT']
            doc_year = vir_header['DOC_YEAR']
            doc_type = vir_header['DOCTYPE']
            process = vir_header['PROCESS']
            version = vir_header['VERSION']

            # Suppression des virements qui ne sont pas dans l'année.
            if doc_year != str(self.year):
                print(f'DOC_YEAR ({doc_year}) ne match pas ({self.year})')
                continue

            datestring = vir_header['CRTDATE'] + " " + vir_header['CRTTIME']

            if any((not self.is_repo and process != 'TRAN',
                    self.is_repo and (process != 'COVR' or doc_type != 'REPO'))):
                print(f'Le process du virement ({doc_number}) ne match pas ({process})')
                continue

            if version != '000':
                print(f'La version du virement ({doc_number}) ne match pas ({version})')
                continue

            vir_date = vir_date_format(datestring, VIR_DATETIME_FORMATS)
            vir = 0

            with transaction.atomic():
                try:
                    # Temp FIX ?
                    if vir_header['DOCDATE'] is None:
                        continue
                    # Creation du virement.
                    if not Virement.objects\
                            .filter(
                                document_number=doc_number,
                                value_date=vir_date_format(vir_header['DOCDATE'], VIR_DATE_FORMATS))\
                            .count():
                        print(f"Création du Virement {doc_number} (date {vir_header['DOCDATE']})")

                        vir = Virement.objects.create(
                            document_number=doc_number,
                            document_type=vir_header['DOCTYPE'],
                            version=version,
                            perimetre=vir_header['FM_AREA'],
                            process=process,
                            creator_login=vir_header['CRTUSER'],
                            creation_date=vir_date,
                            value_date=vir_date_format(vir_header['DOCDATE'], VIR_DATE_FORMATS))

                        for item_data in vir_item_data:
                            self.parseItemData(item_data, vir, "receiver", vir_date)

                        if not self.is_repo:
                            for item_data in vir_sender:
                                self.parseItemData(item_data, vir, "sender", vir_date)

                    else:
                        print(f"Le virement {doc_number} docnumber existe déjà.")
                except CreationVirementException:
                    if vir:
                        print(f"Suppression du virement en erreur {vir.document_number}")
                        vir.delete()
        print('Missing Structure : {}'.format(', '.join(set(self.list_cf_error))))
        print('Missing PFI : {}'.format(', '.join(set(self.list_pfi_error))))
        for pfi in self.list_pfi_created:
            print(f"PFI created : {pfi}")

    def parseItemData(self, item_data, virement, type, vir_date):
        cf_code = item_data['FUNDS_CTR']
        pfi_code = item_data['MEASURE']
        try:
            cf = Structure.active.get(code=cf_code)
            pfi = PlanFinancement.active.get(code=pfi_code, structure=cf)
        except (Structure.DoesNotExist,
                Structure.MultipleObjectsReturned) as e:
            print(f"Something wrong with CF {cf_code} ({e})")
            self.list_cf_error.append(cf_code)
            raise CreationVirementException()
        except PlanFinancement.DoesNotExist as e:
            # We create the PFI with default attribute.
            self.list_pfi_error.append(pfi_code)
            created = PlanFinancement.objects.create(
                structure=cf, code=pfi_code, label='FIXIT', eotp='FIXIT',
                centrecoutderive='FIXIT', centreprofitderive='FIXIT',
                groupe1='FIXIT', groupe2='FIXIT',
                is_fleche=False, is_pluriannuel=False,
                is_active=True)
            self.list_pfi_created.append(f"PFI {created} created on structure {cf}")
            raise CreationVirementException()
        except PlanFinancement.MultipleObjectsReturned as e:
            print(f"Something wrong with PFI {pfi_code} on CF {cf_code} ({e})")
            self.list_pfi_error.append(pfi_code)
            raise CreationVirementException()

        type_budget = item_data['BUDCAT']

        # Virement Depense
        if item_data['CTEM_CATEGORY'] == '3':
            # On est en dépense.
            montant_ae = montant_cp = montant_dc = Decimal('0.00')
            montant = round(item_data['TOTAL_AMOUNT_TCUR'], 2)
            if type == "sender":
                montant = -montant

            if type_budget == '9F':
                montant_dc = montant_cp = Decimal(montant)
            if type_budget == '9G':
                montant_ae = Decimal(montant)

            code_compte_budgetaire = item_data['CMMT_ITEM']
            try:
                naturecomptabledep = NatureComptableDepense.active\
                    .get(code_compte_budgetaire=code_compte_budgetaire)
                domaine = DomaineFonctionnel.active.get(code=item_data['FUNC_AREA'])
            except (NatureComptableDepense.DoesNotExist,
                    NatureComptableDepense.MultipleObjectsReturned) as e:
                print(f"Something wrong with NCD {code_compte_budgetaire} ({e})")
                raise CreationVirementException()
            except (DomaineFonctionnel.DoesNotExist,
                    DomaineFonctionnel.MultipleObjectsReturned) as e:
                print("Something wrong with DF {item_data['FUNC_AREA']} ({e})")
                raise CreationVirementException()

            commentaire = f"{item_data['ITEM_TEXT']} ({virement.document_number})"
            dep = Depense.objects.create(
                pfi=pfi, periodebudget=self.period,
                naturecomptabledepense=naturecomptabledep,
                domainefonctionnel=domaine, annee=self.period.annee,
                fonds=item_data['FUND'], montant_ae=montant_ae, montant_cp=montant_cp,
                montant_dc=montant_dc, commentaire=commentaire,
                virement=virement)

            return True

        # Virement Recette
        if item_data['CTEM_CATEGORY'] == '2':
            montant_ar = montant_re = montant_dc = Decimal('0.00')
            montant = round(item_data['TOTAL_AMOUNT_TCUR'], 2)
            if type == "sender":
                montant = -montant

            if type_budget == '9F':
                montant_dc = montant_re = Decimal(montant)
            if type_budget == '9G':
                montant_ar = Decimal(montant)

            code_compte_budgetaire = item_data['CMMT_ITEM']
            try:
                naturecomptablerecette = NatureComptableRecette.active\
                    .get(code_compte_budgetaire=code_compte_budgetaire)
            except (NatureComptableRecette.DoesNotExist,
                    NatureComptableRecette.MultipleObjectsReturned) as e:
                print(f"Something wrong with NCR {code_compte_budgetaire} ({e})")
                raise CreationVirementException()

            commentaire = f"{item_data['ITEM_TEXT']} ({virement.document_number})"
            rec = Recette.objects.create(
                pfi=pfi, periodebudget=self.period,
                naturecomptablerecette=naturecomptablerecette,
                annee=self.period.annee,
                montant_ar=montant_ar, montant_re=montant_re,
                montant_dc=montant_dc, commentaire=commentaire,
                virement=virement)

            return True
