# -*- coding: utf-8 -*-

from functools import partial, wraps

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.shortcuts import render, render_to_response


#from django.template import RequestContext
#from datetime import datetime
from django.shortcuts import get_object_or_404, redirect

#import json
#from django.http import Http404,HttpResponse
##--------------------------------------------------------------------
#from django.contrib.auth.models import User
#
#from django.contrib.auth.models import Group
#from django.forms.formsets import formset_factory
#from django.contrib import messages
#from django.core.urlresolvers import reverse


from budgetweb.libs.node import generateTree
from .forms import (BaseRecetteFormSet, DepenseForm, PlanFinancementPluriForm,
                    RecetteForm)
from .models import (Authorisation, Depense, DomaineFonctionnel, PeriodeBudget,
                     PlanFinancement, Recette, Structure)

# logging
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------------

# def search(request):
#    pass
#
# --------------------------------------


# @login_required
def home(request):
    return render_to_response('base.html')


def current_budget():
    return PeriodeBudget.objects.filter(is_active=True).first()\
        if PeriodeBudget.objects.filter(is_active=True).first()\
        else 'Pas de période de budget ouverte'
#
#"""-------------------------------------------------
# class Authorisation(models.Model):
#
#-----------------------------------------------------"""


@login_required
def authorisation_list(request):
    """
    Fonction qui affiche la liste des autorisations
    Le formulaire à un searchform pour restreindre l affichage
    """
    myauth = Authorisation.objects.all()
    if request.method == "POST":
        user = request.POST['name']
        obj = request.POST['object']
        if user:
            myauth = myauth.filter(myobject__icontains=user)
        if obj:
            myauth = myauth.objects.filter(username__icontains=obj)

    return render(
        request, 'authorisation_lists.html', {'Authorisations': myauth})


#"""-------------------------------------------------
#Fonction qui renvoie la liste des autorisations pour un utilisateur
#-------------------------------------------------"""
#@login_required
#def authorisation_user(request,myuser=""):
#    mytauth=Authorisation.objects.filter(username=myuser)
#    return render(equest, 'authorisation_lists.html', {'Authorisation':myauth})
#
#
#"""-------------------------------------------------
#Fonction qui prend en parametres:
#un utilisateur précis
#un objet précis
#Fonction qui renvoie 0 si pas d'autorisation pour un objet
#-------------------------------------------------"""
#@login_required
#def is_authorised(myuser, myobject):
#    # chercher les autorisations dans la table
#    # si il y a * dans la table, ok tout
#    # si il y a qqch* alors detailler
#    # si autorisation exacte ok
#    thecount1=Authorisation.objects.filter(username=myuser).filter(myobject='*').count()
#    if thecount1 >0:
#        return thecount1
#    else:
#        a1=Authorisation.objects.filter(
#              username=myuser)
#        myobject=myobject.strip()
#        a2=a1.filter(myobject=myobject
#                 )
#        thecount=a2.count()
#
#        if thecount > 0:
#            return thecount
#        else:
#            #decouper
#            i=0
#            found=0
#            while (i < len(myobject)) and (found == 0):
#                myobjectsubstr = myobject[0:i]
#                a2=a1.filter(myobject__startswith=myobjectsubstr)
#                for o in a2:
#                    j=i+1
#                    if len(o.myobject)>=j and o.myobject[i:j] == '*':
#                        found=1
#                        print('* match autorisation for '+ myuser +'::'+myobject+'::'+o.myobject+'::'+o.myobject[i:j])
#                        return found
#                i+=1
#            return found
#
#

#"""------------------------------------------------------------------
#Liste des structure CF/CC/CP
#------------------------------------------------------------------"""
#@login_required
#def structure_list(request):
#    if request.method == "POST":
#        stname = request.POST['stname']
#        stlabel = request.POST['stlabel']
#        if stname == "" and stlabel == "":
#            myst = Structure.objects.all()
#        elif stname == "":
#            myst = Structure.objects.filter(label__icontains=stlabel)
#        elif stlabel == "":
#            myst = Structure.objects.filter(name__icontains=stname)
#        else:
#            myst = Structure.objects.filter(label__icontains=stlabel) \
#                .filter(name__icontains=stname)
#    else:
#        myst = Structure.objects.all()
#
#    return render(request, 'structure_lists.html', {'reponses': myst})
#
#
#def structure_list2(request):
#    myst = Structure.objects.filter(parent=None)
#
#    return render(request, 'structure_lists_arbomain.html', {'reponses': myst})


