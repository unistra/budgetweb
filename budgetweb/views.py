# -*- coding: utf-8 -*-

from collections import OrderedDict
from decimal import Decimal
from itertools import chain, groupby
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core import management
from django.db.models import F, Prefetch, Sum
from django.forms.models import modelformset_factory
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponseServerError, JsonResponse)
from django.shortcuts import (get_object_or_404, redirect, render)
from django.template import loader, Context
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import requires_csrf_token

from budgetweb.apps.structure.models import (
    DomaineFonctionnel, NatureComptableDepense, NatureComptableRecette,
    PlanFinancement, Structure)
from .decorators import (is_ajax_get, is_authorized_structure,
                         is_authorized_editing)
from .forms import DepenseForm, PlanFinancementPluriForm, RecetteForm
from .models import Depense, PeriodeBudget, Recette
from .templatetags.budgetweb_tags import sum_montants
from .utils import (
    get_authorized_structures_ids, get_detail_pfi_by_period,
    get_pfi_total_types, get_pfi_years, tree_infos, get_selected_year)


@login_required
def home(request):
    return redirect('show_tree', type_affichage='gbcp')


# AJAX
@is_ajax_get
def api_fund_designation_by_nature_and_enveloppe(request, model,
                                                 enveloppe, pfiid):
    pfi = PlanFinancement.objects.get(pk=pfiid)
    models = {
        'naturecomptablerecette': NatureComptableRecette,
        'naturecomptabledepense': NatureComptableDepense,
    }
    natures = models[model].active.filter(
        is_fleche=pfi.is_fleche, enveloppe=enveloppe
    ).order_by('priority', 'ordre')
    response_data = [
        {"id": nature.pk, "label": str(nature)} for nature in natures]
    return HttpResponse(
        json.dumps(response_data), content_type='application/json')


@is_ajax_get
def api_get_details_nature_by_code(request, model, id_nature):
    models = {
        'naturecomptablerecette': NatureComptableRecette,
        'naturecomptabledepense': NatureComptableDepense,
    }
    nature = models[model].active.get(pk=id_nature)
    if model == 'naturecomptabledepense':
        response_data = {
            'code_compte_budgetaire': nature.code_compte_budgetaire,
            'label_compte_budgetaire': nature.label_compte_budgetaire
        }
    else:
        response_data = {
            'code_compte_budgetaire': nature.code_compte_budgetaire,
            'label_compte_budgetaire': nature.label_compte_budgetaire,
            'code_fonds': nature.code_fonds,
            'label_fonds': nature.label_fonds,
        }
    return HttpResponse(
        json.dumps(response_data), content_type='application/json')


@is_ajax_get
def api_get_managment_rules_depense_by_id(request, id_naturecomptabledepense):
    nature = NatureComptableDepense.active.get(pk=id_naturecomptabledepense)
    response_data = {'is_decalage_tresorerie': nature.is_decalage_tresorerie,
                     'is_non_budgetaire': nature.is_non_budgetaire,
                     'is_pi_cfg': nature.is_pi_cfg}

    return HttpResponse(
        json.dumps(response_data), content_type='application/json')


@is_ajax_get
def api_get_managment_rules_recette_by_id(request, id_naturecomptablerecette):
    nature = NatureComptableRecette.active.get(pk=id_naturecomptablerecette)
    response_data = {'is_non_budgetaire': nature.is_non_budgetaire,
                     'is_ar_and_re': nature.is_ar_and_re}

    return HttpResponse(
        json.dumps(response_data), content_type='application/json')


