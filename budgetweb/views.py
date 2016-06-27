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

from .forms import AuthorisationForm, NatureComptableForm , DomaineFonctionnelForm
from .forms import StructureForm , PlanFinancementForm 
from .models import Authorisation, NatureComptable , DomaineFonctionnel , PeriodeBudget,CompteBudget
from .models import Structure , PlanFinancement , DepenseFull , RecetteFull
from .forms import DepenseFullForm , RecetteFullForm , PeriodeBudgetForm , CompteBudgetForm
from .models import ComptaNature,FondBudgetaire
from .forms import ComptaNatureForm, FondBudgetaireForm
import json
from django.http import Http404,HttpResponse
from django.db.models import Sum
#--------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views

from django.contrib.auth.models import Group
#---------------------------------------------------------------------------------

def search(request):
    pass

#---------------------------------------


#@login_required
def home(request):
    return render_to_response('base.html')


def index2(request):
    return render(request, 'tests/emptygrid.html')


def index3(request):
    return render(request, 'tests/notemptygrid.html')

def index3b(request):
    return render(request, 'tests/notemptygrid-b.html')


def index4(request):
    return render(request, 'tests/notemptygrid2.html')

def index5(request):
    return render(request, 'tests/notemptygrid3.html')


"""-------------------------------------------------
 class Authorisation(models.Model):

-----------------------------------------------------"""

"""-------------------------------------------------
Fonction qui affiche la liste des autorisations
Le formulaire à un searchform pour restreindre l'affichage
-------------------------------------------------"""
def authorisation_list(request):
    if request.method== "POST":
        user = request.POST['name']
        obj  = request.POST['object']
        if user == "" and obj == "" :
            myauth=Authorisation.objects.all()
        elif user == "" :
            myauth=Authorisation.objects.filter(myobject__icontains = obj)
        elif obj == "" :
            myauth=Authorisation.objects.filter(username__icontains = user)
        else:
            myauth=Authorisation.objects.filter(username__icontains = user).filter(myobject__icontains = obj)
    else:
        myauth=Authorisation.objects.all()

    return render(request, 'authorisation_lists.html', {'Authorisations':myauth})


"""-------------------------------------------------
Fonction qui renvoie la liste des autorisations pour un utilisateur
-------------------------------------------------"""
def authorisation_user(request,myuser=""):
    mytauth=Authorisation.objects.filter(username=myuser)
    return render(equest, 'authorisation_lists.html', {'Authorisation':myauth})


"""-------------------------------------------------
Fonction qui prend en parametres:
un utilisateur précis
un objet précis
Fonction qui renvoie 0 si pas d'autorisation pour un objet
-------------------------------------------------"""
def is_authorised(myuser, myobject):
    # chercher les autorisations dans la table
    # si il y a * dans la table, ok tout
    # si il y a qqch* alors detailler
    # si autorisation exacte ok
    thecount1=Authorisation.objects.filter(username=myuser).filter(myobject='*').count()
    if thecount1 >0:
        return thecount1
    else:
        a1=Authorisation.objects.filter(
              username=myuser)
        myobject=myobject.strip()
        a2=a1.filter(myobject=myobject
                 )
        thecount=a2.count()

        if thecount > 0:
            return thecount
        else:
            #decouper
            i=0
            found=0
            while (i < len(myobject)) and (found == 0):
                myobjectsubstr = myobject[0:i]
                a2=a1.filter(myobject__startswith=myobjectsubstr)
                for o in a2:
                    j=i+1
                    if len(o.myobject)>=j and o.myobject[i:j] == '*':
                        found=1
                        print('* match autorisation for '+ myuser +'::'+myobject+'::'+o.myobject+'::'+o.myobject[i:j])
                        return found
                i+=1
            return found


"""-------------------------------------------------
Effacer une autorisation dans la table des autorisations
-------------------------------------------------"""
def authorisation_delete(request,pkauth):
    myauth = get_object_or_404(Authorisation,pk=pkauth)
    if request.method== "POST":
        print(request.POST)
        form = AuthorisationForm(request.POST, instance=myauth)
        if form.is_valid():
            myauth.delete()
            return redirect('authorisation_list')
        else:
            return render(request, 'authorisation_delete.html', {'form': form})
    else:
        form = AuthorisationForm(instance=myauth)
        return render(request, 'authorisation_delete.html', {'form': form})


"""-------------------------------------------------
Afficher une autorisation
-------------------------------------------------"""
def authorisation_detail(request,pkauth):
    myauth = get_object_or_404(Authorisation, pk=pkauth)
    return render(request, 'authorisation_detail.html', {'Authorisation':myauth})


"""-------------------------------------------------
Ajout d'une autorisation
-------------------------------------------------"""
def authorisation_new(request):
    if request.method == "POST":
        form = AuthorisationForm(request.POST)
        if form.is_valid():
            print ('form is valid')
            newauth = form.save(commit=False)
            newauth.save()
            return redirect('authorisation_detail', pkauth=newauth.pk)
            return redirect('authorisation_list')
        else:
            print ('form not valid')
    else:
        form = AuthorisationForm()
    return render(request, 'authorisation_new.html', {'form': form})


"""-------------------------------------------------
Import du fichier csv - séparateur ;
-------------------------------------------------"""
def authorisation_importcsv(request):
    if request.method == "POST":
        if request.POST.get("lechemin"):
             lemessage=""
             lechemin=request.POST.get("lechemin")
             fichier = open(lechemin, "r")
             nblignes=0
             for ligne in fichier:
                 if ligne.strip():
                     nblignes = nblignes+1
                     monauth=Authorisation()
                     ligne=ligne.split(";")
                     monauth.username=ligne[0]
                     monauth.myobject = ligne[1]
                     monauth.save()
             lemessage=lemessage+ "  ok fichier "+ lechemin+ " importé "+ str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"authorisation_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'authorisation_import.html', {'lechemin': "", 'lemessage':""})

    return render(request, 'authorisation_import.html', {'lechemin': "", 'lemessage':""})


"""-------------------------------------------------
Vider la table des autorisations
-------------------------------------------------"""
def authorisation_deleteall(request):
    if request.method == "POST":
        html=[]
        html.append('Elements supprimes:')
        html.append(Authorisation.objects.count())
        html.append('<br>')
        html.append('Suppression de tous les elements de la table des autorisations')

        myauth = Authorisation.objects.all()
        for auth in myauth:
            auth.delete()

        html.append('Elements restants:')
        html.append(Authorisation.objects.count())
        html.append('<br>')
        return HttpResponse(html)
    else:
        nbauth=Authorisation.objects.count()
        return render(request, 'authorisation_deleteall.html',{'nb':nbauth})


"""-------------------------------------------------
#class PeriodeBudget(models.Model):
-------------------------------------------------"""
"""-------------------------------------------------
Créer un nouveau budget
-------------------------------------------------"""
def periodebudget_new(request):
    if request.method == "POST":
        form = PeriodeBudgetForm(request.POST)
        if form.is_valid():
            newbud = form.save(commit=False)
            newbud.save()
            return redirect('periodebudget_list')
        else:
            return render(request, 'periodebudget_new.html', {'form': form})
    else:
        form = PeriodeBudgetForm()
    return render(request, 'periodebudget_new.html', {'form': form})


"""-------------------------------------------------
Affichage des éléments de la base budget
avec un searchform pour restreindre l'affichage
-------------------------------------------------"""
def periodebudget_list(request):
    if request.method == "POST":
        ccname = request.POST['ccname']
        cclabel  = request.POST['cclabel']
        if ccname == "" and cclabel == "" :
            mycc = PeriodeBudget.objects.all()
        elif cclabel == "" :
            mycc = PeriodeBudget.objects.filter ( name__icontains = ccname )
        elif ccname == "" :
            mycc = PeriodeBudget.objects.filter ( cclabel__icontains = cclabel )
        else:
            mycc = PeriodeBudget.objects.filter( name__icontains = ccname ).filter( cclabel__icontains = cclabel )
    else:
        mycc = PeriodeBudget.objects.all()

    return render(request, 'periodebudget_lists.html', {'reponses':mycc})


"""-------------------------------------------------
Effacer un budget
-------------------------------------------------"""
def periodebudget_delete(request,pkpb):
    mycc = get_object_or_404( Periodebudget,pk=pkpb )
    if request.method== "POST":
        form = PeriodebudgetForm(request.POST, instance=mycc)
        if form.is_valid():
            mycc.delete()
            return redirect('periodebudget_list')
        else:
            return render(request, 'periodebudget_delete.html', {'form': form})
    else:
        form = PeriodeBudgetForm( instance=mycc )
        return render(request, 'periodebudget_delete.html', {'form': form})


def periodebudget_detail( request,pkpb ):
    """-------------------------------------------------
    Afficher une période de budget
    -------------------------------------------------"""
    mycc = get_object_or_404( PeriodeBudget , pk=pkpb )
    return render(request, 'periodebudget_detail.html', {'reponse':mycc})


def comptebudget_new(request):
    """------------------------------------------------
    new comptebudgetaire 
    ------------------------------------------------"""
    if request.method == "POST":
        form = CompteBudgetForm(request.POST)
        if form.is_valid():
            newcb = form.save(commit=False)
            newcb.save()
            return redirect('comptebudget_list')
    else:
        form = CompteBudgetForm()
    return render(request, 'comptebudget_new.html', {'form': form})


