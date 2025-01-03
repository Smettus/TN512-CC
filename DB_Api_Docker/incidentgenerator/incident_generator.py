import asyncio
import requests
import json
import os
from string import Template
import time
import random
import re
from groq import Groq
from generatorhelperfunctions import IncidentGeneratorAPI
from generatorhelperfunctions import DJANGO_SERVER_URL
import logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO # debug is too verbose
)

generator = IncidentGeneratorAPI()

# TODO: refactor send_to_django as it is used by every api, and make it standard accross the apis.



def send_to_db(data):
    """
        Send to db backend.
    """
    json_data = {
        'Type': "AbstractIncident",
        'Incidents': [data], # make it a list of dictionaries, each an incident
    }
    logging.info(json_data)
    try:
        # Send POST request to Django server
        response = requests.post(DJANGO_SERVER_URL, json=json_data)
        if response.status_code == 201:
            logging.info("Data sent to DB.")
        else:
            logging.info(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"Error connecting to Django server: {e}")




async def generate_incidents():
    """
    Generate incidents and send them to the Django server.
    """
    
    # maybe generate random cities or whatever, to guide it more. TODO
    
    while True:
        
        try: 
            chat_completion = generator.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": generator.MODERNPROMPT,
                    }
                ],
                model="llama3-8b-8192",
            )
            logging.info("Generated incident")
            
            response = chat_completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Error generating incident: {e}")
            
            # Then just sleep for some small time, and try again
            time.sleep(5)
            continue
        
        # Extract json from response
        #print(response)
        try:
            parsedresponse = generator.extract_and_parse_json(response)
        except Exception as e:
            logging.error(f"Error parsing JSON: {e}")
            
            # then try again to generate a valid message
            continue
    
        # Add a random time from in the last hour
        parsedresponse['time'] = generator.generate_random_timestamp()
        
        
        # XXX DO OTHER WAY ROUND, generate the prompt with the random time inserted
        # Also add a random coordinate with name of the city/thing to feed to the llm
        
        #logging.info(parsedresponse)
        
        # Send message to the backend XXX TODO
        generator.entries += 1 # does not care atm, as the db backend will auto-increment
        
        send_to_db(parsedresponse)
        
        
        
        
        
        
        
        time.sleep(random.randint(generator.interval[0], generator.interval[1]))
        

if __name__ == '__main__':
    asyncio.run(generate_incidents())
    
    
    
    
"""
import random
from datetime import datetime, timedelta

# List of Belgian cities and towns
belgian_places = [
    "Brussels", "Antwerp", "Ghent", "Charleroi", "Liège", 
    "Bruges", "Namur", "Leuven", "Mons", "Mechelen",
    "Hasselt", "Kortrijk", "Ostend", "Tournai", "Aalst"
]

def generate_random_coordinates():
    lat = random.uniform(49.5, 51.5)
    lon = random.uniform(2.5, 6.5)
    return round(lat, 4), round(lon, 4)

def generate_random_time():
    now = datetime.now()
    random_time = now - timedelta(minutes=random.randint(0, 1440))
    return random_time.strftime('%Y-%m-%d %H:%M:%S')

def generate_groq_prompt():
    lat, lon = generate_random_coordinates()
    place = random.choice(belgian_places)
    time = generate_random_time()

    prompt = {
        "lat": lat,
        "lon": lon,
        "place": place,
        "time": time,
        "msg_prompt": f"Generate a detailed news report about a military-style attack that occurred in {place}, Belgium, "
                      f"at coordinates ({lat}, {lon}). The attack happened at {time} and caused significant damage. "
                      f"Describe the location, casualties, damage, and emergency response in a vivid and realistic style."
    }
    return prompt

# Generate multiple prompts
for _ in range(5):  # Adjust the range as needed
    print(generate_groq_prompt())



"""