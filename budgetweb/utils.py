from decimal import Decimal
from itertools import chain, groupby

from budgetweb.models import PeriodeBudget, Structure, StructureAuthorizations


# TODO : Ajouter une exception si jamais pas de période ouverte
def get_current_year():
    return PeriodeBudget.active.first().annee


def get_authorized_structures_ids(user):
    """
    Return a tuple of authorized structures and the authorized structures with
    the full ascending hierarchy
    """
    if user.is_superuser:
        user_structures = list(Structure.active.all()\
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

            # TODO: order periodes_set and global periodes_set for depenses and recettes
            compta_details[year] = (compta_types, periodes_set)
        details.append(compta_details)
    return details