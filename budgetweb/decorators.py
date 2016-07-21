from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

from .exceptions import StructureUnauthorizedException
from .models import PlanFinancement, StructureAuthorizations


def is_authorized_structure(func):
    """
    Check if the structure is authorized for the user
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            user = request.user
            is_authorized = False
            pfi = PlanFinancement.objects.get(pk=kwargs.get('pfiid'))
            user_structures = []
            try:
                user_structures = user.structureauthorizations.structures\
                    .filter(is_active=True).values_list('pk', flat=True)
            except StructureAuthorizations.DoesNotExist:
                pass
            is_authorized = user.is_superuser\
                or pfi.structure.pk in user_structures
            if not is_authorized:
                raise StructureUnauthorizedException
        except:
            return HttpResponseForbidden(
                StructureUnauthorizedException().message)
        return func(request, *args, **kwargs)
    return wrapper


def is_ajax_get(view_func):
    """
    Check if the request is and ajax GET request
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.is_ajax() and request.method == 'GET':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied()
    return wrapper