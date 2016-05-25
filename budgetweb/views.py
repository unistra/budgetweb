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
from django.db.models import Sum
#--------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views

from django.contrib.auth.models import Group
#---------------------------------------------------------------------------------

#@login_required(login_url='/accounts/login/')

def search(request):
    pass

#---------------------------------------




#@login_required
def home(request):
    return render_to_response('base.html')

#emptygrid.html  notemptygrid2.html  notemptygrid3.html  notemptygrid.html

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


#"""------------------
#class Authorisation(models.Model):
#    username = models.CharField(max_length=100)
#    object = models.CharField(max_length=100)
#-----------------------------------------"""

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
	

def authorisation_user(request,myuser=""):
    mytauth=Authorisation.objects.filter(username=myuser)
    return render(equest, 'authorisation_lists.html', {'Authorisation':myauth})


def is_authorised(myuser, myobject):
    # chercher les autorisations dans la table
    # si il y a * dans la table, ok tout
    # si il y a qqch* alors detailler
    # si autorisation exacte ok
    #print ("called with :"+myuser+"::"+myobject)
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


def authorisation_delete(request,pkauth):
    myauth = get_object_or_404(Authorisation,pk=pkauth)
    if request.method== "POST":
        print(request.POST)
        form = AuthorisationForm(request.POST, instance=myauth)
        if form.is_valid():
            myauth.delete()
            return redirect('authorisation_list')
    else:
        form = AuthorisationForm(instance=myauth)
        return render(request, 'authorisation_delete.html', {'form': form})




def authorisation_detail(request,pkauth):
    myauth = get_object_or_404(Authorisation, pk=pkauth)
    return render(request, 'authorisation_detail.html', {'Authorisation':myauth})



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
    else:
        lechemin="vide2"
    return render(request, 'authorisation_import.html', {'lechemin': "", 'lemessage':""})


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


# ------------------------------------------
#class PeriodeBudget(models.Model):
#    name = models.CharField(max_length=20)
#    label = models.CharField(max_length=100)
#    annee = models.DateField(blank=True , null=True)
#-------------------------------------------

def periodebudget_new(request):
    if request.method == "POST":
        form = PeriodeBudgetForm(request.POST)
        if form.is_valid():
            newbud = form.save(commit=False)
            newbud.save()
            return redirect('periodebudget_list')
        else:
            print ('form not valid')
    else:
        form = PeriodeBudgetForm()
    return render(request, 'periodebudget_new.html', {'form': form})


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


def periodebudget_delete(request,pkpb):
    mycc = get_object_or_404( CompteComptable,pk=pkpb )
    if request.method== "POST":
        print(request.POST)
        form = PeriodebudgetForm(request.POST, instance=mycc)
        if form.is_valid():
            mycc.delete()
            return redirect('periodebudget_list')
    else:
        form = PeriodeBudgetForm( instance=mycc )
        return render(request, 'periodebudget_delete.html', {'form': form})


def periodebudget_detail( request,pkpb ):
    mycc = get_object_or_404( PeriodeBudget , pk=pkpb )
    return render(request, 'periodebudget_detail.html', {'reponse':mycc})



""" ***********************************
class CompteComptable(models.Model):
    ccid = models.CharField(max_length=100)
    ccparent = models.CharField(max_length=100)
    ccname = models.CharField(max_length=100)
    cclabel = models.CharField(max_length=100)
    cctype = models.Charfield(max_length=100)
    ccinput = models.CharField(max_length=100)
    cctypectrl = models.CharField(max_length=100)
*************************************** """

def comptecomptable_new(request):
    if request.method == "POST":
        form = CompteComptableForm(request.POST)
        if form.is_valid():
            newcc = form.save(commit=False)
            newcc.save()
            return redirect('comptecomptable_list')
        else:
            print ('form not valid')
    else:
        form = CompteComptableForm()
    return render(request, 'comptecomptable_new.html', {'form': form})


