# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.forms.models import modelformset_factory
from django.shortcuts import render, render_to_response

from django.forms import formset_factory

#from django.template import RequestContext
#from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
#
#from .forms import (AuthorisationForm, NatureComptableForm, DomaineFonctionnelForm,
#                   StructureForm, PlanFinancementForm,
#                   DepenseFullForm, RecetteFullForm, PeriodeBudgetForm, CompteBudgetForm,
#                   RecetteFullFormPfifleche, RecetteFullFormPfinonfleche, RecetteFullFormRestrict,
#                   DepenseFullFormPfifleche, DepenseFullFormPfinonfleche, DepenseFullFormRestrict,
#                   ComptaNatureForm, FondBudgetaireForm, BaseDepenseFullFormSet, BaseRecetteFullFormSet)
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
from .forms import (BaseDepenseFullFormSet,  # BaseRecetteFullFormSet,
                    DepenseForm, PlanFinancementPluriForm,
                    DepenseFormPfi, RecetteForm, RecetteFormPfi)
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

"""------------------------------------------------------------------
Liste des structure CF/CC/CP
------------------------------------------------------------------"""
@login_required
def structure_list(request):
    if request.method == "POST":
        stname = request.POST['stname']
        stlabel = request.POST['stlabel']
        if stname == "" and stlabel == "":
            myst = Structure.objects.all()
        elif stname == "":
            myst = Structure.objects.filter(label__icontains=stlabel)
        elif stlabel == "":
            myst = Structure.objects.filter(name__icontains=stname)
        else:
            myst = Structure.objects.filter(label__icontains=stlabel) \
                .filter(name__icontains=stname)
    else:
        myst = Structure.objects.all()

    return render(request, 'structure_lists.html', {'reponses': myst})


