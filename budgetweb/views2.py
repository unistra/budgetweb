from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.

from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.middleware import csrf 
import os
from . import views
from .forms import AuthorisationForm, CompteComptableForm , DomaineFonctionnelForm
from .forms import OrigineFondsForm, StructureForm , PlanFinancementForm , DepenseForm
from .models import Authorisation, CompteComptable , DomaineFonctionnel , PeriodeBudget
from .models import OrigineFonds , Structure , PlanFinancement , Depense , DepenseFull , RecetteFull
from .forms import DepenseForm2 , DepenseFullForm , RecetteFullForm , PeriodeBudgetForm
from django.template import RequestContext
from decimal import *
from django.contrib.auth.decorators import login_required


def rapporthtmlheadersrc():
    html = []
    html.append('<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">')
    html.append('<html xmlns=\"http://www.w3.org/1999/xhtml\">')
    html.append('<head>\n')
    html.append('<meta http-equiv=\"Cache-Control\" content=\"no-cache\"/>') 
    html.append('<meta http-equiv=\"pragma\" content=\"no-cache\"/>') 
    html.append('<meta http-equiv=\"expires\" content=\"-1\"/>') 
    html.append('<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />')
    html.append('<title>Budget Sifac - version :  0.1 | 2016</title>')
    html.append('<link href=\"/budgetweb/site_media/css/styl.css\" rel=\"stylesheet\" type=\"text/css\" />')
    html.append('<script type=\"text/javascript\" language=\"javascript\" src=\"/static/js/lib.js\"></script>')
    html.append('<script type=\"text/javascript\" language=\"javascript\">')
    html.append('<!--[if gte IE 9 ]><link rel="stylesheet" type="text/css" href="/static/photoinfos/_styles.css" media="screen"><![endif]--> ')
    html.append('<!--[if !IE]>--><link rel="stylesheet" type="text/css" href="/static/photoinfos/_styles.css" media="screen"><!--<![endif]--> ')


    html.append('var pb = 4;')
    html.append('</script>')
    html.append('</head>\n')
    html.append(' \n <br>')

    html.append('<body class="fl-theme-app">')
    html.append('<div id="header" class="app-header fl-container-auto">')
    html.append('<div class="logo"></div><div class="header_suite">')
    html.append('<div id="titreAppli" class="titreAppli">')
    html.append('<span class="span_bigTitre">BudgetWeb</span><br/>')
    html.append('<span class="span_titre">Application de gestion du budget Sifac par le web</span>')
    html.append('</div>')
    html.append('<div class="user_displayName">')
    html.append('         <span class="span_currentUser"></span>')
    html.append('</div>')
    html.append('<div class="version">')
    html.append('<span class="span_version">Version  0.1 | 2016</span>')
    html.append('</div></div></div><div id="welcomepages"><div class="app-body"><div class="app-content">')
    html.append('<div class=""></div>')
    html.append('<br/>')
    html.append('<form id="form1" name="form1" method="post" action=".">')

    html.append('<a href=".">Accueil</a> > 	<br />')
    html.append('<br />')
    html.append('<a href="?ag=1">agr&eacuteger</a>')
    html.append('<br />')
    html.append('<br />')
    html.append('<table cellpadding="0" cellspacing="0" width=\'98%\' align=\'center\'>')
    html.append('<tr class="th">')
    html.append('   <th rowspan="2"><span class="cf">CF</span> / <span class="cp">Rec.</span> / <span class="cc">D&eacute;p.</span></th>')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">Budget initial (BP)</th>   ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">Transferts</th>            ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">Ress.Affect.</th>          ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">DBM (DM1)</th>             ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="3">Budget actualis&eacute;</th>')
    html.append('</tr>  ')
    html.append('<tr class="th">')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <th>bal.</th>')
    html.append('</tr>')
    return html



