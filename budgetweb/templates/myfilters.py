# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
import os,time
from os import listdir
from os.path import isfile, join
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import AuthorisationForm, CompteComptableForm , DomaineFonctionnelForm
from .forms import OrigineFondsForm, StructureForm , PlanFinancementForm , DepenseForm
from .models import Authorisation, CompteComptable , DomaineFonctionnel , PeriodeBudget
from .models import OrigineFonds , Structure , PlanFinancement , Depense , DepenseFull , RecetteFull
from .forms import DepenseForm2 , DepenseFullForm , RecetteFullForm , PeriodeBudgetForm
import json
from django.http import Http404,HttpResponse
from django import Library

from django import template
from django.template.defaultfilters import stringfilter


#register = template.Library()
@register.filter(name="rightunderscore")
#@stringfilter
def rightunderscore(value):
    truncd = value.split("_")
    first=1
    for i in truncd:
        if first:
            first=0
        else:
            res=res+"_"+i

    return res

