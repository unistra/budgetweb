class StructureUnauthorizedException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = "Vous n'avez pas accès à cette structure"


class EditingUnauthorizedException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = "La période de saisie n'est pas active. \
                        Aucune modification n'est possible."


class PeriodeBudgetUninitializeError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = "Les périodes budgétaires ne sont pas configurées \
                        correctements. \n\
                        Tous les champs dates doivent être configurés."