def rapporthtmlheadersrc():
    html = []
    html.append('<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">')
    html.append('<html xmlns=\"http://www.w3.org/1999/xhtml\">')
    html.append('<head>\n')
    html.append('<meta http-equiv=\"Cache-Control\" content=\"no-cache\"/>')
    html.append('<meta http-equiv=\"pragma\" content=\"no-cache\"/>')
    html.append('<meta http-equiv=\"expires\" content=\"-1\"/>')
    html.append('<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />')
    html.append('<title>Budget Sifac - version :  0.1 | 2016</title>')
    html.append('<link href=\"/budgetweb/site_media/css/styl.css\" rel=\"stylesheet\" type=\"text/css\" />')
    html.append('<script type=\"text/javascript\" language=\"javascript\" src=\"/static/js/lib.js\"></script>')
    html.append('<script type=\"text/javascript\" language=\"javascript\">')
    html.append('var pb = 4;')
    html.append('</script>')
    html.append('</head>\n')
    html.append(' \n <br>')

    html.append('<body class="fl-theme-app">')
    html.append('<div id="header" class="app-header fl-container-auto">')
    html.append('<div class="logo"></div><div class="header_suite">')
    html.append('<div id="titreAppli" class="titreAppli">')
    html.append('<span class="span_bigTitre">BudgetWeb</span><br/>')
    html.append('<span class="span_titre">Application de gestion du budget Sifac par le web</span>')
    html.append('</div>')
    html.append('<div class="user_displayName">')
    html.append('         <span class="span_currentUser"></span>')
    html.append('</div>')
    html.append('<div class="version">')
    html.append('<span class="span_version">Version  0.1 | 2016</span>')
    html.append('</div></div></div><div id="welcomepages"><div class="app-body"><div class="app-content">')
    html.append('<div class=""></div>')
    html.append('<br/>')
    html.append('<form id="form1" name="form1" method="post" action=".">')

    html.append('<a href=".">Accueil</a> >      <br />')
    html.append('<br />')
    html.append('<a href="?ag=1">agr&eacuteger</a>')
    html.append('<br />')
    html.append('<br />')
    html.append('<table cellpadding="0" cellspacing="0" width=\'98%\' align=\'center\'>')
    html.append('<tr class="th">')
    html.append('   <th rowspan="2"><span class="cf">CF</span> / <span class="cp">Rec.</span> / <span class="cc">D&eacute;p.</span></th>')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">Budget initial (BP)</th>   ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">Transferts</th>            ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">Ress.Affect.</th>          ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">DBM (DM1)</th>             ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="3">Budget actualis&eacute;</th>')
    html.append('</tr>  ')
    html.append('<tr class="th">')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <th>bal.</th>')
    html.append('</tr>')
    return html



def rapporthtmlheader(request=None):
    html = []
    html.append('<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">')
    html.append('<html xmlns=\"http://www.w3.org/1999/xhtml\">')
    html.append('<head>\n')
    html.append('<meta http-equiv=\"Cache-Control\" content=\"no-cache\"/>')
    html.append('<meta http-equiv=\"pragma\" content=\"no-cache\"/>')
    html.append('<meta http-equiv=\"expires\" content=\"-1\"/>')
    html.append('<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />')
    html.append('<title>Budget Sifac - version :  0.1 | 2016</title>')
    html.append('<link href=\"/budgetweb/site_media/css/styl.css\" rel=\"stylesheet\" type=\"text/css\" />')
