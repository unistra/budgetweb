from django.conf import settings
from django.contrib.auth.models import Group


class BudgetWebMiddleware():
    """ Basic operations to modify session at user authentication :
    * adding user's groups in session
    """

    def process_request(self, request):
        """
        Process request method
        """

        if request.user.is_authenticated():
            if not request.user.is_active:
                return HttpResponseForbidden('Unauthorized')

            # Par défaut tous les super utilisateurs sont dans le groupe DFI.
            try:
                user = request.user
                if user.is_superuser and not \
                   user.groups.filter(name=settings.DFI_GROUP_NAME).exists():
                    grp = Group.objects.get(settings.DFI_GROUP_NAME)
                    user.groups.add(grp)
            except Group.DoesNotExist:
                pass
        return None