@is_ajax_get
def api_set_dcfield_value_by_id(request):
    try:
        is_dfi_member = request.user.groups.filter(
            name=settings.DFI_GROUP_NAME).exists()
        is_dfi_member_or_admin = is_dfi_member or request.user.is_superuser
        pk = int(request.GET.get('pk'))
        type_compta = request.GET.get('type')
        montant = request.GET.get('montant').replace(',', '.')
        if is_dfi_member_or_admin:
            if type_compta == "depense":
                compta = Depense.objects.get(pk=pk)
            else:
                compta = Recette.objects.get(pk=pk)
            montant_dc = Decimal(montant)
            compta.montant_dc = montant_dc
            compta.save()
            return JsonResponse(
                {'message': _("The new value has been saved. "
                              "This page will be reloaded")}, status=201)
        else:
            return JsonResponse(
                {'message': _('You are not allowed to do that')}, status=400)
    except Exception as e:
        return JsonResponse(
            {'message': _("Something wrong in "
                          "api_set_dcfield_value_by_id %s") % e},
            status=400)


@login_required
def show_tree(request, type_affichage, structid=0):
    active_period = PeriodeBudget.active.select_related('period').first()
    period_code = active_period.period.code
    selected_year = get_selected_year(request, default_period=active_period)
    prefetches, columns = tree_infos(selected_year, period_code)
    active_fields = columns[type_affichage]

    # Authorized structures list
    is_tree_node = request.is_ajax()
    queryset = {'parent__id': structid} if structid else {'parent': None}
    authorized_structures, hierarchy_structures =\
        get_authorized_structures_ids(request.user)

    structures = Structure.active.prefetch_related(
        *(Prefetch('structuremontant_set', **prefetch)
            for prefetch in prefetches['structure_montants'])
    ).filter(pk__in=hierarchy_structures, **queryset).order_by('code')

    # if the PFI's structure is in the authorized structures
    if int(structid) in authorized_structures:
        pfis = PlanFinancement.active.prefetch_related(*chain(
            (Prefetch('depense_set', **prefetch)
                for prefetch in prefetches['pfis']['depense']),
            (Prefetch('recette_set', **prefetch)
                for prefetch in prefetches['pfis']['recette']),)
        ).select_related('structure').filter(structure__id=structid)
    else:
        pfis = []
    context = {
        'structures': structures,
        'pfis': pfis,
        'typeAffichage': type_affichage,
        'currentYear': selected_year,
        'cols': active_fields,
    }

    # Total sums
    if not is_tree_node:
        fields = active_fields
        total = [[Decimal(0)] * len(field) for field in fields]
        for structure in structures:
            for index0, field in enumerate(fields):
                for index1, montants in enumerate(field):
                    total[index0][index1] += sum_montants(structure, montants[2])
        context['total'] = total

    template = 'show_sub_tree.html' if is_tree_node else 'showtree.html'
    return render(request, template, context)


@login_required
@is_authorized_structure
@is_authorized_editing
def pluriannuel(request, pfiid):
    active_period = PeriodeBudget.active.select_related('period').first()
    pfi = get_object_or_404(PlanFinancement, pk=pfiid)
    if request.method == "POST":
        form = PlanFinancementPluriForm(request.POST, instance=pfi)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('pluriannuel', pfiid=pfi.id)
    else:
        form = PlanFinancementPluriForm(instance=pfi)

    if pfi.date_debut and pfi.date_fin:
        depense, recette = get_pfi_total_types(pfi)
    else:
        depense = recette = {}

    context = {
        'PFI': pfi, 'form': form, 'depense': depense, 'recette': recette,
        'years': get_pfi_years(pfi), 'origin': 'pluriannuel',
        'period': active_period
    }
    return render(request, 'pluriannuel.html', context)


def modelformset_factory_with_kwargs(cls, **formset_kwargs):
    class ModelformsetFactoryWithKwargs(cls):
        def __init__(self, *args, **kwargs):
            kwargs.update(formset_kwargs)
            super().__init__(*args, **kwargs)
    return ModelformsetFactoryWithKwargs