def comptecomptable_list(request):
    if request.method == "POST":
        ccname = request.POST['ccname']
        cclabel  = request.POST['cclabel']
        if ccname == "" and cclabel == "" :
            mycc = CompteComptable.objects.all()
        elif cclabel == "" :
            mycc = CompteComptable.objects.filter ( ccname__icontains = ccname )
        elif ccname == "" :
            mycc = CompteComptable.objects.filter ( cclabel__icontains = cclabel )
        else:
            mycc = CompteComptable.objects.filter( ccname__icontains = ccname ).filter( cclabel__icontains = cclabel )
    else:
        mycc = CompteComptable.objects.all()

    return render(request, 'comptecomptable_lists.html', {'reponses':mycc})


def comptecomptable_delete(request,pkcc):
    mycc = get_object_or_404( CompteComptable,pk=pkcc )
    if request.method== "POST":
        print(request.POST)
        form = CompteComptableForm(request.POST, instance=mycc)
        if form.is_valid():
            mycc.delete()
            return redirect('comptecomptable_list')
    else:
        form = CompteComptableForm( instance=mycc )
        return render(request, 'comptecomptable_delete.html', {'form': form})


def comptecomptable_detail( request,pkcc ):
    mycc = get_object_or_404( CompteComptable , pk=pkcc )
    return render(request, 'comptecomptable_detail.html', {'reponse':mycc})


def comptecomptable_importcsv(request):
    if request.method == "POST":
        if request.POST.get("lechemin"):
             lemessage=""
             lechemin=request.POST.get("lechemin")
             fichier = open(lechemin, "r")
             nblignes=0
             for ligne in fichier:
                 if ligne.strip():
                     nblignes = nblignes+1
                     moncc = CompteComptable()
                     ligne=ligne.split(";")
                     moncc.ccid = ligne[0]
                     moncc.ccparent = ligne[1]
                     moncc.ccname = ligne[2]
                     moncc.cclabel = ligne[3]
                     moncc.cctype = ligne[4]
                     moncc.ccinput = ligne[5]
                     moncc.cctypectrl = ligne[1]
                     moncc.save()
             lemessage=lemessage+ "  ok fichier "+ lechemin+ " importé "+ str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"comptecomptable_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'comptecomptable_import.html', {'lechemin': "", 'lemessage':""})
    else:
        lechemin="vide2"
    return render(request, 'comptecomptable_import.html', {'lechemin': "", 'lemessage':""})



def comptecomptable_deleteall(request):
    if request.method == "POST":
        html=[]
        html.append('Elements supprimes:')
        html.append(CompteComptable.objects.count())
        html.append('<br>')
        html.append('Suppression de tous les elements de la table des comptes comptables')

        mycc = CompteComptable.objects.all()
        for cc in mycc:
            cc.delete()

        html.append('Elements restants:')
        html.append(CompteComptable.objects.count())
        html.append('<br>')
        return HttpResponse(html)
    else:
        nbcc = CompteComptable.objects.count()
        return render(request, 'comptecomptable_deleteall.html',{'nb':nbcc})


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

    return render(request, 'originefonds_lists.html', {'reponses':myof})

def originefonds_delete(request,pkof):
    myof = get_object_or_404( OrigineFonds , pk=pkdf )
    if request.method== "POST":
        form = OrigineFondsForm(request.POST, instance=myof)
        if form.is_valid():
            myof.delete()
            return redirect('originefonds_list')
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
    myid = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    parentid = models.CharField(max_length=100)
    ordre = models.CharField(max_length=100)
    niv = models.CharField(max_length=100)
    bloq = models.CharField(max_length=100)
    modifdate = models.CharField(max_length=100)
    modifpar = models.CharField(max_length=100)
    dfmc = models.CharField(max_length=100)
    fdr = models.CharField(max_length=100)
******************************************************************  """
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


def structure_detail( request,pkst ):
    myst = get_object_or_404( Structure , pk=pkst )
    return render(request, 'structure_detail.html', {'reponse':myst})


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


""" ----------------------------------------------------------------

