# Utilise une image Python officielle comme image de base
FROM python:3.11

# Définit le répertoire de travail à /app à l'intérieur du conteneur
WORKDIR /app

# Copie le fichier requirements.txt dans le conteneur
COPY requirements_Ships.txt /app/

# Installe les dépendances dans le conteneur
RUN pip install --no-cache-dir -r requirements_Ships.txt

# Copie tout le dossier du projet (y compris les scripts Python et le dossier opensky-api)
COPY . /app/

# Reviens au répertoire racine du projet
WORKDIR /app

# Lancer le script Python ou le serveur

RUN curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /usr/local/bin/wait-for-it && chmod +x /usr/local/bin/wait-for-it

CMD ["sh", "-c", "echo 'Waiting for django C2V2 api' && wait-for-it django:${DJANGO_PORT} -- python ship_api.py"]
#CMD ["python", "ship_api.py"]
