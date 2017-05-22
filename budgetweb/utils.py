from decimal import Decimal
from itertools import chain, groupby

from django.db.models import F, Prefetch, Sum

from budgetweb.models import PeriodeBudget, StructureAuthorizations
from budgetweb.apps.structure.models import Structure
from .models import Depense, Recette, StructureMontant


# TODO : Ajouter une exception si jamais pas de période ouverte
def get_current_year():
    return PeriodeBudget.active.first().annee


def get_authorized_structures_ids(user):
    """
    Return a tuple of authorized structures and the authorized structures with
    the full ascending hierarchy
    """
    if user.is_superuser:
        user_structures = list(Structure.active.all()
            .values_list('pk', flat=True))
        return (user_structures, user_structures)
    else:
        try:
            structures = user.structureauthorizations.structures\
                .filter(is_active=True)
            # Add parents in the authorized structures set
            hierarchy_structures = set(map(int, chain(
                *(s.full_path.split('/')[1:] for s in structures))))
            user_structures = {s.pk for s in structures}
            return (user_structures, hierarchy_structures)
        except StructureAuthorizations.DoesNotExist:
            return (set(), set())


def get_detail_pfi_by_period(totals):
    # FIXME: docstring
    montants_dict = {'gbcp': ('AE', 'CP', 'AR', 'RE'), 'dc': ('DC',)}
    montant_type = lambda x: [
        k for k, v in montants_dict.items() if x in v][0]
    details = []

    # Group by year
    for compta in totals:
        compta_details = {}
        for year, year_values in groupby(compta, lambda x: x['annee']):
            compta_types = {k: [{}, {}] for k in montants_dict.keys()}
            periodes_set = set()
            for c in year_values:
                periode = c['periodebudget__period__code']
                periodes_set.add(periode)
                fields = [k for k in c.keys() if k.startswith('sum_')]
                for field in fields:
                    montant = c[field]
                    field_name = field.split('_')[-1].upper()
                    mt = montant_type(field_name)
                    ct = compta_types[mt]
                    nature_dict = ct[0].setdefault(
                        c['enveloppe'], [{}, {}])
                    type_dict = nature_dict[0].setdefault(
                        periode, {})
                    type_dict[field_name] = montant

                    # Total per periode and montant_type
                    nature_dict[1].setdefault(field_name, Decimal(0))
                    nature_dict[1][field_name] += montant

                    # Total per enveloppe
                    total_enveloppe = compta_types[mt][1].setdefault(periode, {})
                    total_enveloppe[field_name] = total_enveloppe.get(field_name, Decimal(0)) + montant

                    # Total per enveloppe and periods
                    total = compta_types[mt][1].setdefault('total', {})
                    total[field_name] = total.get(field_name, Decimal(0)) + montant

            # TODO: order periodes_set and global periodes_set for depenses and recettes
            compta_details[year] = (compta_types, periodes_set)
        details.append(compta_details)
    return details


def get_pfi_total(pfi, years=None):
    """
    Retourne un tableau avec l'année
    """
    query_params = {'pfi': pfi.id}
    if years:
        query_params.update({'annee__in': years})

    depense = Depense.objects.filter(**query_params)\
        .annotate(enveloppe=F('naturecomptabledepense__enveloppe'))\
        .values('annee', 'periodebudget__period__code', 'enveloppe')\
        .annotate(sum_depense_ae=Sum('montant_ae'),
                  sum_depense_cp=Sum('montant_cp'),
                  sum_depense_dc=Sum('montant_dc'))
    recette = Recette.objects.filter(**query_params)\
        .annotate(enveloppe=F('naturecomptablerecette__enveloppe'))\
        .values('annee', 'periodebudget__period__code', 'enveloppe')\
        .annotate(sum_recette_ar=Sum('montant_ar'),
                  sum_recette_re=Sum('montant_re'),
                  sum_recette_dc=Sum('montant_dc'))

    return depense, recette


