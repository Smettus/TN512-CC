#!/bin/bash

webserverport=8000
dbserverport=8080

# Starting web server & db
gnome-terminal -- bash -c "source ../venv-tn512/bin/activate; export webserverport=$webserverport; echo 'Starting Webserver on port $webserverport...'; python ./Website_server/src/manage.py runserver $webserverport; exec bash"
gnome-terminal -- bash -c "source ../venv-tn512/bin/activate; export dbserverport=$dbserverport; echo 'Starting DBserver on port $dbserverport...'; cd ./DB_Api/C2V2/; python manage.py runserver $dbserverport; exec bash"

# Flightapi
gnome-terminal -- bash -c "source ../venv-tn512/bin/activate; echo 'Starting the flightapi...'; cd ./DB_Api/; python flight_api.py; exec bash"