#    html.append('<script type=\"text/javascript\" language=\"javascript\" src=\"/static/js/lib.js\"></script>')
    html.append('<script type="text/javascript" src="/static/photoinfos/dtree.js"></script>')
    html.append('<script type=\"text/javascript\" language=\"javascript\">')
    html.append('<!--[if gte IE 9 ]><link rel="stylesheet" type="text/css" href="/static/css/_styles.css" media="screen"><![endif]-->  ')
    html.append('<!--[if !IE]>--><link rel="stylesheet" type="text/css" href="/static/css/_styles.css" media="screen"><!--<![endif]--> ')
    #<script src="{% static 'js/mainjds.js' %}"></script>

    html.append('var pb = 4;')
    html.append('</script>')
    html.append('</head>\n')
    html.append(' \n <br>')

    html.append('<body class="fl-theme-app">')
    html.append('<div id="header" class="app-header fl-container-auto">')
    html.append('<div class="logo"></div><div class="header_suite">')
    html.append('<div id="titreAppli" class="titreAppli">')
    html.append('<span class="span_bigTitre">BudgetWeb</span><br/>')
    html.append('<span class="span_titre">Application de gestion du budget Sifac par le web</span>')
    html.append('</div>')
    html.append('<div class="user_displayName">')
    html.append('         <span class="span_currentUser"></span>')
    html.append('</div>')
    html.append('<div class="version">')
    html.append('<span class="span_version">Version  0.1 | 2016</span>')
    html.append('</div></div></div><div id="welcomepages"><div class="app-body"><div class="app-content">')
    html.append('<div class=""></div>')
    html.append('<br/>')
    html.append('<form id="form1" name="form1" method="POST" action="">')

    moncsrf=csrf.get_token(request)
    html.append('<script> function cfover() {} ; function cfout() {}; </script>')
    html.append('<input type="hidden" name=\'csrfmiddlewaretoken\' value=\''+moncsrf+'\'><input type="submit" value="">')

    html.append('<a href=".">Accueil</a> >      <br />')
    html.append('<br />')
    html.append('<a href="?ag=1">agr&eacuteger</a>')
    html.append('<br />')
    html.append('<br />')
    return html

def tableheader():
    html=[]
    #document.getElementId(id).click()
    html.append('<script> var clickminus= function(id) { temp="clicked"+id; document.getElementsByName(temp)[0].removeAttribute("disabled"); } </script>')
    html.append('<table cellpadding="0" cellspacing="0" width=\'98%\' align=\'center\'>')

    html.append('<tr class="th">')
    html.append('   <th rowspan="2"><span class="cf">CF</span> / <span class="cp">Rec.</span> / <span class="cc">D&eacute;p.</span></th>')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">Budget initial (BP)</th>   ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">Transferts</th>            ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">Ress.Affect.</th>          ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="2">DBM (DM1)</th>             ')
    html.append('     <td class="bl">&nbsp;</td>         ')
    html.append('   <th colspan="3">Budget actualis&eacute;</th>')
    html.append('</tr>  ')
    html.append('<tr class="th">')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <td class="bl">&nbsp;</td>')
    html.append('    <th>d&eacute;p.</th>')
    html.append('    <th>rec.</th>')
    html.append('    <th>bal.</th>')
    html.append('</tr>')
    return html







def rapporthtmlfooter():
    html = []
    html.append('</table> <br /> </form> ')
    html.append('<img src="/budgetweb/site_media/images/plus.png">')


    html.append(' </body> </html>')
    return html 


def sectionheader( title ):
    html = []
    html.append('<div class="containerjds"> ')
    html.append('<div class="header"><span>Expand</span>')

    html.append('</div> ')
    html.append('<div class="content">')
    html.append('    <ul> ')
    html.append('<li>')
    # contenu
    return html


def sectionfooter():
    html = []
    html.append('</li>') 
    html.append('    </ul> ')
    html.append('</div> ')
    html.append('</div> ')
    return html


def totalrecette(moncp):
    parent1=Structure.objects.filter(myid=moncp.parentid).first()
    parent2=Structure.objects.filter(myid=parent1.parentid).first()
    lesrecettes=RecetteFull.objects.filter(structlev3=parent1)
    montotal=Decimal(0.00)
    for mesrec in lesrecettes:
        if mesrec.montant != None:
            montotal = montotal+Decimal(mesrec.montant)

    return "<center>- &nbsp; &nbsp; &nbsp;</center>" if montotal==Decimal(0.00) else montotal