def get_pfi_years(pfi, begin_current_period=False, year_number=4):
    from .utils import get_current_year

    if pfi.date_debut and pfi.date_fin:
        if begin_current_period:
            begin_year = pfi.date_debut.year
        else:
            begin_year = get_current_year()-1 if pfi.date_debut.year < get_current_year() else get_current_year()
        end_year = min(begin_year + year_number, pfi.date_fin.year)\
            if year_number else pfi.date_fin.year
        return list(range(begin_year, end_year + 1))
    return []


def get_pfi_total_types(pfi):
    # FIXME: docstring
    """
    Output format example for "depense":
    [
        {'AE': [
            {'Investissement': [
                {2017: Decimal(1), 2018: Decimal(2)},
                Decimal(3)],  # Total per "Investissement"
            'Personnel': [
                {2017: Decimal(10), 2018: Decimal(20)},
                Decimal(30)],  # Total per "Personnal"
            'Fonctionnement': [
                {2017: Decimal(100), 2018: Decimal(200)},
                Decimal(300)]  # Total per "Fonctionnement"
            },
            {2017: Decimal(111), 2018: Decimal(222)}],  # Totals per year
        'CP': [...]}
    ]
    """
    montants_dict = {'gbcp': ('AE', 'CP', 'AR', 'RE'), 'dc': ('DC',)}
    default_period = 'BI'
    montant_type = lambda x: [
        k for k, v in montants_dict.items() if x in v][0]
    types = []
    years = get_pfi_years(pfi)

    for comptabilite in get_pfi_total(pfi, years=years):
        compta_types = {k: {default_period: {}} for k in montants_dict.keys()}
        for c in comptabilite:
            fields = [k for k in c.keys() if k.startswith('sum_')]
            for field in fields:
                periode = c['periodebudget__period__code']
                montant = c[field]
                annee = c['annee']
                field_name = field.split('_')[-1].upper()
                mt = montant_type(field_name)
                ct = compta_types[mt]
                periode_dict = ct.setdefault(periode, {})
                type_dict = periode_dict.setdefault(
                    field_name, [{}, dict.fromkeys(years, None)])
                nature_dict = type_dict[0].setdefault(
                    c['enveloppe'], [dict.fromkeys(years, None), None])
                nature_dict[0][annee] = montant
                # Total per enveloppe
                nature_dict[1] = (nature_dict[1] or Decimal(0)) + montant

                # Total per type
                type_dict[1].setdefault(annee, None)
                type_dict[1][annee] =\
                    (type_dict[1][annee] or Decimal(0)) + montant
                type_dict[1]['total'] =\
                    type_dict[1].get('total', Decimal(0)) + montant
        types.append(compta_types)
    return types


