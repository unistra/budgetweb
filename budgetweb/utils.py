from decimal import Decimal
from itertools import chain, groupby

from django.db.models import F, Sum

from budgetweb.apps.structure.models import Structure
from .models import (Depense, PeriodeBudget, StructureAuthorizations, Recette,
                     StructureMontant)


def get_current_year():
    try:
        return PeriodeBudget.active.first().annee
    except Exception:
        return None


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
    details = []

    for compta in totals:
        compta_details = {}
        for year, year_values in groupby(compta, lambda x: x['annee']):
            year_values = list(year_values)
            yd = compta_details.setdefault(year, {})
            for compta_types, montants in montants_dict.items():
                compta_types_dict = yd.setdefault(compta_types, [{}, {}])
                for e, e_values in groupby(year_values, lambda x: x['enveloppe']):
                    e_values = list(e_values)
                    enveloppe_dict = compta_types_dict[0].setdefault(e, [{}, {}])
                    for period, values in groupby(e_values, lambda x: x['periodebudget__period__code']):
                        periods_dict = enveloppe_dict[0].setdefault(period, {})
                        total_period = compta_types_dict[1].setdefault(period, {})
                        final_total = compta_types_dict[1].setdefault('total', {})
                        values = list(values)[0]
                        for m in montants:
                            value = values.get('sum_%s' % m.lower(), None)
                            if value is not None:
                                enveloppe_dict[1].setdefault(m, Decimal(0))
                                total_period.setdefault(m, Decimal(0))
                                periods_dict[m] = value

                                # Totals :
                                # per enveloppe
                                enveloppe_dict[1][m] += value
                                # per periode and montant_type
                                total_period[m] += value
                                # per enveloppe and periods
                                final_total.setdefault(m, Decimal(0))
                                final_total[m] += value

        details.append(compta_details)
    return details


def get_pfi_total(pfi, year=None):
    """
    Retourne un tableau avec l'année
    """
    year = year or get_current_year()
    query_params = {'pfi': pfi.id, 'periodebudget__annee': year}

    depense = Depense.objects.filter(**query_params)\
        .annotate(enveloppe=F('naturecomptabledepense__enveloppe'))\
        .values('annee', 'periodebudget__period__code', 'enveloppe')\
        .annotate(sum_depense_ae=Sum('montant_ae'),
                  sum_depense_cp=Sum('montant_cp'),
                  sum_depense_dc=Sum('montant_dc'))\
        .order_by('annee')
    recette = Recette.objects.filter(**query_params)\
        .annotate(enveloppe=F('naturecomptablerecette__enveloppe'))\
        .values('annee', 'periodebudget__period__code', 'enveloppe')\
        .annotate(sum_recette_ar=Sum('montant_ar'),
                  sum_recette_re=Sum('montant_re'),
                  sum_recette_dc=Sum('montant_dc'))\
        .order_by('annee')

    return depense, recette


def get_pfi_years(pfi, begin_current_period=False, year_number=4, year=None):
    from .utils import get_current_year

    current_year = year or get_current_year()

    if pfi.date_debut and pfi.date_fin:
        if begin_current_period:
            begin_year = pfi.date_debut.year
        else:
            begin_year = current_year - 1 if pfi.date_debut.year < current_year else current_year
        end_year = min(begin_year + year_number, pfi.date_fin.year)\
            if year_number else pfi.date_fin.year
        return list(range(begin_year, end_year + 1))
    return []


def get_pfi_total_types(pfi, year):
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

    def montant_type(x):
        return [k for k, v in montants_dict.items() if x in v][0]

    types = []
    years = get_pfi_years(pfi, year=year)

    for comptabilite in get_pfi_total(pfi, year):
        compta_types = {
            k: [{default_period: {}}, {}] for k in montants_dict.keys()}
        for c in comptabilite:
            fields = [k for k in c.keys() if k.startswith('sum_')]
            for field in fields:
                periode = c['periodebudget__period__code']
                montant = c[field]
                annee = c['annee']
                field_name = field.split('_')[-1].upper()
                mt = montant_type(field_name)
                ct = compta_types[mt]
                periode_dict = ct[0].setdefault(periode, {})
                total_year_dict = ct[1].setdefault(
                    field_name, dict.fromkeys(years, Decimal(0)))
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

                # Total per year
                total_year_dict[annee] =\
                    total_year_dict.get(annee, Decimal(0)) + montant

        types.append(compta_types)

    return types