def totaldepense(moncc):
    parent1=Structure.objects.filter(myid=moncc.parentid).first()
    parent2=Structure.objects.filter(myid=parent1.parentid).first()
    lesdepenses=DepenseFull.objects.filter(structlev3=parent2)
    montotal=Decimal(0.00)
    for mesdep in lesdepenses:
        if mesdep.montantdc != None:
            montotal = montotal+Decimal(mesdep.montantdc)

    return "<center>- &nbsp; &nbsp; &nbsp;</center>" if montotal==Decimal(0.00) else montotal 


def htmlforcpcc(peremyid,pereid,decalage):
    html=[]
    lesfils=Structure.objects.all().filter(parentid=peremyid).filter(type=" cp").order_by('name')
    localpere = lesfils.first()
    localperemyid=localpere.myid
    #lespttsfils2=Structure.objects.all().filter(parentid=localperemyid).order_by('name')
    for pttfils2 in lesfils:
        pttfils2desc1  = unicode(pttfils2.name)+"++"+str(pttfils2.type) if pttfils2.name else "nom_vide"
        pttfils2myid = str(pttfils2.myid)
        pttfils2label= unicode(pttfils2.label)
        # il y a 13 colonnes
        html.append('<tr onmouseover="cfover(this)" onmouseout="cfout(this)" class="thcc">')
        html.append('<td class="tx"> <span class="traits"> &nbsp;&#9474;')
        i=decalage
        while i>0:
            html.append(' &nbsp;')
            i-=1
        html.append(' &#9492;</span>')
        html.append('<!-- position:relative -->')
        html.append('<a style=\'padding-top:120px;\' name="1977">')
        html.append('<a class="cp info" href="">'+pttfils2desc1 + '<span>' + pttfils2label+'</span></a></td>')
        html.append('     <td class="bl">&nbsp;</td>         ')
        html.append('<td>'+""+'</td>')
        html.append('<td align="center"><a href="../recettefull/'+pereid+'/parcp/">'+str(totalrecette(pttfils2))+'</a></td>')
        html.append('     <td class="bl">&nbsp;</td>         ')
        html.append('<td>' + "" +'</td>')
        html.append('<td></td>')
        html.append('     <td class="bl">&nbsp;</td>         ')
        html.append('<td>' + "" + '</td>')
        html.append('<td>' + "" + '</td>')
        html.append('     <td class="bl">&nbsp;</td>         ')
        html.append('<td>' + "" + '</td>')
        html.append('<td></td>')
        html.append('     <td class="bl">&nbsp;</td>         ')
        html.append('<td></td>')
        html.append('<td></td>')
        html.append('<td></td>')
        html.append('</tr> \n')

        lespttsfils3=Structure.objects.all().filter(parentid=pttfils2myid).order_by('name')
        for pttfils3 in lespttsfils3:
            pttfils3desc1  = unicode(pttfils3.name)+"++"+pttfils3.type if pttfils3.name else "nom_vide"
            pttfils3myid = str(pttfils3.myid)
            pttfils3label = unicode(pttfils3.label)

            html.append('<tr onmouseover="cfover(this)" onmouseout="cfout(this)" class="thcc">')
            html.append('<td class="tx"> <span class="traits"> &nbsp;&#9474;')
            i=decalage+1
            while i>0:
                html.append(' &nbsp')
                i-=1
            html.append(' &#9492;</span>')
            html.append('<!-- position:relative -->')
            html.append('<a style=\'padding-top:120px;\' name="1977">')
            html.append('<a class="cc info" href="">'+pttfils3desc1 + '<span>' + pttfils3label+'</span></a></td>')
            html.append('     <td class="bl">&nbsp;</td>         ')
            html.append('<td align="center"><a href="../depensefull/'+pereid+'/parcc/">'+ str(totaldepense(pttfils3))+'</a></td>')
            html.append('<td></td>')
            html.append('     <td class="bl">&nbsp;</td>         ')
            html.append('<td>' + "" +'</td>')
            html.append('<td></td>')
            html.append('     <td class="bl">&nbsp;</td>         ')
            html.append('<td>' + "" + '</td>')
            html.append('<td>' + "" + '</td>')
            html.append('     <td class="bl">&nbsp;</td>         ')
            html.append('<td>' + "" + '</td>')
            html.append('<td></td>')
            html.append('     <td class="bl">&nbsp;</td>         ')
            html.append('<td></td>')
            html.append('<td></td>')
            html.append('<td></td>')
            html.append('</tr> \n')

    return html





