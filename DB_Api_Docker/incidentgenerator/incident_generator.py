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
    level=logging.DEBUG
)

generator = IncidentGeneratorAPI()

# TODO: refactor send_to_django as it is used by every api, and make it standard accross the apis.



def send_to_db(data, entry_id):
    """
        Send to db backend.
    """

    try:
        # Send POST request to Django server
        response = requests.post(DJANGO_SERVER_URL, json=data)
        if response.status_code == 201:
            pass
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
        
        logging.info(parsedresponse)
        
        # Send message to the backend XXX TODO
        generator.entries += 1
        
        
        
        
        
        
        time.sleep(random.randint(generator.interval[0], generator.interval[1]))
        

if __name__ == '__main__':
    asyncio.run(generate_incidents())