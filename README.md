# Stoned API Back-end

## Initialisation du projet en local

Dabord vous avez besoin de cloner le repos git 

https://github.com/Yassine-BADJI/stoned-api.git

Installer python
_(sur windows bien penser à ajouter python dans le PATH et
à fermer et rouvrir votre shell pour interagir avec python nouvellement installé)_
 
https://www.python.org/downloads/

Installer pip :
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

Installer virutalenv via pip 
```bash
pip install virtualenv
```

Creer votre environement virtuel via pip
```bash
cd chemin_du_repo/stoned_api
virtualenv ../stoned-api_env
```

Démarer l'env virtuel
```bash
source ../stoned-api_env/Scripts/activate
```

Installer les requirements
```bash
cd chemin_du_repo/stoned_api
pip install -r requirement.txt
```

Lancer le calcul de la db
```bash
python manage.py db upgrade
```

Lancer l'API
```bash
python manage.py run
```

L'API est désormais accesible à cette adresse : http://127.0.0.1:5000/ 
