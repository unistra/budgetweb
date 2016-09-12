class StructureUnauthorizedException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = "Vous n'avez pas accès à cette structure"
