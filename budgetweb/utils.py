import itertools

from budgetweb.models import PeriodeBudget, Structure, StructureAuthorizations


# TODO : Ajouter une exception si jamais pas de période ouverte
def get_current_year():
    return PeriodeBudget.objects.filter(is_active=True).first().annee


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
            hierarchy_structures = set(map(int, itertools.chain(
                *(s.full_path.split('/')[1:] for s in structures))))
            user_structures = {s.pk for s in structures}
            return (user_structures, hierarchy_structures)
        except StructureAuthorizations.DoesNotExist:
            return (set(), set())
