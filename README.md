# TN512-CC: Command and Control
Make an environment for each part using the requirement.txt files


# Run DB server
## Configure to own machine
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

## Launching the parts
Open an Anaconda prompt in this location: `..\TN512-CC\DB_Api\C2V2`. 

Now run the server with the following command: `python manage.py runserver 8080`

This runs the database on the localmachine on port 8080.

# Run flight_api.py
Open an Anaconda prompt with the environment corresponding to the flight api. Be in this location: `..\TN512-CC\DB_Api\`

Run the following command: `python flight_api.py`

# Run Website
Open a new Anaconda prompt and activate the environment for the website. Go to this location: `..\TN512-CC\Website_server\src\manage.py`.

Run the following command to run the website: `python manage.py runserver`

# DISCLAIMER
It might be possible that you will have problems running the database server. This might be due to the fact that mysql is not installed on your machine. 

Download is from this site: https://www.mysql.com/fr/downloads/
