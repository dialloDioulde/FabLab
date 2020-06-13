       
 # Projet TER
Bonjour,

Voici notre projet compte rendu TER.

Vous pouvez trouver notre code source sur Github 
https://github.com/dialloDioulde/FabLab

#### Group
DIALLO Mamadou
MIHALI Kristi


#### Remarque

Ce projet a été développé sous la supervision de M. Lemasson.

#### Requirements

Django==3.0.5

django-tinymce4-lite==1.7.5

selenium==3.14.0


#### Installation

1) Obtenez une copie du projet.

       git clone new_project.git
        
2) Créer un environnement virtuel et installer des dépendances.

        mkvirtualenv new_project
    ou
        ```virtualenv new_project (in mac)```
        
    Après: 
    
      ```pip3 install -r requirements.txt```
    
3) Initialisez votre base de données.

        python3 ./manage.py migrate
        
   Si votre application a un modèle d'utilisateur personnalisé, vous devrez créer un nouveau super-utilisateur pour l'administrateur.

        python3 ./manage.py createsuperuser
       
4) Lancez le serveur de développement pour vérifier que tout fonctionne.

        python3 ./manage.py runserver

#### Tâche réalisé
* [x] 1 - **Pages** Accueil / Profil de l'utilisateur / un matériel
* [x] 2 - **Formulaire** de Type / de Matériel / d'Emprunteur / d'Emprunt
* [x] 3 - **CRUD** Type / Matériel / Emprunteur / Emprunt
* [x] 4 - Fichiers **média** pour les matériels
* [x] 5 - **django.contrib.auth*** && Niveaux d'utilisateurs (**Utilisanteur / Administrateur**)
* [x] 6 - Intégration graphique responsive en utilisant **Fontawesome** 
* [x] 7 - Utilisation du framework Django **Ajax/JQuery**
* [x] 8 - Réinitialisation du mot de passe (Password Reset View)
* [x] 9 - Tests unitaires (Commande: ```$coverage run --source='.' manage.py test``` pour voir le réslutat)

#### Tâche non réalisé
* [ ] 1 - Avoir le form du Matériel et Type sur le même page. 

#### Démonstration

###### Page d'accueil 

<img src="https://i.imgur.com/fN443XB.png" title="source: imgur.com" />

###### Page d'un matériel 
<img src="https://i.imgur.com/DUbVC5k.png" title="source: imgur.com" />

###### Page création d'un emprunt 
<img src="https://i.imgur.com/fBU29zr.png" title="source: imgur.com" />
<img src="https://i.imgur.com/6WpqYlO.png" title="source: imgur.com" />

###### Page profil de l'utilisateur 
<img src="https://i.imgur.com/JIXZYzo.png" title="source: imgur.com" />

###### Page register staff
<img src="https://i.imgur.com/6D04b3m.png" title="source: imgur.com" />

###### Page login 

<img src="https://i.imgur.com/OvEVHGt.png" title="source: imgur.com" />

###### Page dashboard 

<img src="https://i.imgur.com/wu75801.png" title="source: imgur.com" />

###### Page Emprunt

<a href="https://imgur.com/VWfG4NO"><img src="https://i.imgur.com/VWfG4NO.png" title="source: imgur.com" /></a>
<img src="https://i.imgur.com/p03OkJa" title="source: imgur.com" />

###### Page Type
<a href="https://imgur.com/nh7MXfQ"><img src="https://i.imgur.com/nh7MXfQ.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/jMRkDjt"><img src="https://i.imgur.com/jMRkDjt.png" title="source: imgur.com" /></a>

###### Page Emprunteur
<a href="https://imgur.com/wNppPaV"><img src="https://i.imgur.com/wNppPaV.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/YfZCXes"><img src="https://i.imgur.com/YfZCXes.png" title="source: imgur.com" /></a>

###### Page Matériel

<a href="https://imgur.com/nShpCF8"><img src="https://i.imgur.com/nShpCF8.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/7iAarAe"><img src="https://i.imgur.com/7iAarAe.png" title="source: imgur.com" /></a>