def tree_infos(year, period_code):
    """
    BROLDn = Σ(BR(1..n-1))
    VIRn = Σ(VIR(1..n))
    BAn = BI + VIRn + BROLDn
    BRn = BRn
    BMn = BAn + BRn = montants
    """

    structuremontant_filters = {
        'annee': year, 'periodebudget__annee': year}
    pfi_filters = {'annee': year, 'periodebudget__annee': year}
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
                (('&sum; Dép. AE', 'Sommes des dépenses en AE',
                    {'structure_montants': (('montants', 'depense_montant_ae'),),
                     'pfis': (('depense_bi', 'montant_ae'),)}),
                 ('&sum; Dép. CP', 'Sommes des dépenses en CP',
                    {'structure_montants': (('montants', 'depense_montant_cp'),),
                     'pfis': (('depense_bi', 'montant_cp'),)}),),
                # Recettes
                (('&sum; Rec. AR', 'Sommes des recettes en AR',
                    {'structure_montants': (('montants', 'recette_montant_ar'),),
                     'pfis': (('recette_bi', 'montant_ar'),)}),
                 ('&sum; Rec. RE', 'Sommes des recettes en RE',
                    {'structure_montants': (('montants', 'recette_montant_re'),),
                     'pfis': (('recette_bi', 'montant_re'),)}),)
            ),
            'dc': (
                # Dépenses
                (('<span style="font-size:0.8em;">&sum; Dép. Charges / Immos</span>', 'Sommes des dépenses en DC',
                    {'structure_montants': (('montants', 'depense_montant_dc'),),
                     'pfis': (('depense_bi', 'montant_dc'),)}),),
                # Recettes
                (('<span style="font-size:0.7em;">&sum; Rec. Produits / Ressources</span>', 'Sommes des recettes en DC',
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
                    periodebudget__period__code=period_code, **structuremontant_filters),
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
                        periodebudget__period__code=period_code, **pfi_filters),
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
                        periodebudget__period__code=period_code, **pfi_filters),
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
                (('&sum; Dép. AE BA', 'Le budget actualisé (BA) correspond au budget initial (BI) additionné aux virements (VIR)',
                    {'structure_montants':
                        (('bi', 'depense_montant_ae'), ('vir', 'depense_montant_ae'), ('br_old', 'depense_montant_ae')),
                     'pfis':
                        (('depense_bi', 'montant_ae'), ('depense_vir', 'montant_ae'), ('depense_br_old', 'montant_ae'))
                    }),
                 ('&sum; Dép. AE BR', 'Le budget rectificiatif (BR) correspond aux saisies en cours.',
                    {'structure_montants': (('br', 'depense_montant_ae'),),
                     'pfis': (('depense_br', 'montant_ae'),)}),
                 ('&sum; Dép. AE BM', 'Le budget modifié (BM) correspond au budget actualisé (BA) additionné au budget rectificiatif (BR)',
                    {'structure_montants': (('bm', 'depense_montant_ae'),),
                     'pfis': (('depense_bm', 'montant_ae'),)}),
                 ('&sum; Dép. CP BA', 'Le budget actualisé (BA) correspond au budget initial (BI) additionné aux virements (VIR)',
                    {'structure_montants' :
                        (('bi', 'depense_montant_cp'), ('vir', 'depense_montant_cp'), ('br_old', 'depense_montant_cp')),
                     'pfis':
                        (('depense_bi', 'montant_cp'), ('depense_vir', 'montant_cp'), ('depense_br_old', 'montant_cp'))}),
                 ('&sum; Dép. CP BR', 'Le budget rectificiatif (BR) correspond aux saisies en cours.',
                    {'structure_montants': (('br', 'depense_montant_cp'),),
                     'pfis': (('depense_br', 'montant_cp'),)}),
                 ('&sum; Dép. CP BM', 'Le budget modifié (BM) correspond au budget actualisé (BA) additionné au budget rectificiatif (BR)',
                    {'structure_montants': (('bm', 'depense_montant_cp'),),
                     'pfis': (('depense_bm', 'montant_cp'),)})),
                # Recettes
                #(('&sum; Rec. AR BA', 'Le budget actualisé (BA) correspond au budget initial (BI) additionné aux virements (VIR)',
                #    {'structure_montants':
                #        (('bi', 'recette_montant_ar'), ('vir', 'recette_montant_ar'), ('br_old', 'recette_montant_ar')),
                #     'pfis':
                #        (('recette_bi', 'montant_ar'), ('recette_vir', 'montant_ar'), ('recette_br_old', 'montant_ar'))}),
                # ('&sum; Rec. AR BR', 'Le budget rectificiatif (BR) correspond aux saisies en cours.',
                #    {'structure_montants': (('br', 'recette_montant_ar'),),
                #     'pfis': (('recette_br', 'montant_ar'),)}),
                # ('&sum; Rec. AR BM', 'Le budget modifié (BM) correspond au budget actualisé (BA) additionné au budget rectificiatif (BR)',
                #    {'structure_montants': (('bm', 'recette_montant_ar'),),
                #     'pfis': (('recette_bm', 'montant_ar'),)}),

                  (('&sum; Rec. RE BA', 'Le budget actualisé (BA) correspond au budget initial (BI) additionné aux virements (VIR)',
                     {'structure_montants':
                         (('bi', 'recette_montant_re'), ('vir', 'recette_montant_re'), ('br_old', 'recette_montant_re')),
                      'pfis':
                         (('recette_bi', 'montant_re'), ('recette_vir', 'montant_re'), ('recette_br_old', 'montant_re'))}),
                  ('&sum; Rec. RE BR', 'Le budget rectificiatif (BR) correspond aux saisies en cours.',
                     {'structure_montants': (('br', 'recette_montant_re'),),
                      'pfis': (('recette_br', 'montant_re'),)}),
                  ('&sum; Rec. RE BM', 'Le budget modifié (BM) correspond au budget actualisé (BA) additionné au budget rectificiatif (BR)',
                     {'structure_montants': (('bm', 'recette_montant_re'),),
                      'pfis': (('recette_bm', 'montant_re'),)})
                 ),
            ),
            'dc' : (
                # Dépenses
                (('&sum; Dép. DC BA', 'Le budget actualité (BA) correspond au budget initial (BI) additionné aux virements (VIR)',
                    {'structure_montants':
                        (('bi', 'depense_montant_dc'), ('vir', 'depense_montant_dc'), ('br_old', 'depense_montant_dc')),
                     'pfis':
                        (('depense_bi', 'montant_dc'), ('depense_vir', 'montant_dc'), ('depense_br_old', 'montant_dc'))}),
                 ('&sum; Dép. DC BR', 'Le budget rectificiatif (BR) correspond aux saisies en cours.',
                    {'structure_montants': (('br', 'depense_montant_dc'),),
                     'pfis': (('depense_br', 'montant_dc'),)}),
                 ('&sum; Dép. DC BM', 'Le budget modifié (BM) correspond au budget actualisé (BA) additionné au budget rectificiatif (BR)',
                    {'structure_montants': (('bm', 'depense_montant_dc'),),
                     'pfis': (('depense_bm', 'montant_dc'),)}),),
                # Recettes
                (('&sum; Rec. DC BA', 'Le budget actualité (BA) correspond au budget initial (BI) additionné aux virements (VIR)',
                    {'structure_montants':
                        (('bi', 'recette_montant_dc'), ('vir', 'recette_montant_dc'), ('br_old', 'recette_montant_dc')),
                     'pfis':
                        (('recette_bi', 'montant_dc'), ('recette_vir', 'montant_dc'), ('recette_br_old', 'montant_dc'))}),
                 ('&sum; Rec. DC BR', 'Le budget rectificiatif (BR) correspond aux saisies en cours.',
                    {'structure_montants': (('br', 'recette_montant_dc'),),
                     'pfis': (('recette_br', 'montant_dc'),)}),
                 ('&sum; Rec. DC BM', 'Le budget modifié (BM) correspond au budget actualisé (BA) additionné au budget rectificiatif (BR)',
                    {'structure_montants': (('bm', 'recette_montant_dc'),),
                     'pfis': (('recette_bm', 'montant_dc'),)}),),
            ),
        }

    return prefetches, cols


def get_selected_year(request, default_period=None):
    session_year = request.session.get('period_year')
    if not session_year:
        if default_period:
            return default_period.annee
        else:
            return get_current_year()
    return session_year
