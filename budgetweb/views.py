# -*- coding: utf-8 -*-

from collections import OrderedDict
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Sum
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)

from .decorators import is_ajax_get, is_authorized_structure
from .forms import DepenseForm, PlanFinancementPluriForm, RecetteForm
from .models import (Depense, NatureComptableDepense, NatureComptableRecette,
                     PeriodeBudget, PlanFinancement, Recette, Structure,
                     StructureAuthorizations, StructureMontant)
from .utils import get_authorized_structures_ids, get_current_year
from decimal import Decimal


# @login_required
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
    ).order_by('code_nature_comptable')
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
    nature = models[model].active.filter(id=id_nature).first()
    response_data = [
        {"code_compte_budgetaire": nature.code_compte_budgetaire,
         "label_compte_budgetaire": nature.label_compte_budgetaire}
                    ]
    return HttpResponse(
        json.dumps(response_data), content_type='application/json')


@login_required
def show_tree(request, type_affichage, structid=None):
    # Authorized structures list
    queryset = {'parent__code': structid} if structid else {'parent': None}
    authorized_structures = get_authorized_structures_ids(
        request.user, hierarchy=True)
    structures = Structure.objects.prefetch_related(Prefetch(
        'structuremontant_set',
        queryset=StructureMontant.active_period.all(),
        to_attr='montants')
    ).filter(pk__in=authorized_structures, **queryset).order_by('code')

    # PFI list
    pfis = PlanFinancement.objects.filter(structure__code=structid)\
        .annotate(
            sum_depense_ae=Sum('depense__montant_ae'),
            sum_depense_cp=Sum('depense__montant_cp'),
            sum_depense_dc=Sum('depense__montant_dc'),
            sum_recette_ar=Sum('recette__montant_ar'),
            sum_recette_re=Sum('recette__montant_re'),
            sum_recette_dc=Sum('recette__montant_dc')
        )

    context = {
        'structures': structures,
        'pfis': pfis,
        'typeAffichage': type_affichage,
        'currentYear': get_current_year
    }

    template = 'show_sub_tree.html' if request.is_ajax() else 'showtree.html'
    return render(request, template, context)


@login_required
@is_authorized_structure
def pluriannuel(request, pfiid):
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
        depense, recette = pfi.get_total_types()
    else:
        depense = recette = {}

    context = {
        'PFI': pfi, 'form': form, 'depense': depense, 'recette': recette,
        'currentYear': get_current_year, 'years': pfi.get_years()
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
def depense(request, pfiid, annee):
    pfi = PlanFinancement.objects.get(pk=pfiid)
    periodebudget = PeriodeBudget.objects.filter(is_active=True).first()
    DepenseFormSet = modelformset_factory(
        Depense,
        form=modelformset_factory_with_kwargs(DepenseForm, pfi=pfi,
                                              periodebudget=periodebudget,
                                              annee=annee,
                                              user=request.user),
        exclude=[],
        extra=1,
        can_delete=True
    )
    formset = DepenseFormSet(queryset=Depense.objects.filter(pfi=pfi,
                                                             annee=annee).order_by('naturecomptabledepense__priority', '-montant_ae'))
    if request.method == "POST":
        formset = DepenseFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/detailspfi/%s' % pfi.pk)

    context = {
        'PFI': pfi,
        'formset': formset,
        'currentYear': get_current_year,
        'form_template': 'depense.html'
    }
    return render(request, 'comptabilite.html', context)


@login_required
@is_authorized_structure
def recette(request, pfiid, annee):
    pfi = PlanFinancement.objects.get(pk=pfiid)
    periodebudget = PeriodeBudget.objects.filter(is_active=True).first()
    RecetteFormSet = modelformset_factory(
        Recette,
        form=modelformset_factory_with_kwargs(RecetteForm, pfi=pfi,
                                              periodebudget=periodebudget,
                                              annee=annee,
                                              user=request.user),
        exclude=[],
        extra=1,
        can_delete=True
    )
    formset = RecetteFormSet(queryset=Recette.objects.filter(pfi=pfi,
                                                             annee=annee).order_by('naturecomptablerecette__priority', '-montant_ar'))
    if request.method == "POST":
        formset = RecetteFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/detailspfi/%s' % pfi.pk)

    context = {
        'PFI': pfi,
        'formset': formset,
        'currentYear': get_current_year,
        'form_template': 'recette.html'
    }
    return render(request, 'comptabilite.html', context)


@login_required
@is_authorized_structure
def detailspfi(request, pfiid):
    pfi = PlanFinancement.objects.get(pk=pfiid)

    # A completer.
    listeDepenseRecette = pfi.get_total()

    listeDepense = Depense.objects.filter(
        pfi=pfi).prefetch_related(
            'naturecomptabledepense', 'periodebudget', 'pfi', 'pfi__structure'
        ).order_by('naturecomptabledepense__priority')
    listeRecette = Recette.objects.filter(
        pfi=pfi).prefetch_related(
            'naturecomptablerecette', 'periodebudget', 'pfi', 'pfi__structure'
        ).order_by('naturecomptablerecette__priority')
    sommeDepense = listeDepense.aggregate(sommeDC=Sum('montant_dc'),
                                          sommeAE=Sum('montant_ae'),
                                          sommeCP=Sum('montant_cp'))
    sommeRecette = listeRecette.aggregate(sommeDC=Sum('montant_dc'),
                                          sommeAR=Sum('montant_ar'),
                                          sommeRE=Sum('montant_re'))

    context = {
        'PFI': pfi, 'currentYear': get_current_year,
        'listeDepense': listeDepense, 'listeRecette': listeRecette,
        'sommeDepense': sommeDepense, 'sommeRecette': sommeRecette,
        'listeDepenseRecette': listeDepenseRecette,
    }
    return render(request, 'detailsfullpfi.html', context)


@login_required
def detailscf(request, structid):
    structparent = Structure.objects.get(id=structid)
    liste_structure = structparent.get_children()
    liste_structure.insert(0, structparent)
    liste_depense = []
    liste_recette = []
    somme_depense = { 'sommeAE' : Decimal(0.00), 'sommeCP': Decimal(0.00), 'sommeDC': Decimal(0.00)}
    somme_recette = { 'sommeAR' : Decimal(0.00), 'sommeRE': Decimal(0.00), 'sommeDC': Decimal(0.00)}
    for struct in liste_structure:
        liste_pfi = PlanFinancement.objects.filter(structure=struct.pk)
        for pfi in liste_pfi:
            listeDepense = Depense.objects.filter(
                        pfi=pfi).prefetch_related('naturecomptabledepense')\
                                .prefetch_related('periodebudget')\
                                .prefetch_related('pfi')\
                                .prefetch_related('pfi__structure')\
                                .order_by('naturecomptabledepense__priority')
            listeRecette = Recette.objects.filter(
                        pfi=pfi).prefetch_related('naturecomptablerecette')\
                                .prefetch_related('periodebudget')\
                                .prefetch_related('pfi')\
                                .prefetch_related('pfi__structure')\
                                .order_by('naturecomptablerecette__priority')
            sommeDepense = listeDepense.aggregate(sommeDC=Sum('montant_dc'),
                                                  sommeAE=Sum('montant_ae'),
                                                  sommeCP=Sum('montant_cp'))
            sommeRecette = listeRecette.aggregate(sommeDC=Sum('montant_dc'),
                                                  sommeAR=Sum('montant_ar'),
                                                  sommeRE=Sum('montant_re'))
            for key, values in sommeDepense.items():
                if values is not None:
                    somme_depense[key] += Decimal(values)
            for key, values in sommeRecette.items():
                if values is not None:
                    somme_recette[key] += Decimal(values)
            liste_depense += listeDepense
            liste_recette += listeRecette
            # somme_depense += sommeDepense
            # somme_recette += sommeRecette

    context = {
        'currentYear': get_current_year,
        'listeDepense': liste_depense, 'listeRecette': liste_recette,
        'sommeDepense': somme_depense, 'sommeRecette': somme_recette,
    }
    return render(request, 'detailscf.html', context)