def tree_infos(active_period, period_code):
    """
    BROLDn = Σ(BR(1..n-1))
    VIRn = Σ(VIR(1..n))
    BAn = BI + VIRn + BROLDn
    BRn = BRn
    BMn = BAn + BRn = montants
    """

    structuremontant_filters = {'annee': active_period.annee}
    pfi_filters = {'periodebudget__annee': active_period.annee}
    prefetches = {}
    cols = {}

    if period_code == 'BI':
        prefetches = {
            'structure_montants': (
                {'queryset': StructureMontant.objects.filter(
                    periodebudget__period__code='BI', **structuremontant_filters),
                 'to_attr': 'montants'},
            ),
            'pfis': {
                'depense': (
                    {'queryset': Depense.objects.filter(
                        periodebudget__period__code='BI', **pfi_filters),
                     'to_attr': 'depense_bi'},),
                'recette': (
                    {'queryset': Recette.objects.filter(
                        periodebudget__period__code='BI', **pfi_filters),
                     'to_attr': 'recette_bi'},),
            }
        }
        cols = {
            'gbcp': (
                # Dépenses
                (('&sum; Dép. AE',
                    {'structure_montants': (('montants', 'depense_montant_ae'),),
                     'pfis': (('depense_bi', 'montant_ae'),)}),
                 ('&sum; Dép. CP',
                    {'structure_montants': (('montants', 'depense_montant_cp'),),
                     'pfis': (('depense_bi', 'montant_cp'),)}),),
                # Recettes
                (('&sum; Rec. AR',
                    {'structure_montants': (('montants', 'recette_montant_ar'),),
                     'pfis': (('recette_bi', 'montant_ar'),)}),
                 ('&sum; Rec. RE',
                    {'structure_montants': (('montants', 'recette_montant_re'),),
                     'pfis': (('recette_bi', 'montant_re'),)}),)
            ),
            'dc' : (
                # Dépenses
                (('<span style="font-size:0.8em;">&sum; Dép. Charges / Immos</span>',
                    {'structure_montants': (('montants', 'depense_montant_dc'),),
                     'pfis': (('depense_bi', 'montant_dc'),)}),),
                # Recettes
                (('<span style="font-size:0.7em;">&sum; Rec. Produits / Ressources</span>',
                    {'structure_montants': (('montants', 'recette_montant_dc'),),
                     'pfis': (('recette_bi', 'montant_dc'),)}),),
            ),
        }
    elif period_code.startswith('BR'):
        prefetches = {
            'structure_montants': (
                {'queryset': StructureMontant.objects.filter(
                    periodebudget__period__code='BI', **structuremontant_filters),
                 'to_attr': 'bi'},
                {'queryset': StructureMontant.objects.filter(
                    periodebudget__period__code__startswith='VIR', **structuremontant_filters),
                 'to_attr': 'vir'},
                {'queryset': StructureMontant.objects.filter(
                    periodebudget__period__code__startswith='BR', **structuremontant_filters),
                 'to_attr': 'br'},
                {'queryset': StructureMontant.objects.filter(**structuremontant_filters),
                 'to_attr': 'bm'},
                {'queryset': StructureMontant.objects.filter(
                        periodebudget__period__code__startswith='BR', **structuremontant_filters
                    ).exclude(periodebudget__period__code=period_code),
                 'to_attr': 'br_old'},
            ),
            'pfis': {
                'depense': (
                    {'queryset': Depense.objects.filter(
                        periodebudget__period__code='BI', **pfi_filters),
                     'to_attr': 'depense_bi'},
                    {'queryset': Depense.objects.filter(
                        periodebudget__period__code__startswith='VIR', **pfi_filters),
                     'to_attr': 'depense_vir'},
                    {'queryset': Depense.objects.filter(
                        periodebudget__period__code__startswith='BR', **pfi_filters),
                     'to_attr': 'depense_br'
                    },
                    {'queryset': Depense.objects.filter(**pfi_filters),
                     'to_attr': 'depense_bm'},
                    {'queryset': Depense.objects.filter(
                            periodebudget__period__code__startswith='BR', **pfi_filters
                        ).exclude(periodebudget__period__code=period_code),
                     'to_attr': 'depense_br_old'}
                ),
                'recette': (
                    {'queryset': Recette.objects.filter(
                        periodebudget__period__code='BI', **pfi_filters),
                     'to_attr': 'recette_bi'},
                    {'queryset': Recette.objects.filter(
                        periodebudget__period__code__startswith='VIR', **pfi_filters),
                     'to_attr': 'recette_vir'},
                    {'queryset': Recette.objects.filter(
                        periodebudget__period__code__startswith='BR', **pfi_filters),
                     'to_attr': 'recette_br'},
                    {'queryset': Recette.objects.filter(**pfi_filters),
                     'to_attr': 'recette_bm'},
                    {'queryset': Recette.objects.filter(
                            periodebudget__period__code__startswith='BR', **pfi_filters
                        ).exclude(periodebudget__period__code=period_code),
                     'to_attr': 'recette_br_old'}
                ),
            }
        }
        cols = {
            'gbcp': (
                # Dépenses
                (('&sum; Dép. AE BA', 
                    {'structure_montants':
                        (('bi', 'depense_montant_ae'), ('vir', 'depense_montant_ae'), ('br_old', 'depense_montant_ae')),
                     'pfis':
                        (('depense_bi', 'montant_ae'), ('depense_vir', 'montant_ae'), ('depense_br_old', 'montant_ae'))
                    }),
                 ('&sum; Dép. AE VIR',
                    {'structure_montants': (('vir', 'depense_montant_ae'),),
                     'pfis': (('depense_vir', 'montant_ae'),)}),
                 ('&sum; Dép. AE BM',
                    {'structure_montants': (('bm', 'depense_montant_ae'),),
                     'pfis': (('depense_bm', 'montant_ae'),)}),
                 ('&sum; Dép. CP BA',
                    {'structure_montants' :
                        (('bi', 'depense_montant_cp'), ('vir', 'depense_montant_cp'), ('br_old', 'depense_montant_cp')),
                     'pfis': 
                        (('depense_bi', 'montant_cp'), ('depense_vir', 'montant_cp'), ('depense_br_old', 'montant_cp'))}),
                 ('&sum; Dép. CP VIR',
                    {'structure_montants': (('vir', 'depense_montant_cp'),),
                     'pfis': (('depense_vir', 'montant_cp'),)}),
                 ('&sum; Dép. CP BM',
                    {'structure_montants': (('bm', 'depense_montant_cp'),),
                     'pfis': (('depense_bm', 'montant_cp'),)})),
                # Recettes
                (('&sum; Rec. AR BA',
                    {'structure_montants':
                        (('bi', 'recette_montant_ar'), ('vir', 'recette_montant_ar'), ('br_old', 'recette_montant_ar')),
                     'pfis':
                        (('recette_bi', 'montant_ar'), ('recette_vir', 'montant_ar'), ('recette_br_old', 'montant_ar'))}),
                 ('&sum; Rec. AR VIR',
                    {'structure_montants': (('vir', 'recette_montant_ar'),),
                     'pfis': (('recette_vir', 'montant_ar'),)}),
                 ('&sum; Rec. AR BM',
                    {'structure_montants': (('bm', 'recette_montant_ar'),),
                     'pfis': (('recette_bm', 'montant_ar'),)}),
                 # ('&sum; Rec. RE BA',
                 #    {'structure_montants': 
                 #        (('bi', 'recette_montant_re'), ('vir', 'recette_montant_re'), ('br_old', 'recette_montant_re')),
                 #     'pfis': 
                 #        (('recette_bi', 'montant_re'), ('recette_vir', 'montant_re'), ('recette_br_old', 'montant_re'))}),
                 # ('&sum; Rec. RE VIR', 
                 #    {'structure_montants': (('vir', 'recette_montant_re'),),
                 #     'pfis': (('recette_vir', 'montant_re'),)}),
                 # ('&sum; Rec. RE BM',
                 #    {'structure_montants': (('bm', 'recette_montant_re'),),
                 #     'pfis': (('recette_bm', 'montant_re'),)})
                 ),
            ),
            'dc' : (
                # Dépenses
                (('&sum; Dép. DC BA',
                    {'structure_montants': 
                        (('bi', 'depense_montant_dc'), ('vir', 'depense_montant_dc'), ('br_old', 'depense_montant_dc')),
                     'pfis':
                        (('depense_bi', 'montant_dc'), ('depense_vir', 'montant_dc'), ('depense_br_old', 'montant_dc'))}),
                 ('&sum; Dép. DC VIR', 
                    {'structure_montants': (('vir', 'depense_montant_dc'),),
                     'pfis': (('depense_vir', 'montant_dc'),)}),
                 ('&sum; Dép. DC BM',
                    {'structure_montants': (('bm', 'depense_montant_dc'),),
                     'pfis': (('depense_bm', 'montant_dc'),)}),),
                # Recettes
                (('&sum; Rec. DC BA',
                    {'structure_montants':
                        (('bi', 'recette_montant_dc'), ('vir', 'recette_montant_dc'), ('br_old', 'recette_montant_dc')),
                     'pfis':
                        (('recette_bi', 'montant_dc'), ('recette_vir', 'montant_dc'), ('recette_br_old', 'montant_dc'))}),
                 ('&sum; Rec. DC VIR',
                    {'structure_montants': (('vir', 'recette_montant_dc'),),
                     'pfis': (('recette_vir', 'montant_dc'),)}),
                 ('&sum; Rec. DC BM',
                    {'structure_montants': (('bm', 'recette_montant_dc'),),
                     'pfis': (('recette_bm', 'montant_dc'),)}),),
            ),
        }

    return prefetches, cols
