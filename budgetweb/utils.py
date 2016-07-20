from budgetweb.models import PeriodeBudget


# TODO : Ajouter une exception si jamais pas de période ouverte
def getCurrentYear():
    return PeriodeBudget.objects.filter(is_active=True).first().annee
