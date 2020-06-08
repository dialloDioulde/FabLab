       
 # Projet TER
Bonjour,

Voici notre projet compte rendu TER.

Vous pouvez trouver notre code source sur Github 
https://github.com/dialloDioulde/FabLab

#### Group
MAMADOU Diallo
MIHALI Kristi


#### Remarque


#### Requirements
Django==3.0.5
django-tinymce4-lite==1.7.5
selenium==3.14.0


#### Installation

1) Grab a copy of the project.

       ``` git clone new_project.git```
        
2) Create a virtual environment and install dependencies.

        ```mkvirtualenv new_project```
    or
        ```virtualenv new_project (in mac)```
        ```pip install -r requirements.txt```
        
3) Duplicate 
       ``` new_project/new_project/local_settings_example.py ```
    and save as 
        ```local_settings.py.```
4) Enter your database settings in 
        ```local_settings.py.```
    
5) Initialize your database.

       ``` python ./manage.py syncdb```
        ```python ./manage.py migrate```
        
   If your app has a custom user model, you'll need to create a new superuser for the admin.

       ``` python ./manage.py createsuperuser```
       
7) Run the development server to verify everything is working.

        ```python ./manage.py runserver```

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

###### Page d'accueil - https://projet-laravel.zhangzhao.fr
<img src="https://imgur.com/pKxAHI3.png"/>

###### Page d'un matériel 
<img src="https://imgur.com/EoJL5EL.png"/>
###### Page contact  - https://projet-laravel.zhangzhao.fr/contact
<img src="https://imgur.com/HSmELPj.png"/>

###### Page register  - https://projet-laravel.zhangzhao.fr/register
<img src="https://imgur.com/cKg4Wbc.png"/>

###### Page login (Utilisateur)  - https://projet-laravel.zhangzhao.fr/login
<img src="https://imgur.com/plviClK.png"/>

###### Page dashboard (Utilisateur)  - https://projet-laravel.zhangzhao.fr/profile
<img src="https://imgur.com/K3AniZt.png"/>

###### Page modification d'un article (Utilisateur)  - https://projet-laravel.zhangzhao.fr/article/edit/15
<img src="https://imgur.com/xoNiwib.png"/>

###### Page création d'un article (Utilisateur)  - https://projet-laravel.zhangzhao.fr/create
<img src="https://imgur.com/TCkVaTN.png"/>

###### Page d'administrator voyager (Administrator)  - https://projet-laravel.zhangzhao.fr/admin/posts
<img src="https://imgur.com/luTYbpl.png"/>
<img src="https://imgur.com/vERJFiZ.png"/>
<img src="https://imgur.com/67BqTXi.png"/>




    
    