def structure_list2(request):
    myst = Structure.objects.filter(parent=None)

    return render(request, 'structure_lists_arbomain.html', {'reponses': myst})


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
#
#
#""" -----------------------------------------------------------------
#Création depenses dans le budget - en cours de tests
#Les structures sont classées les unes par rapport aux autres : Un CF depend
#d un autre CF - jusqu au CF Racine
#En dépenses on prend les types dep
#------------------------------------------------------------------- """
#
#@login_required
#def depensefull_new_avec_pfi(request,struct3id,pfiid):
#    """---------------------------------------------
#    Avec le formulaire prérempli .
#    -----------------------------------------------"""
#    budget = PeriodeBudget.objects.filter(bloque=False).first()
#    error = ''
#    if request.method == "POST":
#        #struct1 = Structure.objects.filter(id=request.POST.get("structlev1")).first()
#        #struct2 = Structure.objects.filter(id=request.POST.get("structlev2")).first()
#        struct3 = Structure.objects.filter(id=request.POST.get("structlev3")).first()
#
#        cptdev1 = NatureComptable.objects.filter(id=request.POST.get("cptdeplev1")).first()
#
#        if cptdev1 == None:
#            error = error + 'Veuillez choisir une enveloppe valide'
#        else:
#            domfonc = DomaineFonctionnel.objects.filter(id=request.POST.get("domfonc")).first()
#            plfi = PlanFinancement.objects.filter(id=request.POST.get("plfi")).first()
#
#            montantdc = request.POST.get("montantdc") if request.POST.get("montantdc") else 0
#            montantae = request.POST.get("montantae") if request.POST.get("montantae") else 0
#            montantcp = request.POST.get("montantcp") if request.POST.get("montantcp") else 0
#            string_date=request.POST.get("dateae")
#            dateae = datetime.datetime.strptime(string_date, "DD-MM-YYYY") if request.POST.get("dateae") else ''
#            myfile=request.POST.get("myfile") if request.POST.get("myfile") else ''
#            commentaire = request.POST.get("commentaire") if request.POST.get("commentaire") else ''
#
#            madepense = DepenseFull()
#            #madepense.structlev1 = struct1
#            #madepense.structlev2 = struct2
#            madepense.structlev3 = struct3
#            madepense.cptdeplev1 = cptdev1
#            madepense.domfonc = domfonc
#            madepense.plfi = plfi
#            madepense.montantdc = montantdc
#            madepense.montantae = montantae
#            madepense.dateae = dateae
#            madepense.montantcp = montantcp
#            madepense.commentaire = commentaire
#            madepense.myfile=myfile
#            madepense.periodebudget = budget
#            madepense.creepar = request.user.username
#            madepense.modifiepar = request.user.username
#
#            madepense.save()
#            madepense.myid = madepense.id
#            madepense.save()
#
#            localpkcc=madepense.structlev3.pk
#            return redirect('liste_pfi_avec_depenses_recettes')
#    else:
#        plfi = get_object_or_404(PlanFinancement,pk=pfiid)
#        struct3id=" "+struct3id
#        struct3 = get_object_or_404(Structure,name=struct3id,type=' cf')
#        struct2 = get_object_or_404(Structure,myid=struct3.parentid)
#        struct1 = get_object_or_404(Structure,myid=struct2.parentid)
#
#        domfoncs = DomaineFonctionnel.objects.all().order_by('dfcode') #filter(dfgrpcumul='LOLF_CUMUL')
#
#    return render(request, 'depensefull_new_v3.html', {
#                                                       'struct1': struct1,
#                                                       'struct2': struct2,
#                                                       'struct3': struct3,
#                                                       'domfoncs': domfoncs,
#                                                       'plfin':plfi,
#                                                       'error':error,
#                         })
#
#
#@login_required
#def depensefull_new_avec_pfi_cflink(request,struct3id,pfiid):
#    """---------------------------------------------
#    Avec le formulaire prérempli .
#    -----------------------------------------------"""
#
#    budget = PeriodeBudget.objects.filter(bloque=False).first()
#    plfi = get_object_or_404(PlanFinancement,pk=pfiid)
#    struct3 = get_object_or_404(Structure,id=struct3id)
#    domfoncs = DomaineFonctionnel.objects.all().order_by('dfcode') #filter(dfgrpcumul='LOLF_CUMUL')
#
#    error = ''
#    if request.method == "POST":
#        domfonc = DomaineFonctionnel.objects.filter(id=request.POST.get("domfonc")).first()
#
#        cptdev1 = NatureComptable.objects.filter(id=request.POST.get("cptdeplev1")).first()
#        if cptdev1 == None :
#            error = error + 'Veuillez choisir un type d enveloppe et une enveloppe valide'
#        elif not (request.POST.get("montantdc")):
#            error = error + 'Veuillez saisir un montant DC'
#        elif not (request.POST.get("montantcp")):
#            error = error + 'Veuillez saisir le montant du credit de paiement'
#
#        else:
#            string_date=request.POST.get("dateae")
#
#            if string_date == '':
#                dateae=None
#            else:
#                if string_date == '':
#                    dateae=None
#                else:
#                    try:
#                        dateae = datetime.datetime.strptime(string_date, '%d-%m-%Y')
#                    except ValueError:
#                        return render(request, 'depensefull_new_v3.html', {'struct3': struct3,
#                                                       'domfoncs': domfoncs,
#                                                       'plfin':plfi,
#                                                       'error':error,})
#
#
#            domfonc = DomaineFonctionnel.objects.filter(id=request.POST.get("domfonc")).first()
#
#            plfi = PlanFinancement.objects.filter(id=request.POST.get("plfi")).first()
#
#            montantdc = request.POST.get("montantdc") if request.POST.get("montantdc") else 0
#            montantae = request.POST.get("montantae") if request.POST.get("montantae") else 0
#            montantcp = request.POST.get("montantcp") if request.POST.get("montantcp") else 0
#
#            domfonc = DomaineFonctionnel.objects.filter(id=request.POST.get("domfonc")).first()
#
#            plfi = PlanFinancement.objects.filter(id=request.POST.get("plfi")).first()
#
#            montantdc = request.POST.get("montantdc") if request.POST.get("montantdc") else 0
#            montantae = request.POST.get("montantae") if request.POST.get("montantae") else 0
#            montantcp = request.POST.get("montantcp") if request.POST.get("montantcp") else 0
#
#            commentaire = request.POST.get("commentaire") if request.POST.get("commentaire") else ''
#            myfile = request.POST.get("myfile") if request.POST.get("myfile") else ''
#
#            madepense = DepenseFull()
#            madepense.structlev3 = struct3
#            madepense.cptdeplev1 = cptdev1
#            madepense.domfonc = domfonc
#            madepense.plfi = plfi
#            madepense.montantdc = montantdc
#            madepense.montantae = montantae
#            madepense.dateae = dateae
#            madepense.montantcp = montantcp
#            madepense.commentaire = commentaire
#            madepense.myfile = myfile
#            madepense.periodebudget = budget
#            madepense.creepar = request.user.username
#            madepense.modifiepar = request.user.username
#
#            madepense.save()
#            madepense.myid = madepense.id
#            madepense.save()
#
#            localpkcc=madepense.structlev3.pk
#            return redirect('liste_pfi_avec_depenses_recettes')
#
#    return render(request, 'depensefull_new_v3.html', {
#                                                       'struct3': struct3,
#                                                       'domfoncs': domfoncs,
#                                                       'plfin':plfi,
#                                                       'error':error,
#                         })
#
#
#
#@login_required
#def recettefull_new_avec_pfi_cflink(request,struct3id,pfiid):
#    """---------------------------------------------
#    Avec le formulaire prérempli .
#    -----------------------------------------------"""
#
#    budget = PeriodeBudget.objects.filter(bloque=False).first()
#    error = ''
#    if request.method == "POST":
#        struct3 = Structure.objects.filter(id=request.POST.get("structlev3")).first()
#
#        cptdev1 = NatureComptable.objects.filter(id=request.POST.get("cptdeplev1")).first()
#        df_rec_na= DomaineFonctionnel.objects.filter(dfcode='NA').first()
#
#        plfiid=request.POST.get("plfi")
#        plfi = PlanFinancement.objects.filter(id=plfiid).first()
#        if plfi == None:
#            error = 'Veuillez selectionner un  pfi'
#        elif (cptdev1 == None):
#            error = error + u'Veuillez saisir un type d enveloppe et une enveloppe'
#        elif not (request.POST.get("montantdc")):
#            error = error + u'Veuillez saisir un montant en droit constate'
#        elif not (request.POST.get("montantar")):
#            error = error + u'Veuillez saisir un montant AR'
#        elif not (request.POST.get("montantre")):
#            error = error + u'Veuillez saisir un montant RE'
#
#        else:
#            montantdc = request.POST.get("montantdc") if request.POST.get("montantdc") else 0
#            montantar = request.POST.get("montantar") if request.POST.get("montantar") else 0
#            montantre = request.POST.get("montantre") if request.POST.get("montantre") else 0
#            commentaire = request.POST.get("commentaire") if request.POST.get("commentaire") else ''
#            df_rec_na= DomaineFonctionnel.objects.filter(dfcode='NA').first()
#
#            marecette = RecetteFull()
#            marecette.structlev3 = struct3
#            marecette.cptdeplev1 = cptdev1
#            marecette.domfonc = df_rec_na
#            marecette.plfi = plfi
#            marecette.domfonc=df_rec_na
#            marecette.montantdc = montantdc
#            marecette.montantar = montantar
#            marecette.montantre = montantre
#            marecette.commentaire = commentaire
#            marecette.periodebudget=budget
#
#            marecette.creepar = request.user.username
#            marecette.modifiepar = request.user.username
#            marecette.save()
#            marecette.myid = marecette.id
#            marecette.save()
#            localpkcp=marecette.structlev3.pk
#            return redirect('liste_pfi_avec_depenses_recettes')
#    else:
#        plfi = get_object_or_404(PlanFinancement,pk=pfiid)
#        struct3 = get_object_or_404(Structure,id=struct3id,type=' cf')
#
#        #domfoncs = DomaineFonctionnel.objects.all().order_by('dfcode') #filter(dfgrpcumul='LOLF_CUMUL')
#        # le fond est calcule a partir de l enveloppe = nature comptable
#    return render(request, 'recettefull_new_v3.html', {
#                                                       'struct3': struct3,
#                                                       'plfin':plfi,
#                                                       'error':error,
#                         })
#
#
#

