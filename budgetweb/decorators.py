from functools import wraps

from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseForbidden

from .exceptions import StructureUnauthorizedException


POSTGRESQL_LOCK_MODES = (
    'ACCESS SHARE',
    'ROW SHARE',
    'ROW EXCLUSIVE',
    'SHARE UPDATE EXCLUSIVE',
    'SHARE',
    'SHARE ROW EXCLUSIVE',
    'EXCLUSIVE',
    'ACCESS EXCLUSIVE',
)


def is_authorized_structure(func):
    """
    Check if the structure is authorized for the user
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        from .models import PlanFinancement, StructureAuthorizations

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


def require_lock(model, lock='ACCESS EXCLUSIVE'):
    """
    https://www.caktusgroup.com/blog/2009/05/26/explicit-table-locking-with-postgresql-and-django/
    Decorator for PostgreSQL's table-level lock functionality
    
    PostgreSQL's LOCK Documentation:
    http://www.postgresql.org/docs/9.5/interactive/sql-lock.html
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if lock not in POSTGRESQL_LOCK_MODES:
                raise ValueError('%s is not a PostgreSQL supported lock mode.')
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute(
                'LOCK TABLE %s IN %s MODE' % (model._meta.db_table, lock)
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator
