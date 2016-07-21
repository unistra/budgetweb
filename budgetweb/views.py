# -*- coding: utf-8 -*-

from collections import OrderedDict
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)

from .decorators import is_ajax_get, is_authorized_structure
from .forms import DepenseForm, PlanFinancementPluriForm, RecetteForm
from .models import (Depense, NatureComptableDepense, NatureComptableRecette,
                     PeriodeBudget, PlanFinancement, Recette, Structure,
                     StructureMontant)
from .utils import getCurrentYear


# @login_required
def home(request):
    return redirect('show_tree', type_affichage='gbcp')


# AJAX
@is_ajax_get
def api_fund_designation_by_nature_and_enveloppe(request, model, enveloppe, pfiid):
    pfi = PlanFinancement.objects.get(pk=pfiid)
    models = {
        'naturecomptablerecette': NatureComptableRecette,
        'naturecomptabledepense': NatureComptableDepense,
    }
    natures = models[model].active.filter(
        is_fleche=pfi.is_fleche, enveloppe=enveloppe)
    response_data = [
        {"id": nature.pk, "label": str(nature)} for nature in natures]
    return HttpResponse(
        json.dumps(response_data), content_type='application/json')


@login_required
def show_tree(request, type_affichage, structid=None):
    queryset = {'parent__code': structid} if structid else {'parent': None}
    structures = OrderedDict(
        [(s.pk, {'structure': s}) for s in Structure.objects.filter(
            **queryset).order_by('code')
        ]
    )

    # TODO: select_related ?

    # Et enfin on ajoute les PFI, si jamais il y en a.
    liste_pfi = PlanFinancement.objects.filter(
        structure__code=structid).values()

    cf_montants = StructureMontant.objects.filter(
        structure__pk__in=structures.keys())
    for cf_montant in cf_montants:
        structures[cf_montant.structure.pk]['montants'] = cf_montant

    for pfi in liste_pfi:
        pfi['sommeDepenseAE'] = Depense.objects.filter(
                                pfi__id=pfi['id']).aggregate(
                                somme=Sum('montant_ae'))
        pfi['sommeDepenseCP'] = Depense.objects.filter(
                                pfi__id=pfi['id']).aggregate(
                                somme=Sum('montant_cp'))
        pfi['sommeDepenseDC'] = Depense.objects.filter(
                                pfi__id=pfi['id']).aggregate(
                                somme=Sum('montant_dc'))
        pfi['sommeRecetteAR'] = Recette.objects.filter(
                                pfi__id=pfi['id']).aggregate(
                                somme=Sum('montant_ar'))
        pfi['sommeRecetteRE'] = Recette.objects.filter(
                                pfi__id=pfi['id']).aggregate(
                                somme=Sum('montant_re'))
        pfi['sommeRecetteDC'] = Recette.objects.filter(
                                pfi__id=pfi['id']).aggregate(
                                somme=Sum('montant_dc'))

    context = {
        'structures': structures,
        'listePFI': liste_pfi,
        'typeAffichage': type_affichage,
        'currentYear': getCurrentYear
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

    # On a une date de debut et de fin, on prépare un tableau
    range_year = {}
    if pfi.date_debut and pfi.date_fin:
        start = pfi.date_debut.year
        while start <= pfi.date_fin.year:
            range_year[start] = True
            start = start + 1
    context = {'PFI': pfi, 'form': form,
               'rangeYear': sorted(range_year),
               'currentYear': getCurrentYear}
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
                                              annee=annee),
        exclude=[],
        extra=1,
        can_delete=True
    )
    formset = DepenseFormSet(queryset=Depense.objects.filter(pfi=pfi))
    if request.method == "POST":
        formset = DepenseFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/detailspfi/%s' % pfi.pk)

    context = {
        'PFI': pfi,
        'formset': formset,
        'currentYear': getCurrentYear,
    }
    return render(request, 'depense.html', context)


@login_required
@is_authorized_structure
def recette(request, pfiid, annee):
    pfi = PlanFinancement.objects.get(pk=pfiid)
    periodebudget = PeriodeBudget.objects.filter(is_active=True).first()
    RecetteFormSet = modelformset_factory(
        Recette,
        form=modelformset_factory_with_kwargs(RecetteForm, pfi=pfi,
                                              periodebudget=periodebudget,
                                              annee=annee),
        exclude=[],
        extra=1,
        can_delete=True
    )
    formset = RecetteFormSet(queryset=Recette.objects.filter(pfi=pfi))
    if request.method == "POST":
        formset = RecetteFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/detailspfi/%s' % pfi.pk)

    context = {
        'PFI': pfi,
        'formset': formset,
        'currentYear': getCurrentYear,
    }
    return render(request, 'recette.html', context)


@login_required
@is_authorized_structure
def detailspfi(request, pfiid):
    pfi = PlanFinancement.objects.get(pk=pfiid)
    listeDepense = Depense.objects.filter(
        pfi=pfi).prefetch_related('naturecomptabledepense').prefetch_related('periodebudget')
    listeRecette = Recette.objects.filter(
        pfi=pfi).prefetch_related('naturecomptablerecette').prefetch_related('periodebudget')
    sommeDepense = listeDepense.aggregate(sommeDC=Sum('montant_dc'),
                                          sommeAE=Sum('montant_ae'),
                                          sommeCP=Sum('montant_cp'))
    sommeRecette = listeRecette.aggregate(sommeDC=Sum('montant_dc'),
                                          sommeAR=Sum('montant_ar'),
                                          sommeRE=Sum('montant_re'))
    context = {
        'PFI': pfi, 'currentYear': getCurrentYear,
        'listeDepense': listeDepense, 'listeRecette': listeRecette,
        'sommeDepense': sommeDepense, 'sommeRecette': sommeRecette,
    }
    return render(request, 'detailsfullpfi.html', context)
