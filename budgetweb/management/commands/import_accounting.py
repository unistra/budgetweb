import csv
from decimal import Decimal
import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from budgetweb import models
from budgetweb.apps.structure import models as structure_models


commands_logger = logging.getLogger('import_commands')


def to_decimal(amount):
    return Decimal((amount.replace(' ', '').replace(',', '.')) or 0)


class RowError(Exception):
    pass


class Command(BaseCommand):
    help = 'Import the accounting'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

    def handle(self, *args, **options):

        accountings = []
        period = models.PeriodeBudget.active.first()
        self.errors = []

        # Structure du fichier :

        # Année
        # Structure
        # Plan de financement
        # Dépense/recette
        # Enveloppe
        # Nature comptable
        # Domaine fonctionnel
        # AE
        # CP
        # Charges/immos
        # AR
        # RE
        # Produits/ressources
        # Commentaire

        structures = {s.code: s for s
                      in structure_models.Structure.active.all()}
        pfis = {pfi.code: pfi for pfi
                in structure_models.PlanFinancement.active.all()}
        dan = {(an.code_nature_comptable, an.is_fleche): an for an
               in structure_models.NatureComptableDepense.active.all()}
        ran = {(an.code_nature_comptable, an.is_fleche): an for an
               in structure_models.NatureComptableRecette.active.all()}
        domains = {d.code: d for d
                   in structure_models.DomaineFonctionnel.active.all()}

        for filename in options.get('filename'):
            # Detect charset with chardet ?
            # Windows encoding
            with open(filename, encoding='iso-8859-1') as h:
                reader = csv.reader(h, delimiter=';', quotechar='"')
                for index, row in enumerate(reader):
                    if index == 0:
                        # Ignore header
                        continue

                    try:
                        (year, structure, pfi, accounting_type, enveloppe, nature,
                         domain, ae, cp, d_dc, ar, re, r_dc, commentary) = row

                        pfi = self.get_object(pfis, pfi, 'PFI')
                        if accounting_type.lower().startswith('d'):
                            # Dépense
                            model = models.Depense
                            nature = self.get_object(dan, (nature, pfi.is_fleche), 'nature')
                            functional_domain = self.get_object(
                                domains, domain, 'domaine fonctionnel', msg=f'- nature : {nature}')

                            amounts = {
                                'montant_dc': to_decimal(d_dc),
                                'montant_cp': to_decimal(cp),
                                'montant_ae': to_decimal(ae),
                                'naturecomptabledepense': nature,
                                'domainefonctionnel': functional_domain,
                            }
                        else:
                            # Recette
                            model = models.Recette
                            nature = self.get_object(ran, (nature, pfi.is_fleche), 'nature')

                            amounts = {
                                'montant_dc': to_decimal(r_dc),
                                'montant_re': to_decimal(re),
                                'montant_ar': to_decimal(ar),
                                'naturecomptablerecette': nature,
                                'domainefonctionnel': domain,
                            }

                        structure = self.get_object(structures, structure, 'structure')
                        accountings.append(model(
                            pfi=pfi, commentaire=commentary or None,
                            periodebudget=period, annee=year, **amounts))

                    except RowError:
                        continue

        if self.errors:
            print('ERRORS :\n\n{}'.format('\n'.join(self.errors)))
        else:
            sid = transaction.savepoint()
            try:
                for obj in accountings:
                    obj.save()
                print(f'{len(accountings)} accountings created')
            except Exception as e:
                print(f'Exception on save : {e}')
                transaction.savepoint_rollback(sid)
            else:
                transaction.savepoint_commit(sid)

        commands_logger.info('Command import_accounting launched with parameters : %s' % options)

    def get_object(self, dct, key, name, msg=''):
        try:
            return dct[key]
        except KeyError:
            msg = '' or f' {msg}'
            self.errors.append(f'{name.title()} "{key}" does not exist{msg}')
            raise RowError
