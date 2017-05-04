from decimal import Decimal
from itertools import chain, groupby

from django.db.models import F, Sum

from budgetweb.models import PeriodeBudget, StructureAuthorizations
from budgetweb.apps.structure.models import Structure
from .models import Depense, Recette


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
                periode = c['periodebudget__code']
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
        .values('annee', 'periodebudget__code', 'enveloppe')\
        .annotate(sum_depense_ae=Sum('montant_ae'),
                  sum_depense_cp=Sum('montant_cp'),
                  sum_depense_dc=Sum('montant_dc'))
    recette = Recette.objects.filter(**query_params)\
        .annotate(enveloppe=F('naturecomptablerecette__enveloppe'))\
        .values('annee', 'periodebudget__code', 'enveloppe')\
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
                periode = c['periodebudget__code']
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
