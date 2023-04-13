## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`


### Déploiement
Le site de Orange County Lettings a été déployé sur Heroku. Pour 
déployer le site, nous avons mis en place un pipeline CI/CD avec 
CircleCI. Ainsi, nous avons récupéré le repository de GitHub depuis
CircleCI. Quand nous avons récupéré notre repository, un dossier .circleci
ainsi qu'un fichier config.yml a été automatiquement créée. Nous avons
ensuite récupéré le dossier .circleci et son fichier config.yml en local.
Ensuite, c'est dans ce fichier config.yml que nous avons écrit nos instructions
pour le déploiement du site sur Heroku.

Pour déployer le site sur Heroku, nous avons dans un premier temps
lancer les tests et le linting pour nous assurer que notre code 
fonctionne en local. Ensuite, nous avons conteneurisé notre site 
avec Docker et on a pushé notre conteneur sur DockerHub. Et enfin,
une fois que la conteneurisation a réussi, c'est la que nous avons
procédé au déploiement de notre application(conteneurisé) sur Heroku.
Et pour finir, nous utilisons Sentry pour automatiquement détecter 
des éventuelles bugs et erreurs dans le site.


Pour pouvoir effectuer le déploiement les packages suivants doivent
être installé:

- Django 4.1.7
- flake8 6.0.0
- pytest-django 4.5.2
- pytest 7.2.1
- gunicorn 20.1.0
- whitenoise 6.4.0
- sentry-sdk 1.19.1

Si vous souhaitez d'abord tester le site en local avant de procéder
au déploiement assurez-vous d'avoir crééé un environnment virtuel
avec la commande `python -m venv venv` et ensuite activez 
l'environnement virtuel avec la commande `source venv/bin/activate`.

Une fois que vous aurez la certitude que le site fonctionne correctement
en local, vous pourrez procéder à la conteneurisation. 

Toutes les étapes du déploiement s'effectueront via le fichier config.yml
du dossier .circleci. Le fichier config.yml se composera de 3 jobs:

- test_and_linting
- publishLatestToHub
- deploy

Dans le job test_and_linting, vous devrez éxécuter pytest et flake8
afin de vous assurer qu'il n'y a pas d'erreurs dans le code et que 
la PEP8 est respectée.

Dans publishLatestToHub, vous devrez créer un fichier Dockerfile dans 
la racine du projet. Ce Dockerfile devra se composer du dossier racine
de votre projet: `WORKDIR /<le_nom_de_votre_projet>`, le requirements.txt:
`COPY requirements.txt .`, l'installation de celui-ci: `RUN pip install -r requirements.txt` et
la récupération de tout les dossiers et fichiers du projet: `COPY . .`. Afin que le CSS
S'affiche correctement sur Docker, vous devrez également collecter 
les fichiers statiques en éxécutant la commande suivante: `CMD python manage.py collectstatic`.
Et enfin pour terminer, éxécutez l'application avec gunicorn: `CMD gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT`.
Toute les commandes que je viens d'énumérer devront figurer sur le 
Dockerfile.

Que ça soit dans circleci, dans Dockerfile ou dans le code source,
pensez également à créer des variables d'environnement pour 
protéger vos données sensibles(la secret key de Django par exemple).

Dans circleci, vous devrez construire votre image Docker, vous authentifier
sur DockerHub et pusher votre image dans DockerHub.

Et enfin, dans la dernière étape, le déploiement(deploy), authentifiez-vous
sur Heroku et pusher votre image Docker sur Heroku.

Notre Workflow est configuré de la façon suivante:
- Les tests et le linting s'effectuent sur toutes les branches.
- Si les tests et le linting sont réussis, la conteneurisation pourra se
faire mais elle ne se fera que sur la branche master.
- Si la conteneurisation est réussi, le déploiement sur Heroku 
pourra se faire. Le déploiement ne peut se faire que sur la branche 
master.

Dans ce projet, nous avons travaillez avec Heroku mais vous allez 
peut-être faire le choix de travailler avec un autre hébergeur.