def comptebudget_list(request):
    """------------------------------------------------
    list comptebudgetaire 
    ------------------------------------------------"""
    if request.method == "POST":
        cclabel  = request.POST['cclabel']
        if cclabel == "" :
            mycc = CompteBudget.objects.all()
        else:
            mycc = CompteBudget.objects.filter( cclabel__icontains = cclabel )
    else:
        mycc = CompteBudget.objects.all()

    return render(request, 'comptebudget_lists.html', {'reponses':mycc})


def comptebudget_delete(request,pkcc):
    """------------------------------------------------
    delete comptebudgetaire 
    ------------------------------------------------"""
    mycc = get_object_or_404( CompteBudget,pk=pkcc )
    if request.method== "POST":
        print(request.POST)
        form = CompteBudgetForm(request.POST, instance=mycc)
        if form.is_valid():
            mycc.delete()
            return redirect('comptebudget_list')
    else:
        form = CompteBudgetForm( instance=mycc )
        return render(request, 'comptebudget_delete.html', {'form': form})


#ComptaNature,FondBudgetaire

def comptanature_new(request):
    """------------------------------------------------
    new comptanature 
    ------------------------------------------------"""
    if request.method == "POST":
        form = ComptaNatureForm(request.POST)
        if form.is_valid():
            newcb = form.save(commit=False)
            newcb.save()
            return redirect('comptanature_list')
    else:
        form = ComptaNatureForm()
    return render(request, 'comptanature_new.html', {'form': form})


def comptanature_edit(request,pk):
    """------------------------------------------------------------------
    Editer une comptanature
    ------------------------------------------------------------------"""
    myof = get_object_or_404( ComptaNature , pk=pk )
    if request.method== "POST":
        form = ComptaNatureForm(request.POST, instance=myof )
        if form.is_valid():
            myof.save()
            return redirect('comptanature_list')
    else:
        form = ComptaNatureForm( instance=myof )
    return render(request, 'comptanature_edit.html', {'form': form})


def comptanature_list(request):
    """------------------------------------------------
    list comptanature 
    ------------------------------------------------"""
    if request.method == "POST":
        cclabel  = request.POST['cclabel']
        if cclabel == "" :
            mycc = ComptaNature.objects.all()
        else:
            mycc = Comptanature.objects.filter( label__icontains = cclabel )
    else:
        mycc = ComptaNature.objects.all()

    return render(request, 'comptanature_lists.html', {'reponses':mycc})


def comptanature_delete(request,pkcb):
    """------------------------------------------------
    delete comptanature 
    ------------------------------------------------"""
    mycc = get_object_or_404( ComptaNature,pk=pkcb )
    if request.method== "POST":
        print(request.POST)
        form = ComptaNatureForm(request.POST, instance=mycc)
        if form.is_valid():
            mycc.delete()
            return redirect('comptanature_list')
    else:
        form = ComptaNatureForm( instance=mycc )
        return render(request, 'comptanature_delete.html', {'form': form})


#----------------
def fondbudgetaire_new(request):
    """------------------------------------------------
    new fondbudgetaire 
    ------------------------------------------------"""
    if request.method == "POST":
        form = FondBudgetaireForm(request.POST)
        if form.is_valid():
            newcb = form.save(commit=False)
            newcb.save()
            return redirect('fondbudgetaire_list')
    else:
        form = FondBudgetaireForm()
    return render(request, 'fondbudgetaire_new.html', {'form': form})


def fondbudgetaire_edit(request,pk):
    """------------------------------------------------------------------
    Editer un fond
    ------------------------------------------------------------------"""
    myof = get_object_or_404( FondBudgetaire , pk=pk )
    if request.method== "POST":
        form = FondBudgetaireForm(request.POST, instance=myof )
        if form.is_valid():
            myof.save()
            return redirect('fondbudgetaire_list')
    else:
        form = FondBudgetaireForm( instance=myof )
    return render(request, 'fondbudgetaire_edit.html', {'form': form})



def fondbudgetaire_list(request):
    """------------------------------------------------
    list fondbudgetaire 
    ------------------------------------------------"""
    if request.method == "POST":
        cclabel  = request.POST['cclabel']
        if cclabel == "" :
            mycc = FondBudgetaire.objects.all()
        else:
            mycc = FondBudgetaire.objects.filter( label__icontains = cclabel )
    else:
        mycc = FondBudgetaire.objects.all()

    return render(request, 'fondbudgetaire_lists.html', {'reponses':mycc})


def fondbudgetaire_delete(request,pkcb):
    """------------------------------------------------
    delete fondbudgetaire 
    ------------------------------------------------"""
    mycc = get_object_or_404( FondBudgetaire,pk=pkcb )
    if request.method== "POST":
        print(request.POST)
        form = FondBudgetaireForm(request.POST, instance=mycc)
        if form.is_valid():
            mycc.delete()
            return redirect('fondbudgetaire_list')
    else:
        form = FondBudgetaireForm( instance=mycc )
        return render(request, 'fondbudgetaire_delete.html', {'form': form})



#-----------------

def naturecomptable_new(request):
    """------------------------------------------------
    new Nature comptable 
    ------------------------------------------------"""
    if request.method == "POST":
        form = NatureComptableForm(request.POST)
        if form.is_valid():
            newcc = form.save(commit=False)
            newcc.save()
            return redirect('naturecomptable_list')
        else:
            print ('form not valid')
    else:
        form = NatureComptableForm()
    return render(request, 'naturecomptable_new.html', {'form': form})


def naturecomptable_edit(request,pkcc):
    """------------------------------------------------------------------
    Editer une naturecomptable
    ------------------------------------------------------------------"""
    myof = get_object_or_404( NatureComptable , pk=pkcc )
    if request.method== "POST":
        form = NatureComptableForm(request.POST, instance=myof )
        if form.is_valid():
            myof.save()
            return redirect('naturecomptable_list')
    else:
        form = NatureComptableForm( instance=myof )
    return render(request, 'naturecomptable_edit.html', {'form': form})


def naturecomptable_list(request):
    """------------------------------------------------
    Liste des natures comptables 
    ------------------------------------------------"""

    if request.method == "POST":
        nature = request.POST['nature']
        fond  = request.POST['fond']
        if nature == "" and fond == "" :
            mycc = NatureComptable.objects.all()
        elif fond != "" :
            mycc = NatureComptable.objects.filter (fondbudget_recette__code__icontains = fond )
        else:
            mycc = NatureComptable.objects.filter ( naturec_dep__code__icontains = nature )
    else:
        mycc = NatureComptable.objects.all()

    return render(request, 'naturecomptable_lists.html', {'reponses':mycc})


def naturecomptable_delete(request,pkcc):
    mycc = get_object_or_404( NatureComptable,pk=pkcc )
    if request.method== "POST":
        print(request.POST)
        form = NatureComptableForm(request.POST, instance=mycc)
        if form.is_valid():
            mycc.delete()
            return redirect('naturecomptable_list')
    else:
        form = NatureComptableForm( instance=mycc )
        return render(request, 'naturecomptable_delete.html', {'form': form})


def naturecomptable_detail( request,pkcc ):
    mycc = get_object_or_404( NatureComptable , pk=pkcc )
    return render(request, 'naturecomptable_detail.html', {'reponse':mycc})


def naturecomptable_importcsv(request):
    if request.method == "POST":
        if request.POST.get("lechemin"):
             lemessage=""
             lechemin=request.POST.get("lechemin")
             fichier = open(lechemin, "r")
             nblignes=0
             for ligne in fichier:
                 if ligne.strip():
                     nblignes = nblignes+1
                     moncc = NatureComptable()
                     ligne=ligne.split(";")
                     if ligne[0] == 'PFI fléché' :
                         moncc.pfifleche =True
                     else:
                         moncc.pfifleche =False
                     moncc.ncenveloppe = ligne[1]
                     moncc.nccode = ligne[2]
                     moncc.nclabel = ligne[2]
                     moncc.ncsecondairecode = ligne[3]

                     ccbdcode = ligne[4]
                     moncc.ccbd = CompteBudget.objects.get(code=ccbdcode) 
                     if ligne[6] == 'non':
                         moncc.decalagetresocpae = False
                     else:
                         moncc.decalagetresocpae = True  
                     moncc.nctype = 'dep'

                     moncc.save()
             lemessage=lemessage+ "  ok fichier "+ lechemin+ " importé "+ str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"naturecomptable_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'naturecomptable_import.html', {'lechemin': "", 'lemessage':""})
    else:
        lechemin="vide2"
    return render(request, 'naturecomptable_import.html', {'lechemin': "", 'lemessage':""})