class PlanFinancement(models.Model):
    name = models.CharField(max_length=100)
    label  = models.CharField(max_length=100)
    type   = models.CharField(max_length=100)
    budget = models.CharField(max_length=100)
    nomades= models.CharField(max_length=100)
    refsifac= models.CharField(max_length=100, default="")
    refdfi  = models.CharField(max_length=100, default="")
    societe = models.CharField(max_length=100, default="")
    ccassoc = models.CharField(max_length=100, default="")
    cpassoc = models.CharField(max_length=100, default="")
    responsable = models.CharField(max_length=100, default="")
    dordre = models.CharField(max_length=100, default="")
    divirecette = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=100, default="")
    cleregul = models.CharField(max_length=100, default="")
    domainefonc = models.CharField(max_length=100, default="")
--------------------------------------------------------------  """

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
    mypfi = get_object_or_404( PlanFinancement , pk=pkpfi )
    if request.method== "POST":
        form = PlanFinancementForm(request.POST, instance=mypfi)
        if form.is_valid():
            mypfi.delete()
            return redirect('planfinancement_list')
    else:
        form = PlanFinancementForm( instance=myst )
        return render(request, 'planfinancement_delete.html', {'form': form})


def planfinancement_detail( request,pkpfi ):
    mypfi = get_object_or_404( PlanFinancement , pk=pkpfi )
    return render(request, 'planfinancement_detail.html', {'reponse':mypfi})


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


def planfinancement_importcsv(request):
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
             lemessage=lemessage+ "  ok fichier "+ lechemin+ " importé "+ str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"planfinancement_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'planfinancement_import.html', {'lechemin': "", 'lemessage':""})
    else:
        lechemin="vide2"
    return render(request, 'planfinancement_import.html', {'lechemin': "", 'lemessage':""})


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


""" -----------------------------------------------------------------
class Depense ( models.Model ):
    myid = models.CharField(max_length=100)
    struct = models.ForeignKey ('Structure',blank=True, null=True)
    cptdep = models.ForeignKey ('CompteComptable', blank=True , null=True)
    domfonc = models.ForeignKey ('DomaineFonctionnel' , blank = True , null = True )
    orfonds = models.ForeignKey ( 'OrigineFonds' , blank = True , null = True ) 
    plfi = models.ForeignKey ( 'PlanFinancement' , blank = True , null = True )
    montant = models.CharField ( max_length = 100 )
    commentaire = models.CharField (max_length = 100)

