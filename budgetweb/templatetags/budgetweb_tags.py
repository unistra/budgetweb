from decimal import Decimal
import re

from django import template
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.formats import number_format

register = template.Library()


@register.filter(is_safe=True)
def intspace(value, use_l10n=True):
    """
    Converts an integer to a string containing whitespaces every three digits.
    For example, 3000 becomes '3 000' and 45000 becomes '45 000'.
    """
    if settings.USE_L10N and use_l10n:
        try:
            if not isinstance(value, (float, Decimal)):
                value = int(value)
        except (TypeError, ValueError):
            return intspace(value, False)
        else:
            return number_format(value, force_grouping=True)
    if value is None:
        return value
    orig = force_text(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1> \g<2>', orig)
    if orig == new:
        return new
    else:
        return intspace(new, use_l10n)


@register.filter(is_safe=True)
def dictvalue(value, key):
    """
    Get a dict value by its key
    """
    return value.get(key, None)


@register.filter(is_safe=True)
def getattribute(value, key):
    """
    Get an object's attribute
    """
    return getattr(value, key, None)


@register.simple_tag
def resume_colspan(periodes1, periodes2, montants_types):
    """
    Return the resume colspan
    """
    return (1 + (len(montants_types) * (len(periodes1 or periodes2) + 1)))


@register.simple_tag
def pluriannuel_rowspan(base_rowspan, montants_types):
    """
    Return the pluriannuel rowspan
    """
    return base_rowspan * (len(montants_types))


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter(is_safe=True)
def sum_montants(structure, fields):
    result = Decimal(0)
    for attr, value in fields['structure_montants']:
        try:
            montant = getattr(getattr(structure, attr)[0], value)
        except Exception:
            montant = Decimal(0)
        result += montant
    return result


@register.filter(is_safe=True)
def sum_pfis(pfi, fields):
    result = Decimal(0)
    for attr, field in fields['pfis']:
        compta = getattr(pfi, attr, [])
        for montant in compta:
            try:
                value = getattr(montant, field)
            except Exception:
                value = Decimal(0)
            result += value
    return result


@register.filter(is_safe=True)
def multiply(a, b):
    return int(a) * int(b)