def naturecomptable_recette__importcsv(request):
    if request.method == "POST":
        if request.POST.get("lechemin"):
             lemessage=""
             lechemin=request.POST.get("lechemin")
             fichier = open(lechemin, "r")
             nblignes=0
             for ligne in fichier:
                 if ligne.strip():
                     nblignes = nblignes+1
                     moncc = NatureComptable()
                     ligne=ligne.split(";")
                     if ligne[0] == 'PFI fléché' :
                         moncc.pfifleche =True
                     else:
                         moncc.pfifleche =False
                     moncc.ncenveloppe = ligne[1]
                     moncc.nccode = ligne[2]
                     moncc.nclabel = ligne[2]
                     moncc.ncsecondairecode = ligne[3]
                     
                     ccbdcode = ligne[4]
                     moncc.ccbd = CompteBudget.objects.get(code=ccbdcode) 
                     if ligne[6] == 'non':
                         moncc.decalagetresocpae = False 
                     else:
                         moncc.decalagetresocpae = True     
                     moncc.nctype = 'rec'

                     moncc.save()
             lemessage=lemessage+ "  ok fichier "+ lechemin+ " importé "+ str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"naturecomptable_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'naturecomptable_import.html', {'lechemin': "", 'lemessage':""})
    else:
        lechemin="vide2"
    return render(request, 'naturecomptable_import.html', {'lechemin': "", 'lemessage':""})



def naturecomptable_deleteall(request):
    if request.method == "POST":
        html=[]
        html.append('Elements supprimes:')
        html.append(NatureComptable.objects.count())
        html.append('<br>')
        html.append('Suppression de tous les elements de la table des comptes comptables')

        mycc = NatureComptable.objects.all()
        for cc in mycc:
            cc.delete()

        html.append('Elements restants:')
        html.append(NatureComptable.objects.count())
        html.append('<br>')
        return HttpResponse(html)
    else:
        nbcc = NatureComptable.objects.count()
        return render(request, 'naturecomptable_deleteall.html',{'nb':nbcc})


""" ********************************************
class DomaineFonctionnel(models.Model):
    dfcode = models.CharField(max_length=100, default="")
    dflabel = models.CharField(max_length=100, default="")
    dfgrpcumul = models.CharField(max_length=100, default="")
    dfgrpfonc = models.CharField(max_length=100, default="")
    dfrmq = models.CharField(max_length=100, default="")
    dfdesc = models.CharField(max_length=100, default="")
************************************************ """

def domainefonctionnel_new(request):
    if request.method == "POST":
        form = DomaineFonctionnelForm(request.POST)
        if form.is_valid():
            newdf = form.save(commit=False)
            newdf.save()
            return redirect('domainefonctionnel_list')
        else:
            print ('form not valid')
    else:
        form = DomaineFonctionnelForm()
    return render(request, 'domainefonctionnel_new.html', {'form': form})


def domainefonctionnel_list(request):
    if request.method == "POST":
        dfcode = request.POST['dfcode']
        dfcumul  = request.POST['dfcumul']
        if dfcode == "" and dfcumul == "" :
            mydf = DomaineFonctionnel.objects.all()
        elif dfcumul == "" :
            mydf = DomaineFonctionnel.objects.filter ( dfcode__icontains = dfcode )
        elif dfcode == "" :
            mydf = DomaineFonctionnel.objects.filter ( dfgrpcumul__icontains = dfcumul )
        else:
            mydf = DomaineFonctionnel.objects.filter( dfcode__icontains = dfcode ).filter( dfgrpcumul__icontains = dfcumul )
    else:
        mydf = DomaineFonctionnel.objects.all()

    return render(request, 'domainefonctionnel_lists.html', {'reponses':mydf})


def domainefonctionnel_delete(request,pkdf):
    mydf = get_object_or_404( DomaineFonctionnel,pk=pkdf )
    if request.method== "POST":
        print(request.POST)
        form = DomaineFonctionnelForm(request.POST, instance=mydf)
        if form.is_valid():
            mydf.delete()
            return redirect('domainefonctionnel_list')
    else:
        form = DomaineFonctionnelForm( instance=mydf )
        return render(request, 'domainefonctionnel_delete.html', {'form': form})


def domainefonctionnel_detail( request,pkdf ):
    mydf = get_object_or_404( DomaineFonctionnel , pk=pkdf )
    return render(request, 'domainefonctionnel_detail.html', {'reponse':mydf})


def domainefonctionnel_importcsv(request):
    if request.method == "POST":
        if request.POST.get("lechemin"):
             lemessage=""
             lechemin=request.POST.get("lechemin")
             fichier = open(lechemin, "r")
             nblignes=0
             for ligne in fichier:
                 if ligne.strip():
                     nblignes = nblignes+1
                     mondf = DomaineFonctionnel()
                     ligne=ligne.split(";")
                     mondf.dfcode = ligne[0]
                     mondf.dflabel = ligne[1]
                     mondf.dfgrpcumul = ligne[2]
                     mondf.dfgrpfonc = ligne[3]
                     mondf.dfrmq = ligne[4]
                     mondf.dfdesc = ligne[5]
                     mondf.save()
             lemessage=lemessage+ "  ok fichier "+ lechemin+ " importé "+ str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"domainefonctionnel_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'domainefonctionnel_import.html', {'lechemin': "", 'lemessage':""})
    else:
        lechemin="vide2"
    return render(request, 'domainefonctionnel_import.html', {'lechemin': "", 'lemessage':""})


def domainefonctionnel_deleteall(request):
    if request.method == "POST":
        html=[]
        html.append('Elements supprimes:')
        html.append(DomaineFonctionnel.objects.count())
        html.append('<br>')
        html.append('Suppression de tous les elements de la table des Domaines fonctionnels')

        mydf = DomaineFonctionnel.objects.all()
        for df in mydf:
            df.delete()

        html.append('Elements restants:')
        html.append(DomaineFonctionnel.objects.count())
        html.append('<br>')
        return HttpResponse(html)
    else:
        nbdf = DomaineFonctionnel.objects.count()
        return render(request, 'domainefonctionnel_deleteall.html',{'nb':nbdf})



"""  ******************************************************
class OrigineFonds(models.Model):
    ofid = models.CharField(max_length=100)
    ofparent = models.CharField(max_length=100)
    ofname = models.CharField(max_length=100)
    oflabel = models.CharField(max_length=100)
    oftype = models.CharField(max_length=100)
    ofbudget = models.CharField(max_length=100)
    ofnomades = models.CharField(max_length=100)
****************************************************** """

def originefonds_new(request):
    if request.method == "POST":
        form = OrigineFondsForm(request.POST)
        if form.is_valid():
            newof = form.save(commit=False)
            newof.save()
            return redirect('originefonds_list')
        else:
            print ('form not valid')
    else:
        form = OrigineFondsForm()
    return render(request, 'originefonds_new.html', {'form': form})


def originefonds_edit(request,pkof):
    """------------------------------------------------------------------
    Editer une Origne de Fonds - Raccourcis en fonds par la DFI 
    ------------------------------------------------------------------"""
    myof = get_object_or_404( OrigineFonds , pk=pkof )
    if request.method== "POST":
        form = OrigineFondsForm(request.POST, instance=myof )
        if form.is_valid():
            myof.save()
            return redirect('originefonds_list')
    else:
        form = OrigineFondsForm( instance=myof )
    return render(request, 'originefonds_edit.html', {'form': form})


def originefonds_list(request):
    if request.method == "POST":
        oftype = request.POST['oftype']
        oflabel  = request.POST['oflabel']
        if oftype == "" and oflabel == "" :
            myof = OrigineFonds.objects.all()
        elif oflabel == "" :
            myof = OrigineFonds.objects.filter ( oftype__icontains = oftype )
        elif oftype == "" :
            myof = OrigineFonds.objects.filter ( oflabel__icontains = oflabel )
        else:
            myof = OrigineFonds.objects.filter( oftype__icontains = oftype ).filter( oflabel__icontains = oflabel )
    else:
        myof = OrigineFonds.objects.all()

    myof2 = myof.order_by('ofparent')
    return render(request, 'originefonds_lists.html', {'reponses':myof,'reponses2':myof2})


def originefonds_delete(request,pkof):
    myof = get_object_or_404( OrigineFonds , pk=pkof )
    if request.method== "POST":
        form = OrigineFondsForm(request.POST, instance=myof)
        if form.is_valid():
            myof.delete()
            return redirect('originefonds_list')
        else:
            return render(request, 'originefonds_delete.html', {'form': form})
    else:
        form = OrigineFondsForm( instance=myof )
        return render(request, 'originefonds_delete.html', {'form': form})


def originefonds_detail( request,pkof ):
    myof = get_object_or_404( OrigineFonds , pk=pkof )
    return render(request, 'originefonds_detail.html', {'reponse':myof})


def originefonds_importcsv(request):
    if request.method == "POST":
        if request.POST.get("lechemin"):
             lemessage=""
             lechemin=request.POST.get("lechemin")
             fichier = open(lechemin, "r")
             nblignes=0
             for ligne in fichier:
                 if ligne.strip():
                     nblignes = nblignes+1
                     monof = OrigineFonds()
                     ligne=ligne.split(";")
                     monof.ofid = ligne[0]
                     monof.ofparent = ligne[1]
                     monof.ofname = ligne[2]
                     monof.oflabel = ligne[3]
                     monof.oftype = ligne[4]
                     monof.ofbudget = ligne[5]
                     monof.ofnomades = ligne[6]

                     monof.save()
             lemessage=lemessage+ "  ok fichier "+ lechemin+ " importé "+ str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"originefonds_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'originefonds_import.html', {'lechemin': "", 'lemessage':""})
    else:
        lechemin="vide2"
    return render(request, 'originefonds_import.html', {'lechemin': "", 'lemessage':""})