------------------------------------------------------------------- """

def depense_new(request):
    if request.method == "POST":
        form = DepenseForm(request.POST)
        if form.is_valid():
            newdepense = form.save(commit=False)
            newdepense.save()
            return redirect('depense_list')
        else:
            print ('form not valid')
    else:
        form = DepenseForm()
    return render(request, 'depense_new.html', {'form': form})


def depense_list(request):
    if request.method == "POST":
        depstruct = request.POST['depstruct']
        depcomptcompt = request.POST['depcomptcompt']
        if depstruct == "" and depcomptcompt == "" :
            mydep = Depense.objects.all()
        elif depstruct == "" :
            mydep = Depense.objects.filter ( structure__icontains = depstruct )
        elif depcomptcompt == "" :
            mydep = Depense.objects.filter ( cptdep__icontains = depcomptcompt )
        else:
            mydep = Depense.objects.filter( structure__icontains = depstruct ).filter( cptdep__icontains = depcomptcompt )
    else:
        mydep = Depense.objects.all()

    return render(request, 'depense_lists.html', {'depenses':mydep})


def depense_delete(request,pkdep):
    mydep = get_object_or_404( Depense , pk=pkdep )
    if request.method== "POST":
        form = DepenseForm(request.POST, instance=mydep)
        if form.is_valid():
            mydep.delete()
            return redirect('depense_list')
    else:
        form = DepenseForm( instance=mydep )
        return render(request, 'depense_delete.html', {'form': form})


def depense_detail( request,pkdep ):
    mydep = get_object_or_404( Depense , pk=pkdep )
    return render(request, 'depense_detail.html', {'depense':mydep})


def depense_importcsv(request):
    if request.method == "POST":
        if request.POST.get("lechemin"):
             lemessage=""
             lechemin=request.POST.get("lechemin")
             fichier = open(lechemin, "r")
             nblignes=0
             for ligne in fichier:
                 if ligne.strip():
                     nblignes = nblignes+1
                     madepense = Depense()
                     ligne = ligne.split(";")
                     madepense.myid = ligne[0]
                     madepense.struct = ligne[1]
                     madepense.cptdep = ligne[2]
                     madepense.domfonc = ligne[3]
                     madepense.orfonds = ligne[4]
                     madepense.plfi = ligne[5]
                     madepense.montant = ligne[6]
                     madepense.commentaire = ligne[7]
                     madepense.save()
             lemessage=lemessage+ "  ok fichier "+ lechemin+ " importé "+ str(nblignes) +" lignes trouvées."
             fichier.close()
             return render(request,"depense_import.html",{'lemessage':lemessage})
        else:
             return render(request, 'depense_import.html', {'lechemin': "", 'lemessage':""})
    else:
        lechemin="vide2"
    return render(request, 'depense_import.html', {'lechemin': "", 'lemessage':""})


def depense_deleteall(request):
    if request.method == "POST":
        html=[]
        html.append('Elements supprimes:')
        html.append(Depense.objects.count())
        html.append('<br>')
        html.append('Suppression de tous les elements de la table des Depenses')

        alldepenses = Depense.objects.all()
        for depense in alldepenses:
            depense.delete()

        html.append('Elements restants:')
        html.append(Depense.objects.count())
        html.append('<br>')
        return HttpResponse(html)
    else:
        nbdepense = Depense.objects.count()
        return render(request, 'depense_deleteall.html',{'nb':nbdepense})

#-----V2 de depenses
def depense_new2(request):
    if request.method == "POST":
        form = DepenseForm2(request.POST)
        if form.is_valid():
            newdepense = form.save(commit=False)
            newdepense.save()
            return redirect('depense_list')
        else:
            print ('form not valid')
    else:
        form = DepenseForm2()
    return render(request, 'depense_new.html', {'form': form})


""" ----------------------------------------------------------------------------

