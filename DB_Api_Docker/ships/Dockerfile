# Utilise une image Python officielle comme image de base
FROM python:3.7

# Définit le répertoire de travail à /app à l'intérieur du conteneur
WORKDIR /app

# Copie le fichier requirements.txt dans le conteneur
COPY requirements_Ships.txt /app/

# Installe les dépendances dans le conteneur
RUN pip install --no-cache-dir -r requirements_Ships.txt

# Copie tout le dossier du projet (y compris les scripts Python et le dossier opensky-api)
COPY . /app/

# Change de répertoire vers le répertoire contenant le package (opensky-api/python)
WORKDIR /app/opensky-api/python

# Installe le package OpenSky API en mode éditable
RUN pip install -e .

# Reviens au répertoire racine du projet
WORKDIR /app

# Lancer le script Python ou le serveur
CMD ["python", "ship_api.py"]