def originefonds_deleteall(request):
    if request.method == "POST":
        html=[]
        html.append('Elements supprimes:')
        html.append(OrigineFonds.objects.count())
        html.append('<br>')
        html.append('Suppression de tous les elements de la table des origines des fonds')

        myof = OrigineFonds.objects.all()
        for of in myof:
            of.delete()

        html.append('Elements restants:')
        html.append(OrigineFonds.objects.count())
        html.append('<br>')
        return HttpResponse(html)
    else:
        nbdf = OrigineFonds.objects.count()
        return render(request, 'originefonds_deleteall.html',{'nb':nbof})



""" ********************************************************************
class Structure(models.Model):
******************************************************************  """

"""------------------------------------------------------------------
creation d'une structure CF/CC/CP
------------------------------------------------------------------"""
def structure_new(request):
    if request.method == "POST":
        form = StructureForm(request.POST)
        if form.is_valid():
            newstruct = form.save(commit=False)
            newstruct.save()
            return redirect('structure_list')
        else:
            print ('form not valid')
    else:
        form = StructureForm()
    return render(request, 'structure_new.html', {'form': form})

"""------------------------------------------------------------------
Liste des structure CF/CC/CP
------------------------------------------------------------------"""
def structure_list(request):
    if request.method == "POST":
        stname = request.POST['stname']
        stlabel  = request.POST['stlabel']
        if stname == "" and stlabel == "" :
            myst = Structure.objects.all()
        elif stname == "" :
            myst = Structure.objects.filter ( label__icontains = stlabel )
        elif stlabel == "" :
            myst = Structure.objects.filter ( name__icontains = stname )
        else:
            myst = Structure.objects.filter( label__icontains = stlabel ).filter( name__icontains = stname )
    else:
        myst = Structure.objects.all()

    return render(request, 'structure_lists.html', {'reponses':myst})


def structure_list2(request):
    myst = Structure.objects.filter(parent=None)

    return render(request, 'structure_lists_arbomain.html', {'reponses':myst})


"""------------------------------------------------------------------
Effacer une structure CF/CC/CP
------------------------------------------------------------------"""
def structure_delete(request,pkst):
    myst = get_object_or_404( Structure , pk=pkst )
    if request.method== "POST":
        form = StructureForm(request.POST, instance=myst)
        if form.is_valid():
            myst.delete()
            return redirect('structure_list')
    else:
        form = StructureForm( instance=myst )
        return render(request, 'structure_delete.html', {'form': form})


"""------------------------------------------------------------------
Editer une structure CF/CC/CP
------------------------------------------------------------------"""
def structure_edit(request,pkst):
    myst = get_object_or_404( Structure , pk=pkst )
    if request.method== "POST":
        form = StructureForm(request.POST, instance=myst)
        if form.is_valid():
            myst.save()
            return redirect('structure_list')
    else:
        form = StructureForm( instance=myst )
    return render(request, 'structure_edit.html', {'form': form})



"""------------------------------------------------------------------
Affichage d'une structure CF/CC/CP
------------------------------------------------------------------"""
def structure_detail( request,pkst ):
    myst = get_object_or_404( Structure , pk=pkst )
    return render(request, 'structure_detail.html', {'reponse':myst})


"""------------------------------------------------------------------
Import de structures CF/CC/CP
Format csv séparateur ;
------------------------------------------------------------------"""
def structure_importcsv(request):
    if request.method == "POST":
        if request.POST.get("lechemin"):
             lemessage=""
             lechemin=request.POST.get("lechemin")
             fichier = open(lechemin, "r")
             nblignes=0
             for ligne in fichier:
                 if ligne.strip():
                     nblignes = nblignes+1
                     monst = Structure()
                     ligne = ligne.split(";")
                     monst.myid = ligne[0]
                     monst.type = ligne[1]
                     monst.name = ligne[2]
                     monst.label = ligne[3]
                     monst.parentid = ligne[4]
                     monst.ordre = ligne[5]
                     monst.niv = ligne[6]
                     monst.bloq = ligne[7]
                     monst.modifdate = ligne[8]
                     monst.modifpar = ligne[9]
                     monst.dfmc = ligne[10]
                     monst.fdr = ligne[11]

                     monst.save()
             lemessage=lemessage+ "  ok fichier "+ lechemin+ " importé "+ str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"structure_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'structure_import.html', {'lechemin': "", 'lemessage':""})
    else:
        lechemin="vide2"
    return render(request, 'structure_import.html', {'lechemin': "", 'lemessage':""})


"""------------------------------------------------------------------
Vider la table des structures CF/CC/CP
------------------------------------------------------------------"""
def structure_deleteall(request):
    if request.method == "POST":
        html=[]
        html.append('Elements supprimes:')
        html.append(Structure.objects.count())
        html.append('<br>')
        html.append('Suppression de tous les elements de la table des origines des fonds')

        myst = Structure.objects.all()
        for st in myst:
            st.delete()

        html.append('Elements restants:')
        html.append(Structure.objects.count())
        html.append('<br>')
        return HttpResponse(html)
    else:
        nbst = Structure.objects.count()
        return render(request, 'structure_deleteall.html',{'nb':nbst})



def structure_set_parent(request):
    mystructures = Structure.objects.all()
    for child in mystructures:
        child.parent=Structure.objects.filter(myid=child.parentid).first()
        child.save()

    return render(request, 'structure_lists.html', {'reponses':mystructures})

""" ----------------------------------------------------------------
class PlanFinancement(models.Model):
--------------------------------------------------------------  """

"""------------------------------------------------------------------
creation d'un PFI
------------------------------------------------------------------"""
def planfinancement_new(request):
    if request.method == "POST":
        form = PlanFinancementForm(request.POST)
        if form.is_valid():
            newpfi = form.save(commit=False)
            newpfi.save()
            return redirect('planfinancement_list')
        else:
            print ('form not valid')
    else:
        form = PlanFinancementForm()
    return render(request, 'planfinancement_new.html', {'form': form})


"""------------------------------------------------------------------
Liste des PFI
------------------------------------------------------------------"""
def planfinancement_list(request):
    if request.method == "POST":
        pfiname = request.POST['pfiname']
        pfilabel  = request.POST['pfilabel']
        if pfiname == "" and pfilabel == "" :
            mypfi = PlanFinancement.objects.all()
        elif pfiname == "" :
            mypfi = PlanFinancement.objects.filter ( label__icontains = pfilabel )
        elif stlabel == "" :
            mypfi = PlanFinancement.objects.filter ( name__icontains = pfiname )
        else:
            mypfi = PlanFinancement.objects.filter( label__icontains = pfilabel ).filter( name__icontains = pfiname )
    else:
        mypfi = PlanFinancement.objects.all()

    return render(request, 'planfinancement_lists.html', {'reponses':mypfi})


def planfinancement_delete(request,pkpfi):
    """------------------------------------------------------------------
    Effacer un PFI
    ------------------------------------------------------------------"""

    mypfi = get_object_or_404( PlanFinancement , pk=pkpfi )
    if request.method== "POST":
        form = PlanFinancementForm(request.POST, instance=mypfi)
        if form.is_valid():
            mypfi.delete()
            return redirect('planfinancement_list')
    else:
        form = PlanFinancementForm( instance=mypfi )
        return render(request, 'planfinancement_delete.html', {'form': form})



def planfinancement_edit(request,pkpfi):
    """------------------------------------------------------------------
    Editer un PFI
    ------------------------------------------------------------------"""

    mypfi = get_object_or_404( PlanFinancement , pk=pkpfi )
    if request.method== "POST":
        form = PlanFinancementForm(request.POST, instance=mypfi)
        if form.is_valid():
            mypfi.save()
            return redirect('planfinancement_list')
    else:
        form = PlanFinancementForm( instance=mypfi )
    return render(request, 'planfinancement_edit.html', {'form': form})



"""------------------------------------------------------------------
Afficher un PFI
------------------------------------------------------------------"""
def planfinancement_detail( request,pkpfi ):
    mypfi = get_object_or_404( PlanFinancement , pk=pkpfi )
    form = PlanFinancementForm(instance=mypfi)
    return render(request, 'planfinancement_detail.html', {'form':form})


"""------------------------------------------------------------------
Import csv des PFI -version abandonnée-
------------------------------------------------------------------"""
# ancienne version
def planfinancement_importcsv_v1(request):
    if request.method == "POST":
        if request.POST.get("lechemin"):
             lemessage=""
             lechemin=request.POST.get("lechemin")
             fichier = open(lechemin, "r")
             nblignes=0
             for ligne in fichier:
                 if ligne.strip():
                     nblignes = nblignes+1
                     monpfi = PlanFinancement()
                     ligne = ligne.split(";")
                     monpfi.name = ligne[0]
                     monpfi.label = ligne[1]
                     monpfi.type = ligne[2]
                     monpfi.budget = ligne[3]
                     monpfi.nomades = ligne[4]
                     monpfi.refsifac = ligne[5]
                     monpfi.refdfi = ligne[6]
                     monpfi.societe = ligne[7]
                     monpfi.ccassoc = ligne[8]
                     monpfi.cpassoc = ligne[9]
                     monpfi.responsable = ligne[10]
                     monpfi.dordre = ligne[11]
                     monpfi.divirecette = ligne[12]
                     monpfi.status = ligne[13]
                     #-- 3 champs libres
                     monpfi.cleregul = ligne[17]
                     monpfi.domainefonc = ligne[18]
                     monpfi.save()
             lemessage=lemessage+ "  ok fichier "+ lechemin+ " importé "+ str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"planfinancement_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'planfinancement_import.html', {'lechemin': "", 'lemessage':""})
    else:
        lechemin="vide2"
    return render(request, 'planfinancement_import.html', {'lechemin': "", 'lemessage':""})