#""" -----------------------------------------------------------------
#Liste des depenses dans le budget associées à un CC
#------------------------------------------------------------------- """
#@login_required
#def depensefull_parcc(request,pkcc):
#    madep=Structure.objects.get(id=pkcc)
#    mydep = DepenseFull.objects.filter (structlev3=madep).order_by('structlev3')
#    total = DepenseFull.objects.filter (structlev3=madep).aggregate(Sum('montant'))
#    totaldc=DepenseFull.objects.filter (structlev3=madep).aggregate(Sum('montantdc'))
#    totalcp=DepenseFull.objects.filter (structlev3=madep).aggregate(Sum('montantcp'))
#    totalae=DepenseFull.objects.filter (structlev3=madep).aggregate(Sum('montantae'))
#    lev2 = Structure.objects.get(myid=madep.parentid)
#    lev1 = Structure.objects.get(myid=lev2.parentid)
#    return render(request, 'depensefullcc_lists.html', {'depenses':mydep, 'total':total , 'totaldc':totaldc, 'totalcp':totalcp,'totalae':totalae,'pkcc':pkcc,'mastructurelev1':lev1,'mastructurelev2':lev2,'mastructurelev3':madep})
#
#
#""" -----------------------------------------------------------------
#Liste des recettes dans le budget associées à un CP
#------------------------------------------------------------------- """
#@login_required
#def recettefull_parcp(request,pkcp):
#    madep=Structure.objects.get(id=pkcp)
#    myrec = RecetteFull.objects.filter (structlev3=madep).order_by('structlev3')
#    total=RecetteFull.objects.filter (structlev3=madep).aggregate(Sum('montant'))
#    totalar=RecetteFull.objects.filter (structlev3=madep).aggregate(Sum('montantar'))
#    totalre=RecetteFull.objects.filter (structlev3=madep).aggregate(Sum('montantre'))
#    totaldc=RecetteFull.objects.filter (structlev3=madep).aggregate(Sum('montantdc'))
#    return render(request, 'recettefullcp_lists.html', {'recettes':myrec, 'total':total, 'totaldc':totaldc ,
#                                         'totalar':totalar,'totalre':totalre,'pkcp':pkcp,
#                                         'mastructurelev3':madep})
#
#
#def depensefull_listregroup(request):
#    if request.method == "POST":
#        depstruct = request.POST['depstruct']
#        depcomptcompt = request.POST['depcomptcompt']
#        if depstruct == "" and depcomptcompt == "" :
#            mydep = DepenseFull.objects.all().order_by('structlev3')
#        elif depstruct == "" :
#            mydep = DepenseFull.objects.filter ( structure__icontains = depstruct ).order_by('structlev3')
#        elif depcomptcompt == "" :
#            mydep = DepenseFull.objects.filter ( cptdeplev1__icontains = depcomptcompt ).order_by('structlev3')
#        else:
#            mydep = DepenseFull.objects.filter( structure__icontains = depstruct ).filter( cptdeplev1__icontains = depcomptcompt ).order_by('structlev3')
#    else:
#        mydep = DepenseFull.objects.all().order_by('structlev3')
#
#    return render(request, 'depensefull_listsregroup.html', {'depenses':mydep})
#
#
#def total1(self):
#    qs=DepenseFull.objects.filter(id=self).aggregate(Sum('montant'))
#    sum=qs['amount__sum']
#    if not sum:
#        sum=0.00
#    return sum
#

