# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)


from budgetweb.libs.node import getCurrentYear, generateTree
from .forms import DepenseForm, PlanFinancementPluriForm, RecetteForm
from .models import (Depense, PeriodeBudget, PlanFinancement, Recette,
                     Structure)

# logging
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


# @login_required
def home(request):
    return redirect('show_tree', type_affichage='gbcp')


#---------------------------------------------------------
# AJAX
#--------------------------------------------------------

#def ajax_add_eotp(request,pkstr1):
#    if request.is_ajax():
#        myname=Structure.objects.get(id=pkstr1).name
#        myname=myname.strip()
#
#        planfi = PlanFinancement.objects.filter(cfassoc=myname,pluriannuel=False)
#        todo_items=[]
#
#        for s in planfi:
#            todo_items.append(str(s.id)+"-----"+str(s.name))
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
#
##Pour les recettes
#def ajax_add_enveloppe(request,pkstr1,lenveloppe):
#    recette='rec'
#    if request.is_ajax():
#        isfleche=PlanFinancement.objects.get(id=pkstr1).fleche
#        naturecompta = NatureComptable.objects.filter(pfifleche=isfleche,nctype=recette,enveloppe=lenveloppe)
#        todo_items=[]
#        for s in naturecompta:
#            todo_items.append(
#                '{0.id}-----{0.enveloppe}-----{0.fondbudget_recette}-----{0.ccbd}'.format(s))
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
##pour les depenses
#def ajax_recette_displaycompte(request,pkstr1):
#    if request.is_ajax():
#        naturecompta = NatureComptable.objects.get(id=pkstr1)
#        todo_items=[]
#        todo_items.append(str(naturecompta.ccbd))
#
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
#
#
#
##Pour les recettes
#def ajax_add_enveloppetype(request,pkstr1):
#    recette='rec'
#    if request.is_ajax():
#        isfleche=PlanFinancement.objects.get(id=pkstr1).fleche
#        naturecompta = NatureComptable.objects.filter(pfifleche=isfleche,nctype=recette)
#        todo_items=[]
#        for s in naturecompta:
#            if not (s.enveloppe in todo_items ):
#                      todo_items.append(str(s.enveloppe))
#
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
#
##Pour les depenses
#def ajax_add_enveloppetype_depense(request,pkstr1):
#    depense='dep'
#    if request.is_ajax():
#        isfleche=PlanFinancement.objects.get(id=pkstr1).fleche
#        naturecompta = NatureComptable.objects.filter(pfifleche=isfleche,nctype=depense)
#        todo_items=[]
#        for s in naturecompta:
#            if not (s.enveloppe in todo_items ):
#                todo_items.append(str(s.enveloppe))
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
#def ajax_add_enveloppe_depense(request,pkstr1,lenveloppe):
#    #print ("calling_add_enveloppe pour::" + str(pkstr1))
#    depense='dep'
#    if request.is_ajax():
#        isfleche=PlanFinancement.objects.get(id=pkstr1).fleche
#        naturecompta = NatureComptable.objects.filter(pfifleche=isfleche,nctype=depense,enveloppe=lenveloppe)
#        todo_items=[]
#        for s in naturecompta:
#            todo_items.append(str(s.id)+"-----"+str(s.enveloppe)+"-----"+str(s.naturec_dep)+str(s.ccbd))
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
##Pour les depenses
#def ajax_get_enveloppe_decalage(request,pkstr1):
#    depense='dep'
#    print("go")
#    if request.is_ajax():
#        naturec=NatureComptable.objects.get(id=pkstr1)
#        print("Nature C: "+ str(naturec))
#        print(str(naturec.decalagetresocpae))
#        decalageyesno=str(naturec.decalagetresocpae)
#        print("on decale ou pas:" + decalageyesno)
#        todo_items=[]
#        todo_items.append(decalageyesno)
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404


@login_required
def show_tree(request, type_affichage):
    listeCF = generateTree(request)
    return render(request, 'showtree.html', {'listeCF': listeCF,
                                             'typeAffichage': type_affichage,
                                             'currentYear': getCurrentYear})


@login_required
def show_sub_tree(request, type_affichage, structid):

    # On récupère l'ID sur PAPA
    structure = Structure.objects.get(code=structid)
    # On récupère la liste des CF fils.
    listeCF = Structure.objects.filter(parent=structure)
    # print('LCF : %s' % listeCF)

    # Et enfin on ajoute les PFI, si jamais il y en a.
    listePFI = PlanFinancement.objects.filter(structure=structure).values()
    for pfi in listePFI:
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

    context = {'listeCF': listeCF, 'listePFI': listePFI,
               'typeAffichage': type_affichage,
               'currentYear': getCurrentYear}
    return render(request, 'show_sub_tree.html', context)


@login_required
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
        else:
            print('EEE : %s' % formset.errors)

    context = {
        'PFI': pfi,
        'formset': formset,
        'currentYear': getCurrentYear,
    }
    return render(request, 'depense.html', context)


@login_required
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
        else:
            print('EEE : %s' % formset.errors)

    context = {
        'PFI': pfi,
        'formset': formset,
        'currentYear': getCurrentYear,
    }
    return render(request, 'recette.html', context)


@login_required
def detailspfi(request, pfiid):
    pfi = PlanFinancement.objects.get(pk=pfiid)
    listeDepense = Depense.objects.filter(
        pfi=pfi).prefetch_related('naturecomptabledepense')
    listeRecette = Recette.objects.filter(
        pfi=pfi).prefetch_related('naturecomptablerecette')
    sommeDepense = listeDepense.aggregate(sommeDC=Sum('montant_dc'),
                                          sommeAE=Sum('montant_ae'),
                                          sommeCP=Sum('montant_cp'))
    sommeRecette = listeRecette.aggregate(sommeDC=Sum('montant_dc'),
                                          sommeAR=Sum('montant_ar'),
                                          sommeRE=Sum('montant_re'))
    context = {
        'PFI': pfi,
        'listeDepense': listeDepense, 'listeRecette': listeRecette,
        'sommeDepense': sommeDepense, 'sommeRecette': sommeRecette,
    }
    return render(request, 'detailsfullpfi.html', context)