@login_required
@is_authorized_structure
@is_authorized_editing
def depense(request, pfiid, annee):
    # Values for the form initialization
    periodebudget = PeriodeBudget.activebudget.first()

    # Redirect to detailspfi if the active year is not selected
    if int(annee) < periodebudget.annee:
        return HttpResponseRedirect('/detailspfi/%s' % pfiid)

    pfi = PlanFinancement.objects.get(pk=pfiid)
    is_dfi_member = request.user.groups.filter(name=settings.DFI_GROUP_NAME).exists()
    is_dfi_member_or_admin = is_dfi_member or request.user.is_superuser
    natures = OrderedDict(((n.pk, n) for n in\
        NatureComptableDepense.objects.filter(is_fleche=pfi.is_fleche).order_by('priority','ordre')))
    domaines = [(d.pk, str(d)) for d in DomaineFonctionnel.active.all()]

    DepenseFormSet = modelformset_factory(
        Depense,
        form=modelformset_factory_with_kwargs(
            DepenseForm, pfi=pfi, periodebudget=periodebudget, annee=annee,
            is_dfi_member_or_admin=is_dfi_member_or_admin, natures=natures,
            domaines=domaines, user=request.user
        ),
        exclude=[],
        extra=3,
        can_delete=True
    )
    formset = DepenseFormSet(queryset=Depense.objects.filter(
        pfi=pfi,
        annee=annee,
        periodebudget=periodebudget
    ).order_by('naturecomptabledepense__priority', '-montant_ae'))

    if request.method == "POST":
        formset = DepenseFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/detailspfi/%s' % pfi.pk)

    context = {
        'PFI': pfi,
        'formset': formset,
        'currentYear': annee,
        'is_dfi_member_or_admin': is_dfi_member_or_admin,
        'form_template': 'depense.html'

    }
    return render(request, 'comptabilite.html', context)


@login_required
@is_authorized_structure
@is_authorized_editing
def recette(request, pfiid, annee):
    # Values for the form initialization
    periodebudget = PeriodeBudget.activebudget.first()

    # Redirect to detailspfi if the active year is not selected
    if int(annee) < periodebudget.annee:
        return HttpResponseRedirect('/detailspfi/%s' % pfiid)

    pfi = PlanFinancement.objects.get(pk=pfiid)
    is_dfi_member = request.user.groups.filter(name=settings.DFI_GROUP_NAME).exists()
    is_dfi_member_or_admin = is_dfi_member or request.user.is_superuser
    natures = OrderedDict(((n.pk, n) for n in\
        NatureComptableRecette.objects.filter(is_fleche=pfi.is_fleche).order_by('priority', 'ordre')))

    RecetteFormSet = modelformset_factory(
        Recette,
        form=modelformset_factory_with_kwargs(
            RecetteForm, pfi=pfi, periodebudget=periodebudget, annee=annee,
            is_dfi_member_or_admin=is_dfi_member_or_admin, natures=natures,
            user=request.user
        ),
        exclude=[],
        extra=3,
        can_delete=True
    )
    formset = RecetteFormSet(queryset=Recette.objects.filter(
        pfi=pfi, annee=annee, periodebudget=periodebudget
    ).order_by('naturecomptablerecette__priority', '-montant_ar'))

    if request.method == "POST":
        formset = RecetteFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/detailspfi/%s' % pfi.pk)

    context = {
        'PFI': pfi,
        'formset': formset,
        'currentYear': annee,
        'is_dfi_member_or_admin': is_dfi_member_or_admin,
        'form_template': 'recette.html'
    }
    return render(request, 'comptabilite.html', context)