#---------------------------------------------------------
# AJAX
#--------------------------------------------------------

def ajax_add_eotp(request,pkstr1):
    if request.is_ajax():
        myname=Structure.objects.get(id=pkstr1).name
        myname=myname.strip()

        planfi = PlanFinancement.objects.filter(cfassoc=myname,pluriannuel=False)
        todo_items=[]

        for s in planfi:
            todo_items.append(str(s.id)+"-----"+str(s.name))
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


#Pour les recettes
def ajax_add_enveloppe(request,pkstr1,lenveloppe):
    recette='rec'
    if request.is_ajax():
        isfleche=PlanFinancement.objects.get(id=pkstr1).fleche
        naturecompta = NatureComptable.objects.filter(pfifleche=isfleche,nctype=recette,enveloppe=lenveloppe)
        todo_items=[]
        for s in naturecompta:
            todo_items.append(
                '{0.id}-----{0.enveloppe}-----{0.fondbudget_recette}-----{0.ccbd}'.format(s))
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

#pour les depenses
def ajax_recette_displaycompte(request,pkstr1):
    if request.is_ajax():
        naturecompta = NatureComptable.objects.get(id=pkstr1)
        todo_items=[]
        todo_items.append(str(naturecompta.ccbd))

        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404




#Pour les recettes
def ajax_add_enveloppetype(request,pkstr1):
    recette='rec'
    if request.is_ajax():
        isfleche=PlanFinancement.objects.get(id=pkstr1).fleche
        naturecompta = NatureComptable.objects.filter(pfifleche=isfleche,nctype=recette)
        todo_items=[]
        for s in naturecompta:
            if not (s.enveloppe in todo_items ):
                      todo_items.append(str(s.enveloppe))

        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


