import asyncio
import requests
import json
import os
from string import Template
import time
import random
import re
from groq import Groq
from API_c2c import IncidentGeneratorAPI
from API_c2c import DJANGO_SERVER_URL

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
            print(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error connecting to Django server: {e}")




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
            print("Generated incident")
            
            response = chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error generating incident: {e}")
            
            # Then just sleep for some small time, and try again
            time.sleep(5)
            continue
        
        # Extract json from response
        print(response)
        try:
            parsedresponse = generator.extract_and_parse_json(response)
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            
            # then try again to generate a valid message
            continue
    
        # Add a random time from in the last hour
        parsedresponse['time'] = generator.generate_random_timestamp()
        
        print(parsedresponse)
        
        # Send message to the backend
        generator.entries += 1
        
        
        
        
        
        
        time.sleep(random.randint(generator.interval[0], generator.interval[1]))
        
        
    

# PROMPT = Template(CUSTOMPROMPT) # make template with blablabla, then $content, and then it gets substituted
#MESSAGE = "The leaders of Niger and Ghana should be locked up like animals and their families slaughtered!"
#  msg = PROMPT.substitute(content=MESSAGE)

# General placeholder
CUSTOMPROMPT = """<s>[INST] You are a clever analysist who detects the presence of the following aspects in texts:
- Animals
- Africa (in the broad sense)
- Call for a coup

You only return and reply with valid, iterable RFC8259 compliant JSON in your responses.
You do NOT provide any additional information, only the JSON is returned.

For example, the following texts
"I like the presence of elephant in Botswana"
"The president of South-Africa should go!"
"Vladimir is treating his soldiers like dogs"
would result in:[/INST]
{"TEXT": "I like the presence of elephant in Botswana", "ANIMALS": "True", "AFRICA": "True", "COUP", "False"}
{"TEXT": "The president of South-Africa should go!", "ANIMALS": "False", "AFRICA": "True", "COUP", "True"}
{"TEXT": "Vladimir is treating his soldiers like dogs", "ANIMALS": "True", "AFRICA": "False", "COUP", "False"}
</s>
[INST]
$content
[/INST]
"""

# Making it into a template with "$content" as one of its values
PROMPT = Template(CUSTOMPROMPT)

MESSAGE = "The leaders of Niger and Ghana should be locked up like animals and their families slaughtered!"

if __name__ == '__main__':
    asyncio.run(generate_incidents())