-------------------------------------------------------------------------- """
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


def depensefull_edit(request,pkdep):
    mydep = get_object_or_404( DepenseFull , pk=pkdep )
    if request.method == "POST":
        form = DepenseFullForm(request.POST,instance=mydep)
        if form.is_valid():
            mydep = form.save(commit=False)
            mydep.modifiepar = request.user.username
            mydep.save()
            return redirect('depensefull_list')
        else:
            print ('form not valid')
    else:
        form = DepenseFullForm( instance=mydep)
    return render(request, 'depensefull_edit.html', {'form': form})





def handle_uploaded_file(f, filepathandname):
    with open(filepathandname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
def depensefull_new2(request):

    #desc11=Classification.objects.all().filter(type="1")
    structlev1s = Structure.objects.all().filter(type=" cf",parentid="0")
    structlev2s = "" 
#Structure.objects.all().filter(type=" cc")
    cptdeplev1s = CompteComptable.objects.all().filter(cctype="dep",ccparent="1")
    cptdeplev2s = "" #CompteComptable.objects.all()
    domfoncs = DomaineFonctionnel.objects.all().filter(dfgrpcumul='LOLF_CUMUL')
#    orfonds = OrigineFonds.objects.all().filter(oftype="cc",ofparent="0" )
    orfonds = OrigineFonds.objects.all().filter(oftype="cc",ofid="1" )

    plfis = PlanFinancement.objects.all()

    budget = PeriodeBudget.objects.filter(bloque=False).first()
# pour les autorisations creer un dico avec le sobjets
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

        cptdev1 = CompteComptable.objects.filter(ccid=request.POST.get("cptdeplev1")).first()
        cptdev2ref=request.POST.get("cptdeplev2").split('-----')
        cptdev2id = cptdev2ref[0]
        cptdev2 = CompteComptable.objects.filter(ccid=cptdev2id).first()
        domfonc = DomaineFonctionnel.objects.filter(id=request.POST.get("domfonc")).first()
        orfond = OrigineFonds.objects.filter(id=request.POST.get("orfond")).first()
        orfond2 = OrigineFonds.objects.filter(id=request.POST.get("orfond2")).first()

        plfi = PlanFinancement.objects.filter(id=request.POST.get("plfi")).first()

        if request.POST.get("montantdc"):
            montantdc = request.POST.get("montantdc")
        if request.POST.get("montantae"):
            montantae = request.POST.get("montantae")
        if request.POST.get("montantcp"):
            montantcp = request.POST.get("montantcp")
        if request.POST.get("dateae"):
            dateae = request.POST.get("dateae")

        if request.POST.get("commentaire"):
            commentaire = request.POST.get("commentaire")
        if request.POST.get("myid"):
            myid = request.POST.get("myid")

        madepense = DepenseFull()
        madepense.myid = "myid"
        madepense.structlev1 = struct1
        madepense.structlev2 = struct2
        madepense.structlev3 = struct3
        madepense.cptdeplev1 = cptdev1
        madepense.cptdeplev2 = cptdev2
        madepense.domfonc = domfonc
        madepense.orfonds = orfond
        #madepense.orfonds2 = orfondi2
        madepense.plfi = plfi
        madepense.montant=0.00
        madepense.montantdc = montantdc   #montantdc
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
        # if form.is_valid():
        #    newdepense = form.save(commit=False)
        #   newdepense.save()
        #  return redirect('depensefull_list')
        # else:
        #     print ('form not valid')
        return redirect('depensefull_parcc',pkcc=localpkcc)

    else:
        print("autorisations pour : "+str(len(structlev1ok)))
        return render(request, 'depensefull_new_v2.html', {'structlev1s': structlev1ok ,'structlev2s': structlev2ok,
                                                           'cptdeplev1s': cptdeplev1s, 'cptdeplev2s':cptdeplev2s,
                                                           'domfoncs': domfoncs , 'orfonds': orfonds,
                                                           'plfis': plfis})





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


def depensefull_parcc(request,pkcc):
    madep=Structure.objects.get(id=pkcc)
    #parent1=Structure.objects.filter(myid=madep.parentid).first()
    #parent2=Structure.objects.filter(myid=parent1.id).first()
    mydep = DepenseFull.objects.filter (structlev3=madep).order_by('structlev1','structlev2','structlev3')
    totaldc=DepenseFull.objects.filter (structlev3=madep).aggregate(Sum('montantdc'))
    totalcp=DepenseFull.objects.filter (structlev3=madep).aggregate(Sum('montantcp'))
    totalae=DepenseFull.objects.filter (structlev3=madep).aggregate(Sum('montantae'))
    lev2 = Structure.objects.get(myid=madep.parentid)
    lev1 = Structure.objects.get(myid=lev2.parentid) 
    return render(request, 'depensefullcc_lists.html', {'depenses':mydep, 'totaldc':totaldc, 'totalcp':totalcp,'totalae':totalae,'pkcc':pkcc,'mastructurelev1':lev1,'mastructurelev2':lev2,'mastructurelev3':madep})


def recettefull_parcp(request,pkcp):
    madep=Structure.objects.get(id=pkcp)
    #parent1=Structure.objects.filter(myid=madep.parentid).first()
    #parent2=Structure.objects.filter(myid=parent1.id).first()
    myrec = RecetteFull.objects.filter (structlev3=madep).order_by('structlev1','structlev2','structlev3')
    total=RecetteFull.objects.filter (structlev3=madep).aggregate(Sum('montant'))
    totalar=RecetteFull.objects.filter (structlev3=madep).aggregate(Sum('montantar'))
    totalre=RecetteFull.objects.filter (structlev3=madep).aggregate(Sum('montantre'))
    lev2 = Structure.objects.get(myid=madep.parentid)
    lev1 = Structure.objects.get(myid=lev2.parentid)
    return render(request, 'recettefullcp_lists.html', {'recettes':myrec, 'total':total, 'totalar':totalar,'totalre':totalre,'pkcp':pkcp,'mastructurelev1':lev1,'mastructurelev2':lev2,'mastructurelev3':madep})



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

#Depenses Ajax find structure level 2 from level1
def ajax_add_todo1(request,pkstr1):
    print ("calling_add_todo1")
    if request.is_ajax():
        #print("called by ajax")
        myid=Structure.objects.get(id=pkstr1).myid
        #print("thekey:"+myid)
        struct2qset=Structure.objects.all().filter(parentid=myid)
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
    #print ("calling_add_todo1")
    if request.is_ajax():
        myid=Structure.objects.get(id=pkstr1).myid
        #print("thekey:"+myid)
        struct2qset=Structure.objects.all().filter(parentid=myid)
        todo_items=[]
        #todo_items=['test 1', 'test 2',]
        #todo_items.append('toto')
        #print('username:'+request.user.username)
        structlev2ok = []
        for j in struct2qset:
            if is_authorised(request.user.username,j.name):
                structlev2ok.append(j)

        for s in structlev2ok:
            todo_items.append(str(s.id)+"-----"+str(s.name)+"-----"+str(s.label))
        #print(todo_items)
        data = json.dumps(todo_items)
        #data=json.dumps(struct2qset)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404



#Depenses ajax find struct level3 from level2
def ajax_findstruct_lev3(request,pkstr1):
    #print ("calling_add_todo1")
    if request.is_ajax():
        #print("called by ajax")
        myid=Structure.objects.get(id=pkstr1).myid
        print("recherche des fils de thekey:"+myid)
        struct2qset=Structure.objects.all().filter(parentid=myid)
        todo_items=[]
        print("recherche des fils de thekey:"+myid+ " nb trouves:" + str(len(struct2qset)))
        structlev3ok = []
        for j in struct2qset:
            if is_authorised(request.user.username,j.name):
                print('testons1:' + request.user.username+"::"+j.name)
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
        struct2qset=Structure.objects.all().filter(parentid=myid)
        todo_items=[]
        #todo_items=['test 1', 'test 2',]
        #todo_items.append('toto')

        structlev3ok = []
        for j in struct2qset:
            if is_authorised(request.user.username,j.name):
                print('testons:' + request.user.username+"::"+j.name)
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
        struct2qset=CompteComptable.objects.all().filter(ccparent=pkcpt)
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
        struct2qset=CompteComptable.objects.all().filter(ccparent=pkcpt)
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


#""" -------------------------------------------
#class RecetteFull ( models.Model ):
#    myid = models.CharField(max_length=100)
#    structlev1 = models.ForeignKey ('Structure',blank=True, null=True, related_name='structlev1')
#    structlev2 = models.ForeignKey ('Structure',blank=True, null=True, related_name='structlev2')
#    structlev3 = models.ForeignKey ('Structure',blank=True, null=True, related_name='structlev3')