#Pour les depenses
def ajax_add_enveloppetype_depense(request,pkstr1):
    depense='dep'
    if request.is_ajax():
        isfleche=PlanFinancement.objects.get(id=pkstr1).fleche
        naturecompta = NatureComptable.objects.filter(pfifleche=isfleche,nctype=depense)
        todo_items=[]
        for s in naturecompta:
            if not (s.enveloppe in todo_items ):
                todo_items.append(str(s.enveloppe))
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def ajax_add_enveloppe_depense(request,pkstr1,lenveloppe):
    #print ("calling_add_enveloppe pour::" + str(pkstr1))
    depense='dep'
    if request.is_ajax():
        isfleche=PlanFinancement.objects.get(id=pkstr1).fleche
        naturecompta = NatureComptable.objects.filter(pfifleche=isfleche,nctype=depense,enveloppe=lenveloppe)
        todo_items=[]
        for s in naturecompta:
            todo_items.append(str(s.id)+"-----"+str(s.enveloppe)+"-----"+str(s.naturec_dep)+str(s.ccbd))
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

#Pour les depenses
def ajax_get_enveloppe_decalage(request,pkstr1):
    depense='dep'
    print("go")
    if request.is_ajax():
        naturec=NatureComptable.objects.get(id=pkstr1)
        print("Nature C: "+ str(naturec))
        print(str(naturec.decalagetresocpae))
        decalageyesno=str(naturec.decalagetresocpae)
        print("on decale ou pas:" + decalageyesno)
        todo_items=[]
        todo_items.append(decalageyesno)
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