#par CF/ CC/CP 
@login_required
def menu_list14tree(request, isexpanded=[]):
    photos=Structure.objects.all().filter(type=" cf",parentid="0").order_by('name') 

    if request.method == "POST":
        for key, value in request.POST.items():
            #print(key, value)
            if "clicked" in key:
                clickednode=value
        clickednode=clickednode.split("-")
        clickedphoto = Structure.objects.get(myid=int(clickednode[0]))
        if int(clickednode[1]) == 1 :
            myid = clickedphoto.myid 
            if myid in isexpanded:
                isexpanded.remove(myid)
            else:
                isexpanded.append(myid)
        if int(clickednode[1]) == 2 :
            myid = clickedphoto.myid
            if myid in isexpanded:
                isexpanded.remove(myid)
            else:
                isexpanded.append(myid)
        if int(clickednode[1]) == 3 :
            myid = clickedphoto.myid
            if myid in isexpanded:
                isexpanded.remove(myid)
            else:
                isexpanded.append(myid)
        if int(clickednode[1]) == 4 :
            myid = clickedphoto.myid
            if myid in isexpanded:
                isexpanded.remove(myid)
            else:
                isexpanded.append(myid)
        if int(clickednode[1]) == 6 :
            myid = clickedphoto.myid
            if myid in isexpanded:
                isexpanded.remove(myid)
            else:
                isexpanded.append(myid)

    html = tableheader() 
    html2=[]
    html3=[]
    htmlheader=[]
    htmlfooter=[]
    prevdesc1=""
    prevdesc2=""
    prevdesc3=""
    prevdescdate=""
    nodeindex=1
 
    htmlheader=rapporthtmlheader(request) 
#-------------------------
    lastdesc4=0
    lastdesc3=0
    lastdesc2=0
    lastdesc1=0