#
#
# @login_required
# def structure_set_parent(request):
#    mystructures = Structure.objects.all()
#    for child in mystructures:
#        child.parent=Structure.objects.filter(myid=child.parentid).first()
#        child.save()
#
#    return render(request, 'structure_lists.html', {'reponses':mystructures})
#

@login_required
def liste_pfi_avec_depenses_recettes(request):
    mypfi = PlanFinancement.objects.order_by('societe','cfassoc','ccassoc','cpassoc','myid')
    mydepenses = Depense.objects.all()
    myrecettes = Recette.objects.all()
    return render(request, 'planfinancementavecdeprec_lists.html', {'reponses':mypfi,'depenses':mydepenses,'recettes':myrecettes})


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
                                             'typeAffichage': type_affichage})


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
                                somme=Sum('montantAE'))
        pfi['sommeDepenseCP'] = Depense.objects.filter(
                                pfi__id=pfi['id']).aggregate(
                                somme=Sum('montantCP'))
        pfi['sommeDepenseDC'] = Depense.objects.filter(
                                pfi__id=pfi['id']).aggregate(
                                somme=Sum('montantDC'))
        pfi['sommeRecetteAR'] = Recette.objects.filter(
                                pfi__id=pfi['id']).aggregate(
                                somme=Sum('montantAR'))
        pfi['sommeRecetteRE'] = Recette.objects.filter(
                                pfi__id=pfi['id']).aggregate(
                                somme=Sum('montantRE'))
        pfi['sommeRecetteDC'] = Recette.objects.filter(
                                pfi__id=pfi['id']).aggregate(
                                somme=Sum('montantDC'))

    context = {'listeCF': listeCF, 'listePFI': listePFI,
               'typeAffichage': type_affichage}
    return render(request, 'show_sub_tree.html', context)


@login_required
def pluriannuel(request, pfiid):
    pfi = get_object_or_404(PlanFinancement, pk=pfiid)
    if request.method == "POST":
        form = PlanFinancementPluriForm(request.POST, instance=pfi)
        if form.is_valid():
            print(form)
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
    context = {'PFI': pfi, 'form': form, 'rangeYear': sorted(range_year)}
    return render(request, 'pluriannuel.html', context)


def modelformset_factory_with_kwargs(cls, **formset_kwargs):
    class ModelformsetFactoryWithKwargs(cls):
        def __init__(self, *args, **kwargs):
            kwargs.update(formset_kwargs)
            super().__init__(*args, **kwargs)
    return ModelformsetFactoryWithKwargs


@login_required
def depense(request, pfiid):
    pfi = PlanFinancement.objects.get(pk=pfiid)
    periodebudget = PeriodeBudget.objects.filter(is_active=True).first()
    DepenseFormSet = modelformset_factory(
        Depense,
        form=modelformset_factory_with_kwargs(DepenseForm, pfi=pfi,
                                              periodebudget=periodebudget),
        exclude=[],
        extra=3
    )
    formset = DepenseFormSet(queryset=Depense.objects.filter(pfi=pfi))
    if request.method == "POST":
        formset = DepenseFormSet(request.POST)
        if formset.is_valid():
            for data in formset.cleaned_data:
                if data:
                    obj = Depense(**data)
                    obj.save()
        else:
            print('EEE : %s' % formset.errors)

    context = {
        'test': 'TEST',
        'PFI': pfi,
        'formset': formset
    }
    return render(request, 'depense.html', context)


@login_required
def recette(request, pfiid):
    pfi = PlanFinancement.objects.get(pk=pfiid)
    periodebudget = PeriodeBudget.objects.filter(is_active=True).first()
    RecetteFormSet = modelformset_factory(
        Recette,
        form=modelformset_factory_with_kwargs(RecetteForm, pfi=pfi,
                                              periodebudget=periodebudget),
        exclude=[],
        extra=3
    )
    formset = RecetteFormSet(queryset=Recette.objects.filter(pfi=pfi))
    if request.method == "POST":
        formset = RecetteFormSet(request.POST)
        if formset.is_valid():
            for data in formset.cleaned_data:
                if data:
                    obj = Recette(**data)
                    print(obj)
                    obj.save()
        else:
            print('EEE : %s' % formset.errors)

    context = {
        'test': 'TEST',
        'PFI': pfi,
        'formset': formset
    }
    return render(request, 'recette.html', context)