"""------------------------------------------------------------------
Import des PFI - Version abandonnée
------------------------------------------------------------------"""
def planfinancement_importcsv2(request):
    if request.method == "POST":
        if request.POST.get("lechemin"):
             lechemin=request.POST.get("lechemin")
             fichier = open(lechemin, "r")
             nblignes=0
             for ligne in fichier:
                 if ligne.strip():
                     nblignes = nblignes+1
                     monpfi = PlanFinancement()
                     ligne = ligne.split(";")
                     monpfi.myid = ligne[0]
                     monpfi.name = ligne[1]
                     monpfi.eotp = ligne[2]
                     monpfi.label = ligne[3]
                     monpfi.idabrege = ligne[4]
                     monpfi.creepar = ligne[5]
                     monpfi.creedate = ligne[6]
                     monpfi.modifpar = ligne[7]
                     monpfi.modifdate = ligne[8]
                     monpfi.responsable = ligne[9]
                     monpfi.dem = ligne[10]
                     monpfi.societe = ligne[11]
                     monpfi.ccassoc = ligne[13]
                     monpfi.cpassoc = ligne[12]
                     monpfi.save()
             lemessage="ok fichier "+ lechemin+ " importé "
             lemessage+=str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"planfinancement_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'planfinancement_import.html', {'lechemin': "", 'lemessage':""})
    else:
        lechemin="vide2"
    return render(request, 'planfinancement_import.html', {'lechemin': "", 'lemessage':""})



"""------------------------------------------------------------------
Import des PFI - Version utilisée
#nouveau format:Code eotp;PFI;Désignation Operation;Fleché;Pluriannuel;CF ;CP Dérivé;CC Dérivé;
------------------------------------------------------------------"""
@login_required
def planfinancement_importcsv(request):
    if request.method == "POST":
        if request.POST.get("lechemin"):
             lechemin=request.POST.get("lechemin")
             fichier = open(lechemin, "r")
             nblignes=0
             for ligne in fichier:
                 if ligne.strip():
                     nblignes = nblignes+1
                     monpfi = PlanFinancement()
                     ligne = ligne.split(";")
                     monpfi.myid = ligne[1]
                     monpfi.name = ligne[2]
                     monpfi.eotp = ligne[0]
                     monpfi.creepar = request.user.username
                     monpfi.modifiepar = request.user.username
                     monpfi.societe = "ETAB"
                     monpfi.cfassoc = ligne[5]
                     monpfi.cpassoc = ligne[6]
                     monpfi.ccassoc = ligne[7]
                     if ligne[3] == "oui":
                         monpfi.fleche = True
                     else:
                         monpfi.fleche=False

                     if ligne[4] == "oui":
                         monpfi.pluriannuel = True
                     else:
                         monpfi.pluriannuel=False

                     monpfi.save()
             lemessage="ok fichier "+ lechemin+ " importé "+ str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"planfinancement_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'planfinancement_import.html', {'lechemin': "", 'lemessage':""})
    else:
        lechemin="vide2"
    return render(request, 'planfinancement_import.html', {'lechemin': "", 'lemessage':""})



"""------------------------------------------------------------------
Vidage de la table des PFI
------------------------------------------------------------------"""
def planfinancement_deleteall(request):
    if request.method == "POST":
        html=[]
        html.append('Elements supprimes:')
        html.append(PlanFinancement.objects.count())
        html.append('<br>')
        html.append('Suppression de tous les elements de la table des plans de financement')

        mypfi = PlanFinancement.objects.all()
        for pfi in mypfi:
            pfi.delete()

        html.append('Elements restants:')
        html.append(PlanFinancement.objects.count())
        html.append('<br>')
        return HttpResponse(html)
    else:
        nbpfi = PlanFinancement.objects.count()
        return render(request, 'planfinancement_deleteall.html',{'nb':nbpfi})


def liste_pfi_avec_depenses_recettes(request):
    mypfi = PlanFinancement.objects.order_by('societe','cfassoc','ccassoc','cpassoc','myid')
    mydepenses = DepenseFull.objects.all()
    myrecettes = RecetteFull.objects.all()
    return render(request, 'planfinancementavecdeprec_lists.html', {'reponses':mypfi,'depenses':mydepenses,'recettes':myrecettes})






""" ----------------------------------------------------------------------------
class depensefull
-------------------------------------------------------------------------- """

""" -----------------------------------------------------------------
Création depenses dans le budget - non utilisé
------------------------------------------------------------------- """
@login_required
def depensefull_new(request):
    if request.method == "POST":
        form = DepenseFullForm(request.POST)
        if form.is_valid():
            newdepense = form.save(commit=False)
            newdepense.creepar = request.user.username
            newdepense.save()
            return redirect('depensefull_list')
        else:
            print ('form not valid')
    else:
        form = DepenseFullForm()
    return render(request, 'depensefull_new.html', {'form': form})


""" -----------------------------------------------------------------
Edition depenses dans le budget
------------------------------------------------------------------- """
def depensefull_edit(request,pkdep):
    mydep = get_object_or_404( DepenseFull , pk=pkdep )
    if request.method == "POST":
        form = DepenseFullForm(request.POST,instance=mydep)
        if form.is_valid():
            mydep = form.save(commit=False)
            mydep.modifiepar = request.user.username
            mydep.save()
            localpkcc=mydep.structlev3.pk
            return redirect('depensefull_parcc',pkcc=localpkcc)

        else:
            print ('form not valid')
    else:
        form = DepenseFullForm( instance=mydep)
    return render(request, 'depensefull_edit.html', {'form': form})