#    cptdeplev1 = models.ForeignKey ('CompteComptable', blank=True , null=True, related_name='cptdeplev1')
#    cptdeplev2 = models.ForeignKey ('CompteComptable', blank=True , null=True, related_name='cptdeplev2')

#    domfonc = models.ForeignKey ('DomaineFonctionnel' , blank = True , null = True )
#    orfonds = models.ForeignKey ( 'OrigineFonds' , blank = True , null = True , related_name='orfonds')
#    orfonds2 = models.ForeignKey ( 'OrigineFonds' , blank = True , null = True , related_name='orfonds2')
#    plfi = models.ForeignKey ( 'PlanFinancement' , blank = True , null = True )
#    montant = models.CharField ( max_length = 100 ,blank = True , null = True )
    
#    montantdc = models.DecimalField(max_digits=12, decimal_places=2 , blank = True , null = True )
#    montantar = models.DecimalField(max_digits=12, decimal_places=2 , blank = True , null = True )
#    montantre = models.DecimalField(max_digits=12, decimal_places=2 , blank = True , null = True )
#    commentaire = models.CharField (max_length = 100 , blank=True , null = True)

#    myfile = forms.FileField()

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
            print ('form not valid')
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
            print ('form not valid')
    else:
        form = RecetteFullForm()
    return render(request, 'recettefull_new3.html', {'form': form})


