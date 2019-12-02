from datetime import datetime
from decimal import Decimal
import json
from django.core.management.base import BaseCommand
import britney_utils
from britney.middleware import auth
from django.conf import settings
from django.db import transaction

from budgetweb.apps.structure.models import (
    DomaineFonctionnel, Structure, PlanFinancement,
    NatureComptableDepense, NatureComptableRecette)
from budgetweb.models import (Depense, PeriodeBudget, Recette, Virement)
from budgetweb.utils import get_current_year


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

    def handle(self, *args, **options):
        self.year = options.get('year')
        assert options.get('period'), "Missing period in parameter"
        try:
            self.period = PeriodeBudget.objects.get(
                annee=self.year, period__code=options.get('period'))
        except (PeriodeBudget.DoesNotExist,
                PeriodeBudget.MultipleObjectsReturned) as e:
            print("Something wrong with Periode %s (%s)" % (self.year, e))
            raise CreationVirementException()

        with open(options.get('filename')[0]) as json_data:
            data = json.load(json_data)

        # Traitement des résultats un par un.
        for virement_info in data:
            # try:
            vir_header = virement_info['header']
            vir_item_data = virement_info['item_data']
            vir_sender = virement_info['sender_item_data']

            doc_number = vir_header['DOCUMENT']
            doc_year = vir_header['DOC_YEAR']

            # Suppression des virements qui ne sont pas dans l'année.
            if doc_year != str(self.year):
                print('DOC_YEAR (%s) ne match pas (%s)' % (doc_year, "2018"))
                continue

            datestring = vir_header['CRTDATE'] + " " + vir_header['CRTTIME']
            if vir_header['PROCESS'] != 'TRAN':
                print('Le process du virement (%s) ne match pas (%s)'
                      % (doc_number, vir_header['PROCESS']))
                continue

            if vir_header['VERSION'] != '000':
                print('La version du virement (%s) ne match pas (%s)'
                      % (doc_number, vir_header['VERSION']))
                continue
            vir_date = datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
            vir = 0

            with transaction.atomic():
                try:
                    # Temp FIX ?
                    if vir_header['DOCDATE'] is None:
                        continue
                    # Creation du virement.
                    if not Virement.objects.filter(
                            document_number=doc_number,
                            value_date=vir_header['DOCDATE']).count():
                        print("Création du Virement %s (date %s)" %
                              (doc_number, vir_header['DOCDATE']))

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
        for pfi in self.list_pfi_created:
            print("PFI created : %s" % pfi)

    def parseItemData(self, item_data, virement, type, vir_date):
        cf_code = item_data['FUNDS_CTR']
        pfi_code = item_data['MEASURE']
        try:
            cf = Structure.active.get(code=cf_code)
            pfi = PlanFinancement.active.get(code=pfi_code, structure=cf)
        except (Structure.DoesNotExist,
                Structure.MultipleObjectsReturned) as e:
            print("Something wrong with CF %s (%s)" % (cf_code, e))
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
            msg = "PFI %s created on structure %s" % (created, cf)
            self.list_pfi_created.append(msg)
            raise CreationVirementException()
        except PlanFinancement.MultipleObjectsReturned as e:
            print("Something wrong with PFI %s on CF %s (%s)" % (pfi_code,
                  cf_code, e))
            self.list_pfi_error.append(pfi_code)
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
                structure=cf, pfi=pfi, periodebudget=self.period,
                naturecomptabledepense=naturecomptabledep,
                domainefonctionnel=domaine, annee=self.period.annee,
                fonds=fonds, montant_ae=montant_ae, montant_cp=montant_cp,
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
                structure=cf, pfi=pfi, periodebudget=self.period,
                naturecomptablerecette=naturecomptablerecette,
                annee=self.period.annee,
                montant_ar=montant_ar, montant_re=montant_re,
                montant_dc=montant_dc, commentaire=commentaire,
                virement=virement)

            return True