@login_required
@is_authorized_structure
def detailspfi(request, pfiid):
    to_dict = lambda x: {k: list(v) for k, v in x}
    pfi = PlanFinancement.objects.select_related('structure').get(pk=pfiid)
    current_year = get_selected_year(request)

    depenses = Depense.objects.filter(pfi=pfi).select_related(
            'naturecomptabledepense', 'periodebudget__period', 'pfi',
            'domainefonctionnel', 'pfi__structure')\
        .annotate(enveloppe=F('naturecomptabledepense__enveloppe'))
    recettes = Recette.objects.filter(pfi=pfi).select_related(
            'naturecomptablerecette', 'periodebudget__period', 'pfi',
            'pfi__structure')\
        .annotate(enveloppe=F('naturecomptablerecette__enveloppe'))

    # Depenses and recettes per year for the resume template
    year_depenses = depenses.values(
            'annee', 'enveloppe', 'periodebudget__period__code')\
        .annotate(
            sum_dc=Sum('montant_dc'),
            sum_ae=Sum('montant_ae'),
            sum_cp=Sum('montant_cp'))
    year_recettes = recettes.values(
            'annee', 'enveloppe', 'periodebudget__period__code')\
        .annotate(
            sum_dc=Sum('montant_dc'),
            sum_ar=Sum('montant_ar'),
            sum_re=Sum('montant_re'))

    depenses = to_dict(groupby(depenses.order_by(
        'annee', 'naturecomptabledepense__code_compte_budgetaire',
        'periodebudget__period__order'), lambda x: x.annee))
    recettes = to_dict(groupby(recettes.order_by(
        'annee', 'naturecomptablerecette__code_compte_budgetaire',
        'periodebudget__period__order'), lambda x: x.annee))
    years = (depenses.keys() | recettes.keys()) or [current_year]

    sum_depenses = Depense.objects.filter(pfi=pfi).values('annee').annotate(
        sum_dc=Sum('montant_dc'),
        sum_ae=Sum('montant_ae'),
        sum_cp=Sum('montant_cp'))
    sum_depenses = to_dict(groupby(sum_depenses, lambda x: x['annee']))
    sum_recettes = Recette.objects.filter(pfi=pfi).values('annee').annotate(
        sum_dc=Sum('montant_dc'),
        sum_ar=Sum('montant_ar'),
        sum_re=Sum('montant_re'))
    sum_recettes = to_dict(groupby(sum_recettes, lambda x: x['annee']))

    resume_depenses, resume_recettes = get_detail_pfi_by_period(
        [year_depenses, year_recettes])

    periods = PeriodeBudget.objects.filter(annee=current_year)\
        .order_by('period__order').values_list('period__code', flat=True)

    context = {
        'PFI': pfi, 'currentYear': current_year,
        'listeDepense': depenses, 'listeRecette': recettes,
        'sommeDepense': sum_depenses, 'sommeRecette': sum_recettes,
        'resume_depenses': resume_depenses, 'resume_recettes': resume_recettes,
        'years': years, 'periods': periods, 'origin': 'detailspfi',
    }
    return render(request, 'detailsfullpfi.html', context)


