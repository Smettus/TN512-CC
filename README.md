<<<<<<< HEAD
# TN512-CC: Command and Control
## TO DO
- Make sure that only each dt an API-call is performed, such that the server is not overloaded.
=======
# DATABASE API
**!IMPORTANT!** 

**@Laquay I changed the database a bit regarding the columns for the plane table. Update your database if you are going to use your own.**

This is the main code for the database API, Laquay will adapt this to make it compatible with other devices and to make it communicate with the webserver. 

Different types of HTML queries can be made containing JSON objects.

For the moment I don't know how to make the API available for public IP's, #futurework#loveit

>>>>>>> origin/API_server

## GET request

### Main form
URL to send to if on local machine:`http://127.0.0.1:8080/api/tutorials`

Request JSON:
```
    {
        "Type": "Latest_all"
    }
```
`Type` contains the type of GET request is made.

`Latest_all` will return a list of JSON's of **ALL** the objects in belgium. Thus what mostly will be used in our case for the moment. 

***In the future I will add more functionalities for specific lookups and other future functions.***
## POST 
In this case `flight_api.py` will take the data from **Open Sky API** and send POST requests to the database to store them.
