# Backend Server

The backend server will handle the API calls requested by the web application. It uses a python websocket to establish the connection with the webapp. The server is currently running on `localhost:65432`. 

## Current State
- It is now possible to hover to a desired region on the webb application and to send `bbox` to the backend server in JSON format. 
- The server will conduct an API call of the desired bbox and return a list of planes in the JSON format mentioned in `Example JSON/`.

## Installation
### API_c2c.py
This file contains the `python` classes for each different API call type: Planes, Ground Troops and Ships. To use this class one should install **OpenSkyApi**. Follow the installation process from their github: [OpenSkyApi](https://github.com/openskynetwork/opensky-api).

### BackEnd_server.py
Next these Packages are needed for the server:
```python
import base64
import json
from datetime import datetime
import asyncio
import websockets
```
**Install them in the same environment as the OpenSkyApi.**

### map.js
Map.js will send a request to the backend server to get all the planes in the desired area. This area is the visible part of the map on the sceren!

It will send a JSON file as request witht he following format.
```JSON
{
    'command': String of the desired command: POST, GET, QUIT, INTERACTIVE ,
    'data': bbox of the area
}
```

Example: 
```json
{
    'command': 'GET', 
    'data': {'southwest': {'lat': 50.810382245925, 'lng': 4.283638000488282}, 'northwest': {'lat': 50.9137489045753, 'lng': 4.283638000488282}, 'northeast': {'lat': 50.9137489045753, 'lng': 4.60653305053711}, 'southeast': {'lat': 50.810382245925, 'lng': 4.60653305053711}}
}
```

## API Calls
To acces the API a password and username must be provided. Use the file witht he encrypted password send by me (SaYo). **Save this file in the same directory as** `API_c2c.py`.
```python
class Plane_API():
    def __init__(self) -> None:
        pw_enc = self.get_password()
        self.api = OpenSkyApi("SaYo",base64.b64decode(pw_enc).decode("utf-8"))
```

## Running the server 
To launch the server run the following line in a python environment.
```
python BackEnd_server.py
```
**This must be ran isnide the directory where you saved `BackEnd_server.py`!**

If you haven't already started the web application, you can launch it with the following command. Else refresh the page to conenct to the server. 
```
python -m http.server 8000
```
**This must be ran inside the `basic_html` folder!**

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.