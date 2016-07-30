import itertools

from budgetweb.models import PeriodeBudget, Structure, StructureAuthorizations


# TODO : Ajouter une exception si jamais pas de période ouverte
def getCurrentYear():
    return PeriodeBudget.objects.filter(is_active=True).first().annee


def get_authorized_structures_ids(user, hierarchy=False):
    if user.is_superuser:
        user_structures = Structure.objects.filter(is_active=True)\
            .values_list('pk', flat=True)
    else:
        try:
            structures = user.structureauthorizations.structures\
                .filter(is_active=True)
            if hierarchy:
                user_structures = set(map(int, itertools.chain(
                    *(s.full_path.split('/')[1:] for s in structures))))
            else:
                user_structures = {s.pk for s in structures}

        except StructureAuthorizations.DoesNotExist:
            user_structures = set()
    return user_structures