##Depenses Ajax find structure level 2 from level1
#def ajax_add_todo1(request,pkstr1):
#    if request.is_ajax():
#        myid=Structure.objects.get(id=pkstr1).myid
#        struct2qset=Structure.objects.all().filter(parentid=myid).order_by('name')
#
#        structlev2ok = []
#        for j in struct2qset:
#            if is_authorised(request.user.username,j.name):
#                structlev2ok.append(j)
#
#
#        todo_items=[]
#        for s in structlev2ok:
#            todo_items.append(str(s.id)+"-----"+str(s.name)+"-----"+str(s.label))
#        print(todo_items)
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
#
##Recettes Ajax find structure level 2 from level1
#def ajax_recadd_todo1(request,pkstr1):
#    if request.is_ajax():
#        myid=Structure.objects.get(id=pkstr1).myid
#        struct2qset=Structure.objects.all().filter(parentid=myid).order_by('name')
#        todo_items=[]
#        structlev2ok = []
#        for j in struct2qset:
#            if is_authorised(request.user.username,j.name):
#                structlev2ok.append(j)
#
#        for s in structlev2ok:
#            todo_items.append(str(s.id)+"-----"+str(s.name)+"-----"+str(s.label))
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
#
#
##Depenses ajax find struct level3 from level2
#def ajax_findstruct_lev3(request,pkstr1):
#    if request.is_ajax():
#        myid=Structure.objects.get(id=pkstr1).myid
#        struct2qset=Structure.objects.all().filter(parentid=myid).order_by('name')
#        todo_items=[]
#        structlev3ok = []
#        for j in struct2qset:
#            if is_authorised(request.user.username,j.name):
#                structlev3ok.append(j)
#
#        for s in structlev3ok:
#            todo_items.append(str(s.id)+"-----"+str(s.name)+"-----"+str(s.label))
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
##Recettes ajax find struct level3 from level2
#def ajax_recfindstruct_lev3(request,pkstr1):
#    if request.is_ajax():
#        myid=Structure.objects.get(id=pkstr1).myid
#        struct2qset=Structure.objects.all().filter(parentid=myid).order_by('name')
#        todo_items=[]
#
#        structlev3ok = []
#        for j in struct2qset:
#            if is_authorised(request.user.username,j.name):
#                structlev3ok.append(j)
#
#        for s in structlev3ok:
#            todo_items.append(str(s.id)+"-----"+str(s.name)+"-----"+str(s.label))
#        #print(todo_items)
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
#
##Depenses ajax_add_cptdev_lev2
#def ajax_add_cptdev_lev2(request,pkcpt):
#    if request.is_ajax():
#        struct2qset=NatureComptable.objects.all().filter(ccparent=pkcpt)
#        todo_items=[]
#        for s in struct2qset:
#            todo_items.append(str(s.ccid)+"-----"+str(s.ccname)+"-----"+str(s.cclabel))
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
#
##Recettes ajax_add_cptdev_lev2
#def ajax_recadd_cptdev_lev2(request,pkcpt):
#    if request.is_ajax():
#        struct2qset=NatureComptable.objects.all().filter(ccparent=pkcpt)
#        todo_items=[]
#        for s in struct2qset:
#            todo_items.append(str(s.ccid)+"-----"+str(s.ccname)+"-----"+str(s.cclabel))
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
#
##Depenses ajax find origine des fonds
#def ajax_findorigfond_lev2(request,pkor):
#    ofid=OrigineFonds.objects.get(id=pkor).ofid
#    if request.is_ajax():
#        qset=OrigineFonds.objects.all().filter(ofparent=ofid)
#        todo_items=[]
#        for s in qset:
#            todo_items.append(str(s.ofname)+"-----"+str(s.oflabel))
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
##Recettes ajax find origine des fonds
#def ajax_recfindorigfond_lev2(request,pkor):
#    ofid=OrigineFonds.objects.get(id=pkor).ofid
#    if request.is_ajax():
#        qset=OrigineFonds.objects.all().filter(ofparent=ofid)
#        todo_items=[]
#        for s in qset:
#            todo_items.append(str(s.ofname)+"-----"+str(s.oflabel))
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
#
#
#def ajax_more_todo11(request):
#    #print ("calling_more_todo1111")
#    if request.is_ajax():
#        todo_items=['test 1', 'test 2',]
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404
#
#def ajax_more_todo1(request):
#    #print ("calling_more_todo1")
#    if request.is_ajax():
#        todo_items=['test 1', 'test 2',]
#        data = json.dumps(todo_items)
#        return HttpResponse(data, content_type='application/json')
#    else:
#        raise Http404


