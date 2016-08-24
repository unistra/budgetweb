========================
BudgetWeb
========================

L'application BudgetWeb est basée sur Django.


Prérequis
===================

  apt-get install virtualenv
  apt-get install virtualenvwrapper
  
  * virtualenvwrapper_ et le ``.bashrc`` complété avec les lignes suivantes ::

	# VIRTUALENV PYTHON
	export WORKON_HOME=~/.virtualenvs/
	export PIP_VIRTUALENV_BASE=$WORKON_HOME
	export PIP_RESPECT_VIRTUALENV=true
	source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
	
  * python3.5-dev
  
On revient dans le home dir (exemple /home/lhutin)

  git clone https://git.unistra.fr/di/budgetweb.git
  
On créé le virtualenv pour BudgetWeb.

  * mkvirtualenv -p /usr/bin/python3.5 -a /home/lhutin/budgetweb budgetweb
  
Vous lancerez et désactiverez l'env. avec les commandes suivantes::

  * workon budgetweb
  * deactivate
  
  
Installation des prerequis du projets
-------------------------------------

* Pour installer Django dans l'environnement virtuel::

    pip install -r requirements/dev.txt
    
* On configure l'environnement et on ajoute 

    export DJANGO_SETTINGS_MODULE=budgetweb.settings.dev
    
    workon budgetweb
    cdproject # Si la commande est installé pour se trouver dans le bon répertoire.
    
    # Configuration du modèle.
    python manage.py migrate
    
    # Permet de générer un jeu de test
    python manage.py initial_import
    
    # Permet de générer des écritures aléatoires.
    python manage.py create_structuremontants