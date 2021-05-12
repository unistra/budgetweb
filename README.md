BudgetWeb
========================

![myimage-alt-tag](https://secure.travis-ci.org/unistra/budgetweb.png?branch=master&maxAge=0)
[![Coverage Status](https://coveralls.io/repos/github/unistra/budgetweb/badge.svg?branch=master&maxAge=0)](https://coveralls.io/github/unistra/budgetweb?branch=master)
[![AUR](https://img.shields.io/aur/license/yaourt.svg?maxAge=2592000?style=flat-square)]()
[![Code Climate](https://codeclimate.com/github/unistra/budgetweb/badges/gpa.svg)](https://codeclimate.com/github/unistra/budgetweb)

Résumé
===================

L'application BudgetWeb permet la pré-saisie d'un budget d'une Université en mode décentralisé. Toutes ces pré-saisies sont ensuite consolidées, corrigées et validées par service central pour ensuite être intégré dans le système financier. De nombreuses règles de gestions sont définies et personnalisables. Les accès se font via les profils suivants :
  * un profil "utilisateur" qui permet la connexion et la saisie de prévisions de recettes et de dépenses sur lesquels il dispose d'habilitation. Il existe plusieurs type de programmes de financement (fléché / ou NA / non fléché et pluri-annuel / non pluri-annuel). Pour une PFI pluriannuel la saisie peut se faire sur plusieurs années. Quelques règles de gestion sont en place permettant de cadrer la saisie.
  * un profil "budget" qui permet le suivi les différents saisies, et qui passe outre les règles de gestion.

  L'exploitation des données se fait via un univers Business Objects .
  L'outil permet, via un univers BO, de déverser dans le SI finance les fichiers suivants :
  * Le budget d'engagement et de paiement
  * Le BOPA (Budget pluriannuel)
  * Des pré-budgets analytiques. 

L'application BudgetWeb est basée sur Django, jQuery et BootStrap. La version est maintenant configuré pour fonctionner avec PostGreSQL.


Prérequis
===================
```
  apt-get install virtualenv
  apt-get install virtualenvwrapper
  apt-get install postgresql-9.5
  sudo su postgres
  psql -c "CREATE DATABASE budgetweb;"
  psql -c "CREATE USER budgetweb WITH PASSWORD 'budgetweb';"
  
``` 
  * virtualenvwrapper_ et le ``.bashrc`` complété avec les lignes suivantes :

```
	export WORKON_HOME=~/.virtualenvs/
	export PIP_VIRTUALENV_BASE=$WORKON_HOME
	export PIP_RESPECT_VIRTUALENV=true
	source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
``` 	
  * python3.5-dev (comptatible python 3.4)
  
On revient dans le home dir (exemple /home/lhutin)
``` 
  git clone https://github.com/unistra/budgetweb.git
```   
On créé le virtualenv pour BudgetWeb.
``` 
  mkvirtualenv -p /usr/bin/python3.5 -a /home/lhutin/budgetweb budgetweb
```   
Vous lancerez et désactiverez l'env. avec les commandes suivantes::
```
  workon budgetweb
  deactivate
```   
  
Installation des prerequis du projets
-------------------------------------

* Pour installer Django dans l'environnement virtuel:
```
    pip install -r requirements/dev.txt
```
* On configure l'environnement et on ajoute 
``` 
    nano .virtualenvs/budgetweb/bin/postactivate
    export DJANGO_SETTINGS_MODULE=budgetweb.settings.dev
    
    DEFAULT_DB_USER=budgetweb
    DEFAULT_DB_PASSWORD=budgetweb
    DEFAULT_DB_NAME=budgetweb
    workon budgetweb
    cdproject # Si la commande est installé pour se trouver dans le bon répertoire.

    # Vous devrez ensuite adapter les variables liées à l'authentification centralisé.
    vi budgetweb/budgetweb/settings/base.py 
    CAS_SERVER_URL = XXXXXXXXXXXXXXXX
    CAS_LOGOUT_REQUEST_ALLOWED = ('XXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX')
    
    # Si on ne veut pas utiliser l'authentification CAS, on peut ajouter ce paramètre. Cela permet d'avoir une authentification local.
    # CAS_ADMIN_AUTH = False
    
    # Configuration du modèle.
    python manage.py migrate
    
    # On créé notre "superuser" qui disposera des droits administrateurs. (même login que votre login CAS !)
    python manage.py createsuperuser
    
    # Permet d'importer un jeu de test.
    python manage.py initial_import
    
    # Génération des fichiers de traductions.
    python manage.py compilemessages
    
    # Permet de générer des écritures en dépense et en recette de manière aléatoire.
    python manage.py create_structuremontants
    
    # On démarre le serveur.
    python manage.py runserver
    
    # On lance son navigateur favori via l'adresse suivante :
    http://localhost:8000
``` 

Documentation technique
-----------------------

Initialisation des données.
---------------------------

Nous avons préparé plusieurs scripts d'import vous permettant d'insérer en masse vos données

Le premier fichier à importer est les Structures (CFs)
Le format est le suivant :
Groupe1;Groupe2;Perimetre;CFParent;CF;Label
Groupe1 et Groupe2 correspondent à des groupes personnalisés qui ne servent pas dans BudgetWeb mais qui permettent de faire des tris lors de la génération des annexes via BO. Vous pouvez laisser ces champs vides.
Perimetre est le périmètre financier associé. Pour l'instant ce champs n'est d'aucune utilité. (Chez nous c'est 1010)
CFParent est le nom du CF parent. Les CFs de niveau "0" sont crée directement dans la commande import_structure. Il conviendra d'adapter ce script en fonction du nombre de vos sociétés.
CF est le code du CF (APS, ART, DPI, etc.)
Label est le libellé associé au CFs.

L'import des structures se fait via la commande suivante :
``` 
    python manage.py import_structures path/to/data.csv
```

Le deuxième fichier à importer est les Plan de Financements (PFi)
Le format est le suivant :
 * Structure;Code;Label;fleche;pluri;eotp;cc;cp;groupe1;groupe2
 * **Structure** est le code du CF auquel est rattaché le PFI (Ex APS)
 * **Code** est le code du PFi (Exemple : A13R316B). Le code n'a pas besoin d'être unique.
 * **Label** est le libellé du PFi (Exemple : Mon super PFI)
 * **fleche** défini si le PFi est fléché où non. Un PFi fléché dispose de nature comptable différentes d'un PFi non fléché
 * **pluri** défini si le PFi est pluriannuel où pas. Les écrans de saisie ne sont pas les mêmes.
 * **eotp** correspond  à l'eotp associé. Ce champs n'est pas obligatorie pour BudgetWeb.
 * **cc** correspond au centre de cout du PFi
 * **cp** correspond au centre de profil du PFi
 * **groupe1** et **groupe2** correspondent à des groupes personnalisés (comme pour les structures)

L'import des plan de financement se fait via la commande suivante :
``` 
    python manage.py import_pfi path/to/data.csv
```

Le troisième fichier à importer est les Domaines Fonctionnels
Le format est le suivant :
code;libelle_long;libelle_cours
 * **code** correspond au code du domaine fonctionnel (identique à SAP)
 * **libelle_long** correspond au libellé long du domaine fonctionnel. (Pas utile pour BudgetWeb)
 * **libelle_cours** correspond au libellé cours du domaine fonctionnel. C'est ce libellé qui apparait dans les menus déroulant.
Exemple : D101;Formation initiale et continue de niveau Licence;Formation de niveau Licence
``` 
    python manage.py import_functionaldomains path/to/data.csv
```

Le quatrième fichier à importer est les Natures Comptables Depenses.
Le format est le suivant :

 * pfi_fleche correspond à un boolean qui défini si la nature comptable est de type fléché où non. ('Valeur possible : 'PFI Fléché' où tout autre valeur)
 * enveloppe correspond à une liste à choix ('Fonctionnement', 'Personnel', 'Investissement')
 * libelle_nature_comptable correspond au libellé de la nature comptable.
 * code_nature_comptable correspond au code du compte budgetaire
 * code_compte_budgetaire correspond au code du compte budgetaire
 * libelle_compte_budgetaire correspond au libellé du compte budgétaire
 * regle_decallage_treso correspond à une des règle de gestion pour la nature comptable. (Voir plus loin pour les règles)
 * regle_budgetaire correspond à une des règle de gestion pour la nature comptable. (Voir plus loin pour les règles)
 * regle_pi_cfg correspond à une des règles de gestion pour la nature comptable. (Voir plus loin pour les règles)
 * ordre est un chiffre qui permet le classement des natures comptables par enveloppe.
 
Exemple : PFI fléché;Fonctionnement;Fluides;9DFLU;FF;Fonctionnement Fléché;non;non;non;1
``` 
    python manage.py import_naturecomptabledepense path/to/data.csv
```

Le cinquième fichier à importer est les Natures Comptables Recettes.
Le format est le suivant :

 * pfi_fleche correspond à un boolean qui défini si la nature comptable est de type fléché où non. ('Valeur possible : 'PFI Fléché' où tout autre valeur)
 * code_fond correspond au code du fond
 * libelle_fond correspond au libellé du fond
 * code_nature_comptable correspond au code du compte budgetaire
 * libelle_nature_comptable correspond au libellé de la nature comptable.
 * code_compte_budgetaire correspond au code du compte budgetaire
 * libelle_compte_budgetaire correspond au libellé du compte budgétaire
 * regle_is_ar_re correspond à une des règles de gestion pour la nature comptable. (Voir plus loin pour les règles)
 * regle_is_non_budgetaire correspond à une des règles de gestion pour la nature comptable. (Voir plus loin pour les règles)
  * ordre est un chiffre qui permet le classement des natures comptables par enveloppe.
Exemple : PFI non fléché ou NA;Investissement;NB-Restitution de dépôts ou cautionnements reçus d'un tiers;9DIDE;NEANT;Néant;non;oui;non;74

``` 
    python manage.py import_naturecomptablerecette path/to/data.csv
```

  Depuis la version 2 de BudgetWeb nous avons redécoupé l'application. Nous avons déplacé les données "Structures" dans une application Django à part (Pour pouvoir les réutiliser dans d'autres applications) et les données propre à BudgetWeb dans une autre application Django.

 * La table "Structure" contient la structure financière de l'établissement.
 * La table "StructureAuthorizations" contient les autorisatons des utilisateurs aux structures.
 * La table "StructureMontant" contient les montants cumulés des sous-structures / programme de financement.
 * La table "PeriodeBudget" contient les différentes périodes budgétaires (BI, Virement, BR1, BR2, etc.)
 * La table "DomaineFonctionnel" contient la liste des domaines fonctionnels.
 * La table "PlanFinancement" contient la liste des programmes de financements.
 * La table "NatureComptableDepense" contient la liste des natures comptables dépenses.
 * La table "NatureComptableRecette" contient la liste des natures comptables recettes
 * La table "Depense" qui contient la liste des saisies en dépense.
 * La table "Recette" qui contient la liste des saisies en recette.
 * FIX IT

**Quelques règles de gestion ont été implémentées :**
  * Pour la partie Dépense (1 seul règle possible par nature comptable !):
   * La règle "Décallage trésorerie" définie la règle suivant : Le montant CP et DC doivent obligatoirement être identique.
   * La règle "Non Budgétaire" définie la règle suivant : Le montant AE et CP ne peuvent pas être égal à 0.
   * La règle "PI-CFG" s'applique alors AE = DC et CP = 0
   * Si la nature comptable n'a pas pas de règle alors AE = CP = DC.
  * Pour la partie Recette (1 seul règle possible par nature comptable !):
   * La règle IS_AR_RE ne permet pas de saisir de valeur diffénrents entre AR et RE.
   * La règle IS_NON_BUDGETAIRE définie cette rège : Si "is_non_budgetaire" = oui alors AR = RE = 0 et DC à saisir
  * Enfin si l'utilisateur appartient au groupe "DFI", les règles par défaut s'applique mais il est possible de passer outre en saisissant d'autres valeurs.
  * Les règles s'applique pour les gestionnaires en composantes.
  
 **La gestion des périodes budgétaires**
 Maintenant l'application gère la période budgétaire BI (Budgt initial), la période VIREMENT, la période BR (Budget rectificatif).
 Chaque période est activable via des dates de début et de fin. Les gestionnaires en composantes dispose d'une période de saisie.
 
 **La gestion des virements**
 La gestion des virements se fait par l'import depuis ERP SAP. Pour ce faire, nous avons développé un Web service dédié qui sera prochainement publié (où pas) sur GitHub. L'application BudgetWeb appele le WebService qui lui appele la BAPI qui va bien.
 
A chaque ouverture d'un nouveau BI, un script d'initialisation s'execute pour "migrer" les données saisies dans les PFI "pluriannuel".

Documentation utilisateur
-------------------------

   Vous trouverez ici un pas à pas très détaillé expliquant le fonctionnement de BudgetWeb.
   ![Pas à pas détaillé](docs/Documentation.pdf?raw=true "Documentation BudgetWeb")

La gestion des droits permets de donner des accès à des niveaux très fins (structure de niveau 3 où plus selon la structure financière intégrée.

Un champ "is_active" est disponible pour les structures et les pfi, cela permet d'afficher / masquer les données voulues.

Le jeu de test contient :
    Des programmes de financements fléchés / non fléchés. ( La naturecomptable est différente entre un PFI fléché et non fléché)
    Des programmes de financements pluri-annuel et non pluri-annuel. (Les écrans de saisies ne sont pas identiques).

* Présentation de l'arborescence au budget initial.
![Alt text](docs/images/capture1.jpg?raw=true "Title")
* Présentation de l'arborescence au Budget Rectificatif
![Alt text](docs/images/capture8.jpg?raw=true "Title")
* Formulaire de saisie des dépenses.
![Alt text](docs/images/capture2.jpg?raw=true "Title")
* Formulaire de saisie des recettes
![Alt text](docs/images/capture3.jpg?raw=true "Title")
* Résumé disponible pour chaque niveau.
![Alt text](docs/images/capture4.jpg?raw=true "Title")
![Alt text](docs/images/capture9.jpg?raw=true "Title")
* Gestion des PFI pluri-annuel
![Alt text](docs/images/capture5.jpg?raw=true "Title")
![Alt text](docs/images/capture6.jpg?raw=true "Title")
*Exploitation des données via un univers BO dédié.
![Alt text](docs/images/capture7.jpg?raw=true "Title")

Contact
========================

Une seule adresse : ludovic.hutin@unistra.fr