#-------------------------
    #html.append('<ol class="tree">  ')
    passone = 1 
    for p in photos:     #step 1
        desc1  = unicode(p.name)+"++"+p.type if p.name else "nom_vide"
        myid = str(p.myid) if p.myid else "nom_vide"
        theid = str(p.id) if p.id else "nom_vide"
        desc2  = str(p.myid) if p.myid else "nom_vide"
        mylabel  = unicode(p.label) if p.label else "nom_vide" 
        desc3  = "" 
        desc4  = ""
        descdate = desc4
        
        thetop=0
        lenom = unicode(p.name)

        pkkey='<a href="../'+myid+'/edit/"</a>'+ lenom
        pluspng='/budgetweb/site_media/images/plus.png'
        moinspng = '/budgetweb/site_media/images/moins.png'

        # premier niveau - que des CF
        # il y a 13 colonnes
        html.append('<tr onmouseover="cfover(this)" onmouseout="cfout(this)" class="thcf"> ')
        html.append('<td class="tx"><span class="traits"></span> ')
        if myid in isexpanded:
            html.append('<input disabled type="hidden" name="clicked'+myid+str(-1)+'" value='+myid+str(-1)+'>')
            html.append('<input type="image" id=\''+myid+str(-1)+'\' onclick=clickminus(this.id) ')
            html.append(' src="'+moinspng+'" alt="save" value="save" class="pm" /></a>  ')
        else:
            html.append('<input disabled type="hidden" name="clicked'+myid+str(-1)+'" value='+myid+str(-1)+'>')
            html.append('<input type="image" id=\''+myid+str(-1)+'\' onclick=clickminus(this.id) ')
            html.append(' src="'+pluspng+'" alt="save" value="save" class="pm" /></a>  ')

        html.append('<!-- position:relative --> ')
        html.append('<a style=\'padding-top:120px;\' name="966"> ')
        html.append('<a class="cf info" href="">'+ desc1 + '<span>' + mylabel+'</span></a></td> ')
        html.append('<td class="bl">&nbsp;</td> ')
        html.append('<td class="mt"><a href="" class="cf">-&nbsp; &nbsp; &nbsp;</a></td> ')
        html.append('<td class="mt"><a href="" class="cf">-&nbsp; &nbsp; &nbsp;</a></td> ')
        html.append('<td class="bl">&nbsp;</td> ')
        html.append('<td class="mt"><a href="" class="cf">-&nbsp; &nbsp; &nbsp;</a></td> ')
        html.append('<td class="mt"><a href="" class="cf">-&nbsp; &nbsp; &nbsp;</a></td> ')
        html.append('<td class="bl">&nbsp;</td> ')
        html.append('<td class="mt"><a href="" class="cf">-&nbsp; &nbsp; &nbsp;</a></td> ')
        html.append('<td class="mt"><a href="" class="cf">-&nbsp; &nbsp; &nbsp;</a></td> ')
        html.append('<td class="bl">&nbsp;</td> ')
        html.append('<td class="mt"><a href="" class="cf">-&nbsp; &nbsp; &nbsp;</a></td>')
        html.append('<td class="mt"><a href="" class="cf">-&nbsp; &nbsp; &nbsp;</a></td>')
        html.append('<td class="bl">&nbsp;</td>')
        html.append('<td class="mt"><a href="" class="cf">-&nbsp; &nbsp; &nbsp;</a></td> ')
        html.append('<td class="mt"><a href="" class="cf">-&nbsp; &nbsp; &nbsp;</a></td>')
        html.append('<td class="mt"><a href="" class="cf">-&nbsp; &nbsp; &nbsp;</a></td>')
        html.append('</tr>')


        if myid in isexpanded: #step 2
                #trouver les fils puis rebelote pour isexpanded.
                #lesfils=Structure.objects.all().filter(parentid=myid).filter(type=" cp").order_by('name')
                htmllocal=htmlforcpcc(myid,theid,0)
                html=html+htmllocal
                lesfils=Structure.objects.all().filter(parentid=myid).filter(type=" cf").order_by('name')
                for fils in lesfils:
                    filsdesc1  = unicode(fils.name)+'+'+fils.type if fils.name else "nom_vide"
                    filsmyid = fils.myid
                    filstheid = str(fils.id)
                    filslabel = unicode(fils.label)
 
                    html.append('<tr onmouseover="cfover(this)" onmouseout="cfout(this)" class="thcp">')
                    html.append('<td class="tx"> <span class="traits"> &nbsp;&#9500;</span>')

                    if filsmyid in isexpanded: 
                        html.append('<input disabled type="hidden" name="clicked'+str(filsmyid)+'-2" value='+str(fils.myid)+str(-2)+'>')
                        html.append('<input type="image" id=\''+str(filsmyid)+'-2\' onclick=clickminus(this.id) ')
                        html.append(' src="'+moinspng+'" alt="save" value="save" class="pm" /></a>  ')
                    else:
                        html.append('<input disabled type="hidden" name="clicked'+str(filsmyid)+'-2" value='+str(filsmyid)+str(-2)+'>')
                        html.append('<input type="image" id=\''+str(filsmyid)+'-2\' onclick=clickminus(this.id) ')
                        html.append(' src="'+pluspng+'" alt="save" value="save" class="pm" /></a>  ')

                    html.append('<!-- position:relative -->')
                    html.append('<a style=\'padding-top:120px;\' name="806">')
                    html.append('<a class="cf info" href="">'+filsdesc1+ '<span>' + filslabel+'</span></a></td>')
                    html.append('     <td class="bl">&nbsp;</td>         ')
                    html.append('<td>'+"" +'</td>')
                    html.append('<td></td>')
                    html.append('     <td class="bl">&nbsp;</td>         ')
                    html.append('<td>' + "" +'</td>')
                    html.append('<td></td>')
                    html.append('     <td class="bl">&nbsp;</td>         ')
                    html.append('<td>' + "" + '</td>')
                    html.append('<td>' + "" + '</td>')
                    html.append('     <td class="bl">&nbsp;</td>         ')
                    html.append('<td>' + "" + '</td>')
                    html.append('<td></td>')
                    html.append('     <td class="bl">&nbsp;</td>         ')
                    html.append('<td></td>')
                    html.append('<td></td>')
                    html.append('<td></td>')
                    html.append('</tr> \n')

                    prevdesc2=filsmyid

                    if filsmyid in isexpanded : #step3   reste a gerer les CF 
                        htmllocal=htmlforcpcc(filsmyid,filstheid,0)
                        html=html+htmllocal
                        lespttsfils=Structure.objects.all().filter(parentid=filsmyid).filter(type=" cf").order_by('name')   # traiter les cf et les cc differemment
                        for pttfils in lespttsfils:
                            pttfilsdesc1  = unicode(pttfils.name)+"++"+pttfils.type if pttfils.name else "nom_vide"
                            pttfilsmyid = str(pttfils.myid)
                            pttfilsid = str(pttfils.id)
                            pttfilslabel = unicode(pttfils.label)

                            # il y a 13 colonnes
                            html.append('<tr onmouseover="cfover(this)" onmouseout="cfout(this)" class="thcc">')
                            html.append('<td class="tx"> <span class="traits"> &nbsp;&#9474; &#9492; </span>')
                            if pttfilsmyid in isexpanded:
                                html.append('<input disabled type="hidden" name="clicked'+pttfilsmyid+str(-3)+'" value='+pttfilsmyid+str(-3)+'>')
                                html.append('<input type="image" id=\''+pttfilsmyid+str(-3)+'\' onclick=clickminus(this.id) ')
                                html.append(' src="'+moinspng+'" alt="save" value="save" class="pm" /></a>  ')
                            else:
                                html.append('<input disabled type="hidden" name="clicked'+pttfilsmyid+str(-3)+'" value='+pttfilsmyid+str(-3)+'>')
                                html.append('<input type="image" id=\''+pttfilsmyid+str(-3)+'\' onclick=clickminus(this.id) ')
                                html.append(' src="'+pluspng+'" alt="save" value="save" class="pm" /></a>  ')
                            html.append('<!-- position:relative -->')
                            html.append('<a style=\'padding-top:120px;\' name="40726">')
                            html.append('<a class="cp info" href="">'+pttfilsdesc1+ '<span>' + pttfilslabel+'</span></a></td>')
                            html.append('     <td class="bl">&nbsp;</td>         ')
                            html.append('<td>'+ "" +'</td>')
                            html.append('<td></td>')
                            html.append('     <td class="bl">&nbsp;</td>         ')
                            html.append('<td>' + "" +'</td>')
                            html.append('<td></td>')
                            html.append('     <td class="bl">&nbsp;</td>         ')
                            html.append('<td>' + "" + '</td>')
                            html.append('<td>' + "" + '</td>')
                            html.append('     <td class="bl">&nbsp;</td>         ')
                            html.append('<td>' + "" + '</td>')
                            html.append('<td></td>')
                            html.append('     <td class="bl">&nbsp;</td>         ')
                            html.append('<td></td>')
                            html.append('<td></td>')
                            html.append('<td></td>')
                            html.append('</tr> \n')


                            if pttfilsmyid in isexpanded:
                                htmllocal=htmlforcpcc(pttfilsmyid,pttfilsid,2)
                                html=html+htmllocal
                                lespttsfils2=Structure.objects.all().filter(parentid=pttfilsmyid).filter(type=' cf').order_by('name')
                                for pttfils2 in lespttsfils2:
                                    pttfils2desc1  = unicode(pttfils2.name)+'++'+pttfils2.type if pttfils2.name else "nom_vide"
                                    pttfils2myid = str(pttfils2.myid)
                                    pttfils2theid = str(pttfils2.id)
                                    pttfils2label= unicode(pttfils2.label)
                                    if pttfils2.type == ' cc':
                                        pass
                                    elif pttfils2.type == ' cp':
                                        pass #htmlforcpcc(pttfils2myid,pttfils2theid,1)
                                    elif pttfils2.type == ' cf':
#---------------------------------------------
                                        # il y a 13 colonnes
                                        html.append('<tr onmouseover="cfover(this)" onmouseout="cfout(this)" class="thcc">')
                                        html.append('<td class="tx"> <span class="traits"> &nbsp;&#9474; &nbsp;&nbsp;&nbsp; &#9492; </span>')
                                        if pttfils2myid in isexpanded:
                                            html.append('<input disabled type="hidden" name="clicked'+pttfils2myid+str(-6)+'" value='+pttfils2myid+str(-6)+'>')
                                            html.append('<input type="image" id=\''+pttfils2myid+str(-6)+'\' onclick=clickminus(this.id) ')
                                            html.append(' src="'+moinspng+'" alt="save" value="save" class="pm" /></a>  ')
                                        else:
                                            html.append('<input disabled type="hidden" name="clicked'+pttfils2myid+str(-6)+'" value='+pttfils2myid+str(-6)+'>')
                                            html.append('<input type="image" id=\''+pttfils2myid+str(-6)+'\' onclick=clickminus(this.id) ')
                                            html.append(' src="'+pluspng+'" alt="save" value="save" class="pm" /></a>  ')
                                        html.append('<!-- position:relative -->')
                                        html.append('<a style=\'padding-top:120px;\' name="40726">')
                                        html.append('<a class="cp info" href="">'+pttfils2desc1+ '<span>' + pttfils2label+'</span></a></td>')
                                        html.append('     <td class="bl">&nbsp;</td>         ')
                                        html.append('<td>'+ "" +'</td>')
                                        html.append('<td></td>')
                                        html.append('     <td class="bl">&nbsp;</td>         ')
                                        html.append('<td>' + "" +'</td>')
                                        html.append('<td></td>')
                                        html.append('     <td class="bl">&nbsp;</td>         ')
                                        html.append('<td>' + "" + '</td>')
                                        html.append('<td>' + "" + '</td>')
                                        html.append('     <td class="bl">&nbsp;</td>         ')
                                        html.append('<td>' + "" + '</td>')
                                        html.append('<td></td>')
                                        html.append('     <td class="bl">&nbsp;</td>         ')
                                        html.append('<td></td>')
                                        html.append('<td></td>')
                                        html.append('<td></td>')
                                        html.append('</tr> \n')

                                        if pttfils2myid in isexpanded:
                                            htmllocal=htmlforcpcc(pttfils2myid,pttfils2theid,3)
                                            html=html+htmllocal
                                            #lespttsfils3=Structure.objects.all().filter(parentid=pttfils2myid).filter(type=' cp').order_by('name')
                                            #print("nb pttspttsfils:"+str(lespttsfils3.count())+"pour myid"+str(pttfils2myid))
                                            #for pttfils3 in lespttsfils3:
                                            #    pttfils3myid = str(pttfils3.myid)
                                            #    pttfils3theid = str(pttfils3.id)
                                            #    htmlforcpcc(pttfils3myid,pttfils3theid,2)
#-------------------------------------------------------------------------------



                                    else:
                                        print ('ERROR')

        html.append("\n")
        
    #html.append('</ol>')
 
    htmlfooter=rapporthtmlfooter()
    html2 = htmlheader + html3 + html + htmlfooter

    html2.append('Version de d&eacuteveloppement Jos&eacute Dos Santos')


    return HttpResponse(html2)







