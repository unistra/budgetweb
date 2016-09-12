BudgetWeb
========================

L'application BudgetWeb est basée sur Django.


Prérequis
===================
```
  apt-get install virtualenv
  apt-get install virtualenvwrapper
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
    
    workon budgetweb
    cdproject # Si la commande est installé pour se trouver dans le bon répertoire.

    # Vous devrez ensuite adapter les variables liées à l'authentification centralisé.
    vi budgetweb/budgetweb/settings/base.py 
    CAS_SERVER_URL = XXXXXXXXXXXXXXXX
    CAS_LOGOUT_REQUEST_ALLOWED = ('XXXXXXXXXXXXX', 'XXXXXXXXXXXXXXX')
    
    # Configuration du modèle.
    python manage.py migrate
    
    # On créé notre "superuser" qui disposera des droits administrateurs. (même login que votre login CAS !)
    python manage.py createsuperuser
    
    # Permet d'importer un jeu de test.
    python manage.py initial_import
    
    # Permet de générer des écritures en dépense et en recette de manière aléatoire.
    python manage.py create_structuremontants
    
    # On démarre le serveur.
    python manage.py runserver
    
    # On lance son navigateur favori via l'adresse suivante :
    http://localhost:8000
``` 

Documentation technique
-----------------------

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

Quelques règles de gestion ont été implémentées :
  * Si l'utilisateur appartient au groupe "DFI"
        Alors le champ "DC" en recette et en dépense est ouvert à la saisie
        Sinon le champ "DC" est bloqué et est égal au champ "CP" en dépense et au champ "RE" en recette.
  * Si la nature comptable dépense autorise le décalage de trésorerie
        Alors le champ CP n'est pas bloqué et la saisie est libre.
        Sinon le champ CP est égal au champ AE.
  * FIX IT.

Documentation utilisateur
-------------------------

La gestion des droits permets de donner des accès à des niveaux très fins (structure de niveau 3 où plus selon la structure financière intégrée.

Un champ "is_active" est disponible pour les strcutres et les pfi, cela permet d'afficher / masquer les données voulues.

Le jeu de test contient :
    Des programmes de financements fléchés / non fléchés. ( La naturecomptable est différente entre un PFI fléché et non fléché)
    Des programmes de financements pluri-annuel et non pluri-annuel. (Les écrans de saisies ne sont pas identiques).

* Présentation de l'arborescence.
![Alt text](docs/images/capture1.jpg?raw=true "Title")
* Formulaire de saisie des dépenses.
![Alt text](docs/images/capture2.jpg?raw=true "Title")
* Formulaire de saisie des recettes
![Alt text](docs/images/capture3.jpg?raw=true "Title")
* Résumé disponible pour chaque niveau.
![Alt text](docs/images/capture4.jpg?raw=true "Title")
* Gestion des PFI pluri-annuel
![Alt text](docs/images/capture5.jpg?raw=true "Title")
![Alt text](docs/images/capture6.jpg?raw=true "Title")
*Exploitation des données via un univers BO dédié.
![Alt text](docs/images/capture7.jpg?raw=true "Title")

Contact
========================

Une seule adresse : ludovic.hutin@unistra.fr