@login_required
def baseformsetdepensefullavec_pfi_cflink(request, pfiid):
    pfi = get_object_or_404(PlanFinancement, pk=pfiid)
    structure = pfi.structure
    isfleche = pfi.is_fleche
    initial = ''  # {'structlev3': struct3id,'plfi': pfiid}

    DepenseFullFormSet = modelformset_factory(
        Depense,
        form=DepenseFormPfi,
        formset=BaseDepenseFullFormSet,
        exclude=[],
        extra=3)
    # print('BF : %s' % DepenseFullFormSet.form.base_fields)
    DepenseFullFormSet.form.base_fields['structure'] = structure
    DepenseFullFormSet.form.base_fields['pfi'] = pfi


    budget = current_budget()
    depense = 'dep'
    depensesdupfi = Depense.objects.filter(
        pfi_id=pfiid, periodebudget=budget)

    if request.method == 'POST':
        myformset = DepenseFullFormSet(request.POST)
        if myformset.is_valid():
            instances = myformset.save()
            for dep in depensesdupfi:
                if not(dep in instances):
                    dep.delete()

            for instance in instances:
                if not instance.creepar:
                    instance.creepar = request.user.username
                instance.modifiepar = request.user.username
                instance.structure = structure
                instance.pfi = pfi
                instance.periodebudget = budget
                instance.save()

            return redirect('liste_pfi_avec_depenses_recettes')
        else:
            depensefull_formset = myformset

    else:
        depensefull_formset = DepenseFullFormSet(
            initial=initial,
            queryset=Depense.objects.filter(
                pfi_id=pfiid, periodebudget=budget))

    domfoncs = DomaineFonctionnel.objects.all().order_by('code')

    context = {
       'depensefull_formset': depensefull_formset,
       'pfi': pfi,
       'budget': budget,
       'structure': structure,
       'domfoncs': domfoncs,
    }
    return render(request, 'depensefull_formset.html', context)


@login_required
def baseformsetrecettefullavec_pfi_cflink(request, pfiid):

    pfi = get_object_or_404(PlanFinancement, pk=pfiid)
    structure = pfi.structure
    isfleche = pfi.is_fleche

    RecetteFullFormSet = modelformset_factory(
        Recette,
        form=RecetteFormPfi,
        formset=BaseRecetteFullFormSet,
        exclude=[],
        extra=3)
    RecetteFullFormSet.form.base_fields['structure'] = structure
    RecetteFullFormSet.form.base_fields['pfi'] = pfi

    df_rec_na = DomaineFonctionnel.objects.filter(code='NA').first()
    budget = current_budget()
    initial = ''
    recettesdupfi = Recette.objects.filter(
        pfi_id=pfiid, periodebudget=budget)

    if request.method == 'POST':
        myformset = RecetteFullFormSet(request.POST)
        if myformset.is_valid():
            instances = myformset.save()
            for rec in recettesdupfi:
                if not(rec in instances):
                    rec.delete()

            for instance in instances:
                if not instance.creepar:
                    instance.creepar = request.user.username
                instance.modifiepar = request.user.username
                instance.structlev3 = structure
                instance.plfi = pfi
                instance.periodebudget = budget
                instance.domfonc = df_rec_na
                instance.save()
                instance.myid = instance.id
                instance.save()

            return redirect('liste_pfi_avec_depenses_recettes')
        else:
            recettefull_formset = myformset

    else:
        recettefull_formset = RecetteFullFormSet(
            initial=initial,
            queryset=Recette.objects.filter(
                pfi_id=pfiid, periodebudget=budget))

    domfoncs = DomaineFonctionnel.objects.filter(code='NA')

    context = {
       'recettefull_formset': recettefull_formset,
       'pfi': pfi,
       'budget': budget,
       'structure': structure,
       'domfoncs': domfoncs,
    }

    return render(request, 'recettefull_formset.html', context)


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

    return render(request, 'pluriannuel.html', {'PFI': pfi, 'form': form})


@login_required
def depense(request, pfiid):
    pfi = PlanFinancement.objects.get(pk=pfiid)
    depense = DepenseForm(pfiid=pfiid)
    if request.method == "POST" in request.POST:
        depense = RecetteForm(request.POST)
        if form_depense.is_valid():
            print("coucou")
    return render(request, 'depense.html', {'test': 'TEST', 'PFI': pfi,
                                            'form_depense': depense})

from functools import partial, wraps


@login_required
def recette(request, pfiid):
    pfi = PlanFinancement.objects.get(pk=pfiid).id
    RecetteFormSet = formset_factory(wraps(RecetteForm)(partial(RecetteForm, pfiid=pfi)), extra=3)
    if request.method == "POST" in request.POST:
        recette = RecetteForm(request.POST)
        if form_recette.is_valid():
            print("coucou")
    context = {
        'test': 'TEST',
        'PFI': pfi,
        'formset': RecetteFormSet
    }
    return render(request, 'recette.html', context)
