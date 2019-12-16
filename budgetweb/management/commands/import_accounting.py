import csv
from decimal import Decimal

from django.core.management.base import BaseCommand

from budgetweb import models
from budgetweb.apps.structure import models as structure_models


def to_decimal(amount):
    return Decimal((amount.replace(' ', '').replace(',', '.')) or 0)


class Command(BaseCommand):
    help = 'Import the accounting'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+')

    def handle(self, *args, **options):

        period = models.PeriodeBudget.active.first()

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
        dan = {an.code_nature_comptable: an for an
               in structure_models.NatureComptableDepense.active.all()}
        ran = {an.code_nature_comptable: an for an
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
                    (year, structure, pfi, accounting_type, enveloppe, nature,
                     domain, ae, cp, d_dc, ar, re, r_dc, commentary) = row
                    if accounting_type.lower().startswith('d'):
                        # Dépense
                        model = models.Depense
                        amounts = {
                            'montant_dc': to_decimal(d_dc),
                            'montant_cp': to_decimal(cp),
                            'montant_ae': to_decimal(ae),
                            'naturecomptabledepense': dan[nature],
                            'domainefonctionnel': domains[domain],
                        }
                    else:
                        # Recette
                        model = models.Recette
                        amounts = {
                            'montant_dc': to_decimal(d_dc),
                            'montant_re': to_decimal(re),
                            'montant_ar': to_decimal(ar),
                            'naturecomptablerecette': ran[nature],
                            'domainefonctionnel': domain,
                        }
                    model.objects.create(
                        pfi=pfis[pfi], structure=structures[structure],
                        commentaire=commentary or None,
                        periodebudget=period, annee=year, **amounts)
