# TN512-CC: Command and Control
## TO DO
- Make sure that only each dt an API-call is performed, such that the server is not overloaded.

## Scheme of the C&C app

## Backend - Client server
The backend server has been ported to the Django framework. As always, make sure to install the necessary dependencies in your python virtual environment:
$$$
ip install -r requirements.txt
$$$

Running the server is as easy as:
$$$
cd src/
python manage.py runserver
$$$

### Multithreading
Already handled by the Django framework. However useful

### User accounts
A basic Django login/logout system was introduced. The admin can manage the accounts from 'http://127.0.0.1:8000/admin'.

Under the Django app 'accounts', the routing system can be viewed. To view the html of the pages, see 'my_project/templates/accounts'.


## Frontend
### Visualization
TODO:
- Nicer pages all round (login/logout, base page)
- map.html: search box for location
    - make the body black, to have it black when no tiles are there.
    - make search bar cleaner (maybe a css option already, not leaflet.js)

### Speedups:
1. Upon load, the user needs to fetch the leaflet.js. This takes time. Can we store it in the user session locally?
$$$html
<!-- Leaflet JS -->
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
$$$
-> base to solution is in comment in the flight_map.html. No, localstorage probably too small. use service workers?


