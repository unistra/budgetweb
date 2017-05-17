from functools import wraps
from importlib import import_module

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseForbidden

from .exceptions import (StructureUnauthorizedException,
                         EditingUnauthorizedException,
                         PeriodeBudgetUninitializeError)


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
        from .utils import get_authorized_structures_ids

        try:
            user = request.user
            is_authorized = False
            structure_id = int(kwargs.get('structid', 0))
            if 'pfiid' in kwargs:
                pfi = PlanFinancement.objects.get(pk=kwargs.get('pfiid'))
                structure_id = pfi.structure_id
            user_structures = get_authorized_structures_ids(user)[0]
            is_authorized = structure_id in user_structures
            if not is_authorized:
                raise StructureUnauthorizedException
        except:
            return HttpResponseForbidden(
                StructureUnauthorizedException().message)
        return func(request, *args, **kwargs)
    return wrapper


def is_authorized_editing(func):
    """
    Check if the user can write something in the period
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        from budgetweb.apps.structure.models import PlanFinancement
        from .models import PeriodeBudget
        from datetime import datetime
        try:
            is_authorized = False
            user = request.user
            periode_active = PeriodeBudget.activebudget.first()

            if periode_active.date_debut_saisie is None or \
               periode_active.date_fin_saisie is None or \
               periode_active.date_debut_retardataire is None or \
               periode_active.date_fin_retardataire is None or \
               periode_active.date_debut_dfi is None or \
               periode_active.date_fin_dfi is None or \
               periode_active.date_debut_admin is None or \
               periode_active.date_fin_admin is None:
                raise PeriodeBudgetUninitializeError

            date_today = datetime.now().date()

            if periode_active.date_debut_saisie <= date_today and\
               periode_active.date_fin_saisie >= date_today:
                is_authorized = True

            is_late_group_member = request.user.groups.filter(
                                        name=settings.LATE_GROUP_NAME).exists()
            if periode_active.date_debut_retardataire <= date_today and\
               periode_active.date_fin_retardataire >= date_today and\
               is_late_group_member:
                is_authorized = True

            is_dfi_member = request.user.groups.filter(
                                        name=settings.LATE_GROUP_NAME).exists()
            if periode_active.date_debut_dfi <= date_today and\
               periode_active.date_fin_dfi >= date_today and\
               is_dfi_member:
                is_authorized = True

            if periode_active.date_debut_admin <= date_today and\
               periode_active.date_fin_admin >= date_today and\
               request.user.is_superuser:
                is_authorized = True

            if not is_authorized:
                raise EditingUnauthorizedException
        except EditingUnauthorizedException as e:
            return HttpResponseForbidden(
                EditingUnauthorizedException().message)
        except PeriodeBudgetUninitializeError as e:
            return HttpResponseForbidden(
                PeriodeBudgetUninitializeError().message)
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


def require_lock(models, lock='ACCESS EXCLUSIVE'):  # pragma: no cover
    """
    https://www.caktusgroup.com/blog/2009/05/26/explicit-table-locking-with-postgresql-and-django/
    Decorator for PostgreSQL's table-level lock functionality

    PostgreSQL's LOCK Documentation:
    http://www.postgresql.org/docs/9.5/interactive/sql-lock.html
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if settings.DATABASES['default']['ENGINE'].endswith('psycopg2'):
                if lock not in POSTGRESQL_LOCK_MODES:
                    raise ValueError('%s is not a PostgreSQL supported lock mode.')
                from django.db import connection
                cursor = connection.cursor()
                for model in models:
                    if isinstance(model, str):
                        app_label, model_name = model.split('.')
                        app_package = django_apps.get_app_package(app_label)
                        model_module = import_module('%s.models' % app_package)
                        model = getattr(model_module, model_name)
                    cursor.execute(
                        'LOCK TABLE %s IN %s MODE' % (model._meta.db_table, lock)
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator
