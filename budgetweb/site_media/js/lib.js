// JavaScript Document

var occupe = 0;


function makeRequest(url) {
//	alert("makeRequest");
	http_request = false;
	if (window.XMLHttpRequest) { // Mozilla, Safari,...
		http_request = new XMLHttpRequest();
		if (http_request.overrideMimeType) {
			http_request.overrideMimeType('text/xml');
		}
	} else if (window.ActiveXObject) { // IE
		try {
			http_request = new ActiveXObject("Msxml2.XMLHTTP");
		} catch (e) {
			try {
			http_request = new ActiveXObject("Microsoft.XMLHTTP");
			} catch (e) {}
		}
	}
	if (!http_request) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}
	http_request.onreadystatechange = writeContents;
	http_request.open('GET', url, true);
	http_request.send(null);
}

function writeContents() {
	if (http_request.readyState == 4) {
		if (http_request.status == 200) {
			
			var xmldoc = http_request.responseXML;

			var divs = xmldoc.getElementsByTagName('div');
			for (var i = 0; i < divs.length; i++) {
				var ndiv = divs[i].getElementsByTagName('ndiv').item(0).firstChild.data;
				var ref = divs[i].getElementsByTagName('ref').item(0).firstChild.data;
				var innerhtml = divs[i].getElementsByTagName('innerhtml').item(0).firstChild.data;
				
				if (document.getElementById("div"+ref+ndiv).innerHTML = innerhtml) occupe = 0;
				occupe = 0;
			}
			if (xmldoc.getElementsByTagName('alerte').item(0)) {
				var alerte = xmldoc.getElementsByTagName('alerte').item(0).firstChild.data;
				alert(alerte);	
			}



		} else {
			alert('Erreur interne !!');
		}
	}	
}

function chgdiv(ndiv,parent,ref,type) {
	if (occupe == 0) {
		occupe = 1;
		makeRequest("div.php?parent="+parent+"&ndiv="+ndiv+"&ref="+ref+"&type="+type);
	}
}


//http://anothergeekwebsite.com/fr/2007/03/trim-en-javascript
var regExpBeginning = /^\s+/;
var regExpEnd       = /\s+$/;
// Supprime les espaces inutiles en début et fin de la chaîne passée en paramètre.
function trim(aString) {
    return aString.replace(regExpBeginning, "").replace(regExpEnd, "");
}

function verifmontant() {
	var erreur = 0;
	var v = document.form1.montant.value.replace(/ /g,"");
	v = document.form1.montant.value.replace(/,/,".");
	var m = parseFloat(v);
	m = Math.round(m*100)/100;
	if (isNaN(m)) {
		erreur = 4;
	} else if ((m < 0) && (pb <= 1)) {
		if (document.form1.selectnomades1) {
			if (document.form1.selectnomades1.options.item(document.form1.selectnomades1.options.selectedIndex).innerHTML.substr(0,1) != '9') {
				erreur = 2;
			}
		} else {
			erreur = 2;
		}
	} else if (m == 0) {
		erreur = 6;
	} else if (m > 999999999) {
		erreur = 3;
	}
	
	var eotpnom = document.form1.eotpnom.value.replace(/ /g,"");
	eotpnom = eotpnom.toUpperCase();
	document.form1.eotpnom.value = eotpnom;
	if (eotpnom != '') {
		if (trim(document.form1.eotpdesign.value) == '') {
			erreur = 9;
		}
		if (eotpnom.length > 13) {
			erreur = 7;
		} else {
			var filter  = '/^[a-zA-Z0-9]{' + eotpnom.length + '}$/';
			if (!filter.test(eotpnom)) {
				erreur = 8;
			} else {
				document.form1.selecteotp0.value = document.form1.selecteotp0.options[1].value;
			}
		}
	}
	var e = document.form1.elements;
	for (i=0; i<e.length; i++) {
		if ((e[i].value == -1) && (e[i].name != 'montant')) {
			erreur = 1;
		}
	}
	if (occupe > 0) {
		erreur = 5;
	}
	if (erreur == 1) {
		alert ('Renseignez tous les champs !');
		return false;
	} else if (erreur == 5) {
		alert ('Contactez le responsable !');
		return false;
	} else if (erreur == 2) {
		alert ('Le montant est négatif !');
		return false;
	} else if (erreur == 3) {
		alert ('Montant maximum : 1 000 000 000,00 € !');
		return false;
	} else if (erreur == 4) {
		alert ('Mauvais montant !');
		return false;
	} else if (erreur == 6) {
		return confirm ('Le montant est nul : 0,00 €');
	} else if (erreur == 7) {
		alert ('Le nom de l’élément de PFI doit comporter au maximul 13 caracteres (si non vide) !');
		return false;
	} else if (erreur == 8) {
		alert ('Le nom de l’élément de PFI ne doit pas comporter de caractères spéciaux !\nCaractères acceptés: A à Z et 0 à 9');
		return false;
	} else if (erreur == 9) {
		alert ('Le description de l’élément de PFI est vide !');
		return false;
	} else {
		return true;
	}
}


function cfover(tr) {
	tr.className += ' cfover';
}
function cfout(tr) {
	tr.className = tr.className.replace( ' cfover', '' );
}
function cpover(tr) {
	tr.className += ' cpover';
}
function cpout(tr) {
	tr.className = tr.className.replace( ' cpover', '' );
}
function ccover(tr) {
	tr.className += ' ccover';
}
function ccout(tr) {
	tr.className = tr.className.replace( ' ccover', '' );
}

 
function opacity()
{
    opaciT = opaciT - transition;
    var speed = 10;
    var transition = 10;
    var timer= 0;
    var opaciT = 100; 
    var object = document.getElementById("cache").style;
    object.opacity = (opaciT / 100);
    object.MozOpacity = (opaciT / 100);
    object.KhtmlOpacity = (opaciT / 100);
    object.filter = "alpha(opacity=" + opaciT + ")"; 
 
	if (opaciT <= 0)
	{
		document.getElementById("preloader").style.visibility="hidden";
		clearInterval(timer);
	}
 
}