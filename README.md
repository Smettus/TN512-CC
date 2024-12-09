# TN512-CC: Command and Control
Make an environment for each part using the requirement.txt files.


## Backend
### Database
#### Clearing the database
First you must make sure that the database is correctly configurated. First check if `DB_Api\C2V2\tutorials\migrations` only contains the `__init__.py` file (and also your own `pycache`). If this is not the case, DELETE all migrations files but not `__init__.py`!

Next go to open the `mysql command line client`. Here you use the following commands:

* To start the mysql server: `source "[location to]\DB_Api\C2V2\C2V2\db.sql"`
* Check if it is correctly loaded: `show databases;` here you must see c2
* check if your database is empty:
  * `use c2;`
  * `show tables;` If this command does not show the tables like: Plane, Entities, etc. You're good and you can go to next section
* IF YOUR DATABASES DOES CONTAINS THE TABLES planes entitites, etc. you must clear everything:
  * `SET FOREIGN_KEY_CHECKS = 0;`
  * `DROP DATABASE c2;`
  * `CREATE DATABASE c2;`
  * `SET FOREIGN_KEY_CHECKS = 1;`
  * THIS CAN ALSO BE DONE JUST TO MAKE SURE THAT YOUR DATABASE IS TOTALY EMPTY

#### Configure to own machine
Configure the database with your own useraccount. Make sure that mysql is installed.

- In `DB_Api\C2V2\manage.py`:
```py
    def run_sql_file():
    db_user = 'USERNAME'
    db_password = 'PASSWORD'
    db_host = '127.0.0.1'  # or your MySQL server address
    sql_file_path = './C2V2/db.sql'
    # Connect to MySQL without specifying a database
    connection = pymysql.connect(
        user=db_user,
        password=db_password,
        host=db_host
    )
    cursor = connection.cursor()
```
- In `DB_Api\C2V2\C2V2\settings.py`
```py
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'C2',
            'USER': 'USERNAME',
            'PASSWORD': 'PASSWORD',
            'HOST': '127.0.0.1',
            'PORT': '8080',
        }
    }
```

#### Creating the database
Now that you configured your code to your own machine and that you cleared and started the database server we can generate the tables that we need.

Go to the folder `[location to]\DB_Api\C2V2>` in your python environment and run the following commands. **MAKE SURE THAT YOU DID EVERYTHING FROM THE CLEARING PART ELSE IT IS NOT GOING TO WORK**

* `python manage.py makemigrations`
* `python manage.py migrate`

Now you can go back to `mysql` and check if your tables are generated using the following codes:



* To see if all the tables are added: `show tables;`, you must get the following result:
* 
![image](https://github.com/user-attachments/assets/659fe2fb-2435-4574-9831-3a4bc1d28e99)

* To see if the plane table is correctly configured: `describe plane;`, you should get this:
  
![image](https://github.com/user-attachments/assets/61fa5d99-4dde-4204-a2ef-9180b856cfd1)

**YOU MUST HAVE ALL THE ROWS LIKE HERE OR ELSE THEIR WILL BE ERRORS**

* If you want to see all the entries from a table: `select * from <table_name>`, e.g. `select * from entities`



#### Launching the parts
Open an Anaconda prompt in this location: `..\TN512-CC\DB_Api\C2V2`. 

Now run the server with the following command: `python manage.py runserver 8080`

This runs the database on the localmachine on port 8080.

### Gathering data
#### FlightAPI
Open an Anaconda prompt with the environment corresponding to the flight api. Be in this location: `..\TN512-CC\DB_Api\`

Run the following command: `python flight_api.py`

#### Naval

#### AI reports


### Host website - Django
Open a new Anaconda prompt and activate the environment for the website. Go to this location: `..\TN512-CC\Website_server\src\manage.py`.

Run the following command to run the website: `python manage.py runserver`

### DISCLAIMER
It might be possible that you will have problems running the database server. This might be due to the fact that mysql is not installed on your machine. 

Download is from this site: https://www.mysql.com/fr/downloads/

### User accounts
A basic Django login/logout system was introduced. The admin can manage the accounts from ‘http://127.0.0.1:8000/admin’. For now, the login
credentials are admin-admin. 

Under the Django app ‘accounts’, the routing system can be viewed. To view the html of the pages, see ‘my_project/templates/accounts’.

TODO:
- Make that admin can control who has access and who has not
- Manage what each user can see

## Frontend
### Visualisation
TODO:
- Nicer pages all round (login/logout, base page)
- map.html:
    - search box
    - body black -> such that whole thing is black if tiles are loading.