def recettefull_new2(request):

    #desc11=Classification.objects.all().filter(type="1")
    structlev1s = Structure.objects.all().filter(type=" cf",parentid="0")
    structlev2s = ""
#Structure.objects.all().filter(type=" cc")
    cptdeplev1s = CompteComptable.objects.all().filter(cctype="rec",ccparent="150")
    cptdeplev2s = "" #CompteComptable.objects.all()
    domfoncs = DomaineFonctionnel.objects.all() #.filter(dfgrpcumul='LOLF_CUMUL')
    orfonds = OrigineFonds.objects.all().filter(oftype="cp",ofparent="0" )
    plfis = PlanFinancement.objects.all()
    budget = PeriodeBudget.objects.all().filter(bloque=False).first()

    if request.method == "POST":
        struct1 = Structure.objects.filter(id=request.POST.get("structlev1")).first()
        struct2ref=request.POST.get("structlev2").split("-----")
        struct2id=struct2ref[0]
        struct2 = Structure.objects.filter(id=struct2id).first()
        struct3ref=request.POST.get("structlev3").split('-----')
        struct3id=struct3ref[0]
        struct3 = Structure.objects.filter(id=struct3id).first()

        cptdev1 = CompteComptable.objects.filter(ccid=request.POST.get("cptdeplev1")).first()
        cptdev2ref=request.POST.get("cptdeplev2").split('-----')
        cptdev2id = cptdev2ref[0]
        cptdev2 = CompteComptable.objects.filter(ccid=cptdev2id).first()
        domfonc = DomaineFonctionnel.objects.filter(id=request.POST.get("domfonc")).first()
        orfond = OrigineFonds.objects.filter(id=request.POST.get("orfond")).first()
        orfond2 = OrigineFonds.objects.filter(id=request.POST.get("orfond2")).first()

        plfi = PlanFinancement.objects.filter(id=request.POST.get("plfi")).first()

        if request.POST.get("montant"):
            montant = request.POST.get("montant")
        if request.POST.get("montantar"):
            montantar = request.POST.get("montantar")
        if request.POST.get("montantre"):
            montantre = request.POST.get("montantre")

        if request.POST.get("commentaire"):
            commentaire = request.POST.get("commentaire")
        if request.POST.get("myid"):
            myid = request.POST.get("myid")

        madepense = RecetteFull()
        madepense.myid = "myid"
        madepense.structlev1 = struct1
        madepense.structlev2 = struct2
        madepense.structlev3 = struct3
        madepense.cptdeplev1 = cptdev1
        madepense.cptdeplev2 = cptdev2
        madepense.domfonc = domfonc
        madepense.orfonds = orfond
        #madepense.orfonds2 = orfondi2
        madepense.plfi = plfi
        madepense.montant = montant
        #madepense.montantdc = montantdc
        madepense.montantar = montantar
        madepense.montantre = montantre
        madepense.commentaire = commentaire
        madepense.periodebudget=budget
        #handle_uploaded_file(request.Files['file'],'/tmp/file1.txt')
        #madepense.noms_des_fichiers=request.Files['file']

        #username = None
        #if request.user.is_authenticated():
        #    username = request.user.username
        madepense.creepar = request.user.username
        madepense.modifiepar = request.user.username
        madepense.save()
        madepense.myid = madepense.id
        madepense.save()
        localpkcp=madepense.structlev3.pk
        # if form.is_valid():
        #    newdepense = form.save(commit=False)
        #   newdepense.save()
        #  return redirect('depensefull_list')
        # else:
        #     print ('form not valid')
        return redirect('recettefull_parcp',pkcp=localpkcp)

    else:
        return render(request, 'recettefull_new_v2.html', {'structlev1s': structlev1s ,'structlev2s': structlev2s,
                                                           'cptdeplev1s': cptdeplev1s, 'cptdeplev2s':cptdeplev2s,
                                                           'domfoncs': domfoncs , 'orfonds': orfonds,
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
    else:
        form = RecetteFullForm( instance=myrec)
    return render(request, 'recettefull_edit.html', {'form': form})