""" -----------------------------------------------------------------
En test - programme pour uploader des fichiers en Django
------------------------------------------------------------------- """
def handle_uploaded_file(f, filepathandname):
    with open(filepathandname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


""" -----------------------------------------------------------------
Création depenses dans le budget - en cours de tests
Les structures sont classées par niveau .
On commence par le niveau 0
En dépenses on prend les types dep
------------------------------------------------------------------- """
@login_required
def depensefull_new2(request):

    #desc11=Classification.objects.all().filter(type="1")
    structlev1s = Structure.objects.all().filter(type=" cf",parentid="0")
    structlev2s = ""
#Structure.objects.all().filter(type=" cc")
    cptdeplev1s = "" #NatureComptable.objects.all().filter(nctype="dep")
    domfoncs = DomaineFonctionnel.objects.all().order_by('dfcode') #filter(dfgrpcumul='LOLF_CUMUL')

    plfis = "" #PlanFinancement.objects.all()

    budget = PeriodeBudget.objects.filter(bloque=False).first()
# pour les autorisations creer un dico avec les objets
    structlev1ok = []
    for i in structlev1s:
        if is_authorised(request.user.username,i.name):
            structlev1ok.append(i)

    structlev2ok = []
    for j in structlev2s:
        if is_authorised(request.user.username,j.name):
            structlev2ok.append(i)
       #else:
        #    structlev1pok.append(i)

    if request.method == "POST":
        struct1 = Structure.objects.filter(id=request.POST.get("structlev1")).first()
        struct2ref=request.POST.get("structlev2").split("-----")
        struct2id=struct2ref[0]
        struct2 = Structure.objects.filter(id=struct2id).first()

        struct3ref=request.POST.get("structlev3").split('-----')
        struct3id=struct3ref[0]
        struct3 = Structure.objects.filter(id=struct3id).first()

        cptdev1ref = request.POST.get("cptdeplev1").split('-----')
        cptdev1id = cptdev1ref[0]
        cptdev1 = NatureComptable.objects.filter(id=cptdev1id).first()

        domfonc = DomaineFonctionnel.objects.filter(id=request.POST.get("domfonc")).first()

        plfiid=request.POST.get("plfi").split("--")[0]
        plfi = PlanFinancement.objects.filter(id=plfiid).first()

        if request.POST.get("montantdg"):
            montantdg = request.POST.get("montantdg")
        else:
            montantdg = 0

        if request.POST.get("montantdc"):
            montantdc = request.POST.get("montantdc")
        else:
            montantdc = 0

        if request.POST.get("montantae"):
            montantae = request.POST.get("montantae")
        else:
            montantae =0

        if request.POST.get("montantcp"):
            montantcp = request.POST.get("montantcp")
        else:
            montantcp = 0

        if request.POST.get("dateae"):
            dateae = request.POST.get("dateae")
        else:
            dateae = "" 

        if request.POST.get("commentaire"):
            commentaire = request.POST.get("commentaire")
        else:
            commentaire =""

        madepense = DepenseFull()
        madepense.structlev1 = struct1
        madepense.structlev2 = struct2
        madepense.structlev3 = struct3
        madepense.cptdeplev1 = cptdev1
        madepense.domfonc = domfonc
        madepense.plfi = plfi
        madepense.montant=montantdg
        madepense.montantdc = montantdc 
        madepense.montantae = montantae
        madepense.dateae = dateae
        madepense.montantcp = montantcp
        madepense.commentaire = commentaire
        madepense.periodebudget = budget
        #username = None
        #if request.user.is_authenticated():
        #    username = request.user.username
        madepense.creepar = request.user.username
        #madepense.creepar = username
        madepense.modifiepar = request.user.username

        #handle_uploaded_file(request.Files['file'],'/tmp/file1.txt')
        #madepense.noms_des_fichiers=request.Files['file']
        madepense.save()
        madepense.myid = madepense.id
        madepense.save()

        localpkcc=madepense.structlev3.pk
        return redirect('depensefull_parcc',pkcc=localpkcc)

    else:
        return render(request, 'depensefull_new_v2.html', {
                                                       'structlev1s': structlev1ok ,
                                                       'structlev2s': structlev2ok,
                                                       'cptdeplev1s': cptdeplev1s,
                                                       'domfoncs': domfoncs,
                         })


@login_required
def depensefull_new_avec_pfi(request,struct3id,pfiid):
    """---------------------------------------------
    Avec le formulaire prérempli .
    -----------------------------------------------"""

    budget = PeriodeBudget.objects.filter(bloque=False).first()

    if request.method == "POST":
        struct1 = Structure.objects.filter(id=request.POST.get("structlev1")).first()
        struct2ref=request.POST.get("structlev2").split("-----")
        struct2id=struct2ref[0]
        struct2 = Structure.objects.filter(id=struct2id).first()

        struct3ref=request.POST.get("structlev3").split('-----')
        struct3id=struct3ref[0]
        struct3 = Structure.objects.filter(id=struct3id).first()

        cptdev1ref = request.POST.get("cptdeplev1").split('-----')
        cptdev1id = cptdev1ref[0]
        cptdev1 = NatureComptable.objects.filter(id=cptdev1id).first()

        domfonc = DomaineFonctionnel.objects.filter(id=request.POST.get("domfonc")).first()

        plfiid=request.POST.get("plfi").split("--")[0]
        plfi = PlanFinancement.objects.filter(id=plfiid).first()


        if request.POST.get("montantdc"):
            montantdc = request.POST.get("montantdc")
        else:
            montantdc = 0

        if request.POST.get("montantae"):
            montantae = request.POST.get("montantae")
        else:
            montantae = 0

        if request.POST.get("montantcp"):
            montantcp = request.POST.get("montantcp")
        else:
            montantcp = 0

        if request.POST.get("dateae"):
            dateae = request.POST.get("dateae")
        else:
            dateae = ""

        if request.POST.get("commentaire"):
            commentaire = request.POST.get("commentaire")
        else:
            commentaire = ""

        madepense = DepenseFull()
        madepense.structlev1 = struct1
        madepense.structlev2 = struct2
        madepense.structlev3 = struct3
        madepense.cptdeplev1 = cptdev1
        madepense.domfonc = domfonc
        madepense.plfi = plfi
        madepense.montantdc = montantdc
        madepense.montantae = montantae
        madepense.dateae = dateae
        madepense.montantcp = montantcp
        madepense.commentaire = commentaire
        madepense.periodebudget = budget
        #username = None
        #if request.user.is_authenticated():
        #    username = request.user.username
        madepense.creepar = request.user.username
        #madepense.creepar = username
        madepense.modifiepar = request.user.username

        #handle_uploaded_file(request.Files['file'],'/tmp/file1.txt')
        #madepense.noms_des_fichiers=request.Files['file']
        madepense.save()
        madepense.myid = madepense.id
        madepense.save()

        localpkcc=madepense.structlev3.pk
        #return redirect('depensefull_parcc',pkcc=localpkcc)
        return redirect('liste_pfi_avec_depenses_recettes')
    else:
        plfi = get_object_or_404(PlanFinancement,pk=pfiid)
        struct3id=" "+struct3id
        struct3 = get_object_or_404(Structure,name=struct3id,type=' cf')
        struct2 = get_object_or_404(Structure,myid=struct3.parentid)
        struct1 = get_object_or_404(Structure,myid=struct2.parentid)

        domfoncs = DomaineFonctionnel.objects.all().order_by('dfcode') #filter(dfgrpcumul='LOLF_CUMUL')

        return render(request, 'depensefull_new_v3.html', {
                                                       'struct1': struct1,
                                                       'struct2': struct2,
                                                       'struct3': struct3,
                                                       'domfoncs': domfoncs,
                                                       'plfin':plfi,
                         })



@login_required
def recettefull_new_avec_pfi(request,struct3id,pfiid):
    """---------------------------------------------
    Avec le formulaire prérempli .
    -----------------------------------------------"""

    budget = PeriodeBudget.objects.filter(bloque=False).first()

    if request.method == "POST":
        struct1 = Structure.objects.filter(id=request.POST.get("structlev1")).first()
        struct2ref=request.POST.get("structlev2").split("-----")
        struct2id=struct2ref[0]
        struct2 = Structure.objects.filter(id=struct2id).first()
        struct3ref=request.POST.get("structlev3").split('-----')
        struct3id=struct3ref[0]
        struct3 = Structure.objects.filter(id=struct3id).first()

        cptdev1ref = request.POST.get("cptdeplev1").split('-----')
        cptdev1id = cptdev1ref[0]
        cptdev1 = NatureComptable.objects.filter(id=cptdev1id).first()

        plfiid=request.POST.get("plfi").split("--")[0]
        plfi = PlanFinancement.objects.filter(id=plfiid).first()

        if request.POST.get("montantdc"):
            montantdc = request.POST.get("montantdc")
        else:
            montantdc = 0

        if request.POST.get("montantar"):
            montantar = request.POST.get("montantar")
        else:
            montantar = 0

        if request.POST.get("montantre"):
            montantre = request.POST.get("montantre")
        else:
            montantre = 0

        if request.POST.get("commentaire"):
            commentaire = request.POST.get("commentaire")
        else:
            commentaire = ""

        marecette = RecetteFull()
        marecette.structlev1 = struct1
        marecette.structlev2 = struct2
        marecette.structlev3 = struct3
        marecette.cptdeplev1 = cptdev1

        marecette.plfi = plfi
        marecette.montantdc = montantdc
        marecette.montantar = montantar
        marecette.montantre = montantre
        marecette.commentaire = commentaire
        marecette.periodebudget=budget

        marecette.creepar = request.user.username
        marecette.modifiepar = request.user.username
        marecette.save()
        marecette.myid = marecette.id
        marecette.save()
        localpkcp=marecette.structlev3.pk
        #return redirect('recettefull_parcp',pkcp=localpkcp)
        return redirect('liste_pfi_avec_depenses_recettes')
    else:
        plfi = get_object_or_404(PlanFinancement,pk=pfiid)
        struct3id=" "+struct3id
        struct3 = get_object_or_404(Structure,name=struct3id,type=' cf')
        #print("struct2id: "+str(struct3.myid))
        struct2 = get_object_or_404(Structure,myid=struct3.parentid)
        struct1 = get_object_or_404(Structure,myid=struct2.parentid)

        #domfoncs = DomaineFonctionnel.objects.all().order_by('dfcode') #filter(dfgrpcumul='LOLF_CUMUL')
        # le fond est calcule a partir de l enveloppe = nature comptable
        return render(request, 'recettefull_new_v3.html', {
                                                       'struct1': struct1,
                                                       'struct2': struct2,
                                                       'struct3': struct3,
                                                       'plfin':plfi,
                         })





""" -----------------------------------------------------------------
Liste des depenses dans le budget
------------------------------------------------------------------- """
def depensefull_list(request):
    if request.method == "POST":
        depstruct = request.POST['depstruct']
        depcomptcompt = request.POST['depcomptcompt']
        if depstruct == "" and depcomptcompt == "" :
            mydep = DepenseFull.objects.all().order_by('structlev1','structlev2','structlev3')
        elif depstruct == "" :
            mydep = DepenseFull.objects.filter ( structure__icontains = depstruct ).order_by('structlev1','structlev2','structlev3')
        elif depcomptcompt == "" :
            mydep = DepenseFull.objects.filter ( cptdeplev1__icontains = depcomptcompt ).order_by('structlev1','structlev2','structlev3')
        else:
            mydep = DepenseFull.objects.filter( structure__icontains = depstruct ).filter( cptdeplev1__icontains = depcomptcompt ).order_by('structlev1','structlev2','structlev3')
    else:
        mydep = DepenseFull.objects.all().order_by('structlev1','structlev2','structlev3')

    return render(request, 'depensefull_lists.html', {'depenses':mydep})


""" -----------------------------------------------------------------
Liste des depenses dans le budget associées à un CC
------------------------------------------------------------------- """
def depensefull_parcc(request,pkcc):
    madep=Structure.objects.get(id=pkcc)
    #parent1=Structure.objects.filter(myid=madep.parentid).first()
    #parent2=Structure.objects.filter(myid=parent1.id).first()
    mydep = DepenseFull.objects.filter (structlev3=madep).order_by('structlev1','structlev2','structlev3')
    total = DepenseFull.objects.filter (structlev3=madep).aggregate(Sum('montant'))
    totaldc=DepenseFull.objects.filter (structlev3=madep).aggregate(Sum('montantdc'))
    totalcp=DepenseFull.objects.filter (structlev3=madep).aggregate(Sum('montantcp'))
    totalae=DepenseFull.objects.filter (structlev3=madep).aggregate(Sum('montantae'))
    lev2 = Structure.objects.get(myid=madep.parentid)
    lev1 = Structure.objects.get(myid=lev2.parentid)
    return render(request, 'depensefullcc_lists.html', {'depenses':mydep, 'total':total , 'totaldc':totaldc, 'totalcp':totalcp,'totalae':totalae,'pkcc':pkcc,'mastructurelev1':lev1,'mastructurelev2':lev2,'mastructurelev3':madep})


""" -----------------------------------------------------------------
Liste des recettes dans le budget associées à un CP
------------------------------------------------------------------- """
def recettefull_parcp(request,pkcp):
    madep=Structure.objects.get(id=pkcp)
    #parent1=Structure.objects.filter(myid=madep.parentid).first()
    #parent2=Structure.objects.filter(myid=parent1.id).first()
    myrec = RecetteFull.objects.filter (structlev3=madep).order_by('structlev1','structlev2','structlev3')
    total=RecetteFull.objects.filter (structlev3=madep).aggregate(Sum('montant'))
    totalar=RecetteFull.objects.filter (structlev3=madep).aggregate(Sum('montantar'))
    totalre=RecetteFull.objects.filter (structlev3=madep).aggregate(Sum('montantre'))
    totaldc=RecetteFull.objects.filter (structlev3=madep).aggregate(Sum('montantdc'))
    lev2 = Structure.objects.get(myid=madep.parentid)
    lev1 = Structure.objects.get(myid=lev2.parentid)
    return render(request, 'recettefullcp_lists.html', {'recettes':myrec, 'total':total, 'totaldc':totaldc ,
                                         'totalar':totalar,'totalre':totalre,'pkcp':pkcp,'mastructurelev1':lev1,
                                         'mastructurelev2':lev2,'mastructurelev3':madep})



def depensefull_listregroup(request):
    if request.method == "POST":
        depstruct = request.POST['depstruct']
        depcomptcompt = request.POST['depcomptcompt']
        if depstruct == "" and depcomptcompt == "" :
            mydep = DepenseFull.objects.all().order_by('structlev1','structlev2','structlev3')
        elif depstruct == "" :
            mydep = DepenseFull.objects.filter ( structure__icontains = depstruct ).order_by('structlev1','structlev2','structlev3')
        elif depcomptcompt == "" :
            mydep = DepenseFull.objects.filter ( cptdeplev1__icontains = depcomptcompt ).order_by('structlev1','structlev2','structlev3')
        else:
            mydep = DepenseFull.objects.filter( structure__icontains = depstruct ).filter( cptdeplev1__icontains = depcomptcompt ).order_by('structlev1','structlev2','structlev3')
    else:
        mydep = DepenseFull.objects.all().order_by('structlev1','structlev2','structlev3')

    return render(request, 'depensefull_listsregroup.html', {'depenses':mydep})


def total1(self):
    qs=DepenseFull.objects.filter(id=self).aggregate(Sum('montant'))
    sum=qs['amount__sum']
    if not sum:
        sum=0.00
    return sum





def depensefull_delete(request,pkdep):
    mydep = get_object_or_404( DepenseFull , pk=pkdep )
    if request.method== "POST":
        form = DepenseForm(request.POST, instance=mydep)
        if form.is_valid():
            mydep.delete()
            return redirect('depensefull_list')
    else:
        form = DepenseFullForm( instance=mydep )
        return render(request, 'depensefull_delete.html', {'form': form})

def depensefull_delete2(request,pkdep):
    mydep = get_object_or_404( DepenseFull , pk=pkdep )
    if request.method== "POST":
        localpkcc=mydep.structlev3.pk
        form = DepenseForm(request.POST, instance=mydep)
        if form.is_valid():
            mydep.delete()
            return redirect('depensefull_parcc', pkcc=localpkcc )
    else:
        form = DepenseFullForm( instance=mydep )
        return render(request, 'depensefull_delete2.html', {'form': form})


def depensefull_detail( request,pkdep ):
    mydep = get_object_or_404( DepenseFull , pk=pkdep )
    return render(request, 'depensefull_detail.html', {'depense':mydep})

def depensefull_detail2( request,pkdep):
    mydep = get_object_or_404( DepenseFull , pk=pkdep )
    return render(request, 'depensefull_detail2.html', {'depense':mydep})


def depensefull_deleteall(request):
    if request.method == "POST":
        html=[]
        html.append('Elements supprimes:')
        html.append(DepenseFull.objects.count())
        html.append('<br>')
        html.append('Suppression de tous les elements de la table des Depenses')

        alldepenses = DepenseFull.objects.all()
        for depense in alldepenses:
            depense.delete()

        html.append('Elements restants:')
        html.append(DepenseFull.objects.count())
        html.append('<br>')
        return HttpResponse(html)
    else:
        nbdepense = DepenseFull.objects.count()
        return render(request, 'depense_deleteall.html',{'nb':nbdepense})



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
            todo_items.append(str(s.id)+"-----"+str(s.enveloppe)+"-----"+str(s.fondbudget_recette)+"-----"+str(s.ccbd))
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


#Depenses Ajax find structure level 2 from level1
def ajax_add_todo1(request,pkstr1):
    if request.is_ajax():
        #print("called by ajax")
        myid=Structure.objects.get(id=pkstr1).myid
        #print("thekey:"+myid)
        struct2qset=Structure.objects.all().filter(parentid=myid).order_by('name')

        structlev2ok = []
        for j in struct2qset:
            if is_authorised(request.user.username,j.name):
                structlev2ok.append(j)


        todo_items=[]
        #todo_items=['test 1', 'test 2',]
        #todo_items.append('toto')
        for s in structlev2ok:
            todo_items.append(str(s.id)+"-----"+str(s.name)+"-----"+str(s.label))
        print(todo_items)
        data = json.dumps(todo_items)
        #data=json.dumps(struct2qset)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


#Recettes Ajax find structure level 2 from level1
def ajax_recadd_todo1(request,pkstr1):
    if request.is_ajax():
        myid=Structure.objects.get(id=pkstr1).myid
        struct2qset=Structure.objects.all().filter(parentid=myid).order_by('name')
        todo_items=[]
        structlev2ok = []
        for j in struct2qset:
            if is_authorised(request.user.username,j.name):
                structlev2ok.append(j)

        for s in structlev2ok:
            todo_items.append(str(s.id)+"-----"+str(s.name)+"-----"+str(s.label))
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404



#Depenses ajax find struct level3 from level2
def ajax_findstruct_lev3(request,pkstr1):
    #print ("calling_add_todo1")
    if request.is_ajax():
        #print("called by ajax")
        myid=Structure.objects.get(id=pkstr1).myid
        #print("recherche des fils de thekey:"+myid)
        struct2qset=Structure.objects.all().filter(parentid=myid).order_by('name')
        todo_items=[]
        #print("recherche des fils de thekey:"+myid+ " nb trouves:" + str(len(struct2qset)))
        structlev3ok = []
        for j in struct2qset:
            if is_authorised(request.user.username,j.name):
                structlev3ok.append(j)

        for s in structlev3ok:
            todo_items.append(str(s.id)+"-----"+str(s.name)+"-----"+str(s.label))
        #print(todo_items)
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

#Recettes ajax find struct level3 from level2
def ajax_recfindstruct_lev3(request,pkstr1):
    #print ("calling_add_todo1")
    if request.is_ajax():
        #print("called by ajax")
        myid=Structure.objects.get(id=pkstr1).myid
        #print("thekey:"+myid)
        struct2qset=Structure.objects.all().filter(parentid=myid).order_by('name')
        todo_items=[]
        #todo_items=['test 1', 'test 2',]
        #todo_items.append('toto')

        structlev3ok = []
        for j in struct2qset:
            if is_authorised(request.user.username,j.name):
                #print('testons:' + request.user.username+"::"+j.name)
                structlev3ok.append(j)

        for s in structlev3ok:
            todo_items.append(str(s.id)+"-----"+str(s.name)+"-----"+str(s.label))
        #print(todo_items)
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


#Depenses ajax_add_cptdev_lev2
def ajax_add_cptdev_lev2(request,pkcpt):
    #print ("calling_add_cptdev")
    if request.is_ajax():
        #print("called by ajax cptdev")
        struct2qset=NatureComptable.objects.all().filter(ccparent=pkcpt)
        todo_items=[]
        for s in struct2qset:
            todo_items.append(str(s.ccid)+"-----"+str(s.ccname)+"-----"+str(s.cclabel))
        #print(todo_items)
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


#Recettes ajax_add_cptdev_lev2
def ajax_recadd_cptdev_lev2(request,pkcpt):
    #print ("calling_add_cptdev")
    if request.is_ajax():
        #print("called by ajax cptdev")
        struct2qset=NatureComptable.objects.all().filter(ccparent=pkcpt)
        todo_items=[]
        for s in struct2qset:
            todo_items.append(str(s.ccid)+"-----"+str(s.ccname)+"-----"+str(s.cclabel))
        #print(todo_items)
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


#Depenses ajax find origine des fonds
def ajax_findorigfond_lev2(request,pkor):
    #print ("calling_findorigfond")
    ofid=OrigineFonds.objects.get(id=pkor).ofid
    #print ("ofid :"+str(ofid))
    if request.is_ajax():
        qset=OrigineFonds.objects.all().filter(ofparent=ofid)
        todo_items=[]
        for s in qset:
            todo_items.append(str(s.ofname)+"-----"+str(s.oflabel))
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

#Recettes ajax find origine des fonds
def ajax_recfindorigfond_lev2(request,pkor):
    #print ("calling_findorigfond")
    ofid=OrigineFonds.objects.get(id=pkor).ofid
    #print ("ofid :"+str(ofid))
    if request.is_ajax():
        qset=OrigineFonds.objects.all().filter(ofparent=ofid)
        todo_items=[]
        for s in qset:
            todo_items.append(str(s.ofname)+"-----"+str(s.oflabel))
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404



def ajax_more_todo11(request):
    #print ("calling_more_todo1111")
    if request.is_ajax():
        todo_items=['test 1', 'test 2',]
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def ajax_more_todo1(request):
    #print ("calling_more_todo1")
    if request.is_ajax():
        todo_items=['test 1', 'test 2',]
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


#---------------------------------------------------------------------"""
#---

def recettefull_new(request):
    if request.method == "POST":
        form = RecetteFullForm(request.POST)
        if form.is_valid():
            newrecette = form.save(commit=False)
            newrecette.creepar = request.user.username
            newrecette.save()
            return redirect('recettefull_list')
    else:
        form = RecetteFullForm()
    return render(request, 'recettefull_new.html', {'form': form})


def recettefull_new3(request):
    if request.method == "POST":
        form = RecetteFullForm(request.POST)
        if form.is_valid():
            newrecette = form.save(commit=False)
            newrecette.creepar = request.user.username
            newrecette.save()
            return redirect('recettefull_list')
    else:
        form = RecetteFullForm()
    return render(request, 'recettefull_new3.html', {'form': form})


def recettefull_new2(request):

    structlev1s = Structure.objects.all().filter(type=" cf",parentid="0")
    structlev2s = ""
    cptdeplev1s = "" 
    cptdeplev2s = ""
    domfoncs = ""
    plfis = "" 
    budget = PeriodeBudget.objects.all().filter(bloque=False).first()

    if request.method == "POST":
        struct1 = Structure.objects.filter(id=request.POST.get("structlev1")).first()
        struct2ref=request.POST.get("structlev2").split("-----")
        struct2id=struct2ref[0]
        struct2 = Structure.objects.filter(id=struct2id).first()
        struct3ref=request.POST.get("structlev3").split('-----')
        struct3id=struct3ref[0]
        struct3 = Structure.objects.filter(id=struct3id).first()

        cptdev1ref = request.POST.get("cptdeplev1").split('-----')
        cptdev1id = cptdev1ref[0]
        cptdev1 = NatureComptable.objects.filter(id=cptdev1id).first()

        plfiid=request.POST.get("plfi").split("--")[0]
        plfi = PlanFinancement.objects.filter(id=plfiid).first()

        if request.POST.get("montant"):
            montant = request.POST.get("montant")
        else:
            montant = 0

        if request.POST.get("montantdc"):
            montantdc = request.POST.get("montantdc")
        else:
            montantdc = 0

        if request.POST.get("montantar"):
            montantar = request.POST.get("montantar")
        else:
            montantar = 0

        if request.POST.get("montantre"):
            montantre = request.POST.get("montantre")
        else:
            montantre = 0

        if request.POST.get("commentaire"):
            commentaire = request.POST.get("commentaire")
        else:
            commentaire = ""

        marecette = RecetteFull()
        marecette.structlev1 = struct1
        marecette.structlev2 = struct2
        marecette.structlev3 = struct3
        marecette.cptdeplev1 = cptdev1

        marecette.plfi = plfi
        marecette.montantdc = montantdc
        marecette.montantar = montantar
        marecette.montantre = montantre
        marecette.commentaire = commentaire
        marecette.periodebudget=budget

        marecette.creepar = request.user.username
        marecette.modifiepar = request.user.username
        marecette.save()
        marecette.myid = marecette.id
        marecette.save()
        localpkcp=marecette.structlev3.pk

        return redirect('recettefull_parcp',pkcp=localpkcp)
    else:
        return render(request, 'recettefull_new_v2.html', {'structlev1s': structlev1s ,'structlev2s': structlev2s,
                                                           'cptdeplev1s': cptdeplev1s,
                                                           'domfoncs': domfoncs , 
                                                           'plfis': plfis})


def recettefull_list(request):
    if request.method == "POST":
        depstruct = request.POST['depstruct']
        depcomptcompt = request.POST['depcomptcompt']
        if depstruct == "" and depcomptcompt == "" :
            mydep = RecetteFull.objects.all()
        elif depstruct == "" :
            mydep = RecetteFull.objects.filter ( structure__icontains = depstruct )
        elif depcomptcompt == "" :
            mydep = RecetteFull.objects.filter ( cptdeplev1__icontains = depcomptcompt )
        else:
            mydep = RecetteFull.objects.filter( structure__icontains = depstruct ).filter( cptdeplev1__icontains = depcomptcompt )
    else:
        mydep = RecetteFull.objects.all()

    return render(request, 'recettefull_lists.html', {'recettes':mydep})


def recettefull_delete(request,pkrec):
    myrec = get_object_or_404( RecetteFull , pk=pkrec )
    if request.method== "POST":
        form = RecetteFullForm(request.POST, instance=myrec)
        if form.is_valid():
            myrec.delete()
            return redirect('recettefull_list')
    else:
        form = RecetteFullForm( instance=myrec )
        return render(request, 'recettefull_delete.html', {'form': form})


def recettefull_delete2(request,pkrec):
    myrec = get_object_or_404( RecetteFull , pk=pkrec )
    if request.method== "POST":
        localpkcc=myrec.structlev3.pk
        form = RecetteFullForm(request.POST, instance=myrec)
        if form.is_valid():
            myrec.delete()
            return redirect('recettefull_parcp', pkcp=localpkcc)
    else:
        form = RecetteFullForm( instance=myrec )
        return render(request, 'recettefull_delete2.html', {'form': form})



def recettefull_detail( request,pkrec ):
    myrec = get_object_or_404( RecetteFull , pk=pkrec )
    return render(request, 'recettefull_detail.html', {'recette':myrec})


def recettefull_detail2( request,pkrec ):
    myrec = get_object_or_404( RecetteFull , pk=pkrec )
    return render(request, 'recettefull_detail2.html', {'recette':myrec})



def recettefull_deleteall(request):
    if request.method == "POST":
        html=[]
        html.append('Elements supprimes:')
        html.append(RecetteFull.objects.count())
        html.append('<br>')
        html.append('Suppression de tous les elements de la table des recettes')

        allrecettes = RecetteFull.objects.all()
        for recette in allrecettes:
            recette.delete()

        html.append('Elements restants:')
        html.append(RecetteFull.objects.count())
        html.append('<br>')
        return HttpResponse(html)
    else:
        nbrecette = RecetteFull.objects.count()
        return render(request, 'recette_deleteall.html',{'nb':nbrecette})


def recettefull_edit(request,pkrec):
    myrec = get_object_or_404( RecetteFull , pk=pkrec )
    if request.method == "POST":
        form = RecetteFullForm(request.POST,instance=myrec)
        if form.is_valid():
            myrec = form.save(commit=False)
            myrec.modifiepar = request.user.username
            myrec.save()
            return redirect('recettefull_list')
        else:
            print ('form not valid')
    #else:
    form = RecetteFullForm( instance=myrec)
    return render(request, 'recettefull_edit.html', {'form': form})


def recettefull_edit2(request,pkrec):
    myrec = get_object_or_404( RecetteFull , pk=pkrec )
    if request.method == "POST":
        #form = RecetteFullForm(request.POST,instance=myrec)
        #if form.is_valid():
        #    myrec = form.save(commit=False)
        myrec.montant=request.POST['montant']
        myrec.montantar=request.POST['montantar']
        myrec.montantre=request.POST['montantre']
        myrec.montantdc=request.POST['montantdc']
        myrec.modifiepar = request.user.username
        myrec.save()
        #localpkcp=myrec.structlev3.pk
        #return redirect('recettefull_parcp',pkcp=localpkcp)
        return redirect('liste_pfi_avec_depenses_recettes')

    #else:
    form = RecetteFullForm( instance=myrec)
    return render(request, 'recettefull_edit.html', {'form': form})



def depensefull_edit2(request,pkdep):
    mydep = get_object_or_404( DepenseFull , pk=pkdep )
    if request.method == "POST":
        mydep.montant=request.POST['montant']
        mydep.montantdc=request.POST['montantdc']
        mydep.montantcp=request.POST['montantcp']
        mydep.montantae=request.POST['montantae']
        mydep.modifiepar = request.user.username
        mydep.save()
        #localpkcp=myrec.structlev3.pk
        #return redirect('recettefull_parcp',pkcp=localpkcp)
        return redirect('liste_pfi_avec_depenses_recettes')

    #else:
    form = DepenseFullForm( instance=mydep)
    return render(request, 'depensefull_edit.html', {'form': form})