@login_required
@is_authorized_structure
def detailscf(request, structid):
    to_dict = lambda x: {k: list(v) for k, v in x}
    structparent = Structure.objects.get(id=structid)
    liste_structure = list(structparent.get_unordered_children())
    liste_structure.insert(0, structparent)
    structure_ids = [s.pk for s in liste_structure]
    current_year = get_selected_year(request)

    queryset = {'pfi__structure__in': structure_ids}
    depenses = Depense.objects.filter(**queryset)\
        .select_related(
            'naturecomptabledepense', 'periodebudget__period', 'pfi',
            'domainefonctionnel', 'pfi__structure')\
        .annotate(enveloppe=F('naturecomptabledepense__enveloppe'))\
        .order_by('annee', 'structure',
                  'naturecomptabledepense__code_nature_comptable',
                  'periodebudget__period__order',
                  'virement__document_number')
    recettes = Recette.objects.filter(**queryset)\
        .select_related(
            'naturecomptablerecette', 'periodebudget__period', 'pfi',
            'pfi__structure')\
        .annotate(enveloppe=F('naturecomptablerecette__enveloppe'))\
        .order_by('annee', 'structure',
                  'naturecomptablerecette__code_nature_comptable',
                  'periodebudget__period__order',
                  'virement__document_number')

    # Depenses and recettes per year for the resume template
    year_depenses = depenses.values(
            'annee', 'enveloppe', 'periodebudget__period__code',
            'periodebudget__period__order')\
        .annotate(
            sum_dc=Sum('montant_dc'),
            sum_ae=Sum('montant_ae'),
            sum_cp=Sum('montant_cp')).order_by('periodebudget__period__order')
    year_recettes = recettes.values(
            'annee', 'enveloppe', 'periodebudget__period__code',
            'periodebudget__period__order')\
        .annotate(
            sum_dc=Sum('montant_dc'),
            sum_ar=Sum('montant_ar'),
            sum_re=Sum('montant_re')).order_by('periodebudget__period__order')

    depenses = to_dict(groupby(depenses, lambda x: x.annee))
    recettes = to_dict(groupby(recettes, lambda x: x.annee))
    years = depenses.keys() | recettes.keys()

    resume_depenses, resume_recettes = get_detail_pfi_by_period(
        [year_depenses, year_recettes])

    periods = PeriodeBudget.objects.filter(annee=current_year)\
        .order_by('period__order').values_list('period__code', flat=True)

    context = {
        'cf': structparent, 'currentYear': current_year,
        'resume_depenses': resume_depenses, 'resume_recettes': resume_recettes,
        'years': years, 'periods': periods
    }

    if structparent.depth > 2 or\
            structparent.get_first_ancestor().code != "1010":
        sum_depenses = Depense.objects.filter(**queryset).values('annee').annotate(
            sum_dc=Sum('montant_dc'),
            sum_ae=Sum('montant_ae'),
            sum_cp=Sum('montant_cp'))
        sum_depenses = to_dict(groupby(sum_depenses, lambda x: x['annee']))
        sum_recettes = Recette.objects.filter(**queryset).values('annee').annotate(
            sum_dc=Sum('montant_dc'),
            sum_ar=Sum('montant_ar'),
            sum_re=Sum('montant_re'))
        sum_recettes = to_dict(groupby(sum_recettes, lambda x: x['annee']))
        context.update({
            'listeDepense': depenses, 'listeRecette': recettes,
            'sommeDepense': sum_depenses, 'sommeRecette': sum_recettes
        })

    return render(request, 'detailscf.html', context)


def set_year(request):
    """
    Redirect to a given url while setting the chosen year in the session.
    The url and year need to be specified in the request parameters.

    This view is based on django.viwes.i18n.set_language
    """
    next = request.POST.get('next', request.GET.get('next'))
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    response = HttpResponseRedirect(next)
    if request.method == 'POST':
        year = request.POST.get('year', None)
        request.session['period_year'] = int(year)
    return response


@requires_csrf_token
def handler500(request, template_name='500.html'):  # pragma: no cover
    import sys
    import traceback
    #copy of django.views.defaults.server_error
    exctype, value, tb = sys.exc_info()
    t = loader.get_template(template_name)
    return HttpResponseServerError(t.render(
        Context({
            'error': value.message if hasattr(value, 'message') else value,
            'type': exctype.__name__,
            'tb': traceback.format_exception(exctype, value, tb)
        })
    ))


@staff_member_required
def migrate_pluriannuel(request, period_id):
    try:
        period = get_object_or_404(PeriodeBudget, pk=period_id)
        if period.has_entries():
            msg = _('There are already pluriannual entries for this period')
            messages.add_message(request, messages.ERROR, msg)
        else:
            management.call_command(
                'migrate_pluriannuel', str(period.annee), '-v 0')
            msg = _('Migration done')
            messages.add_message(request, messages.INFO, msg)
    except Exception as e:
        msg = 'Error in the migration : %s' % e
        messages.add_message(request, messages.ERROR, msg)

    return redirect('/admin/budgetweb/periodebudget/%s' % period_id)
