from datetime import datetime, timedelta
import json
import os
import random
import re
from groq import Groq


DJANGO_SERVER_URL = os.environ.get('DJANGO_URL')

class IncidentGeneratorAPI():
    def __init__(self):
        self.api_key = os.environ.get('KEY_INCIDENT_GENERATOR_API')
        self.client = self.get_client()
        
        
        self.entries = 0    # same scheme as the others. replace this with UUID?
        
        # Generation settings
        self.interval = [30, 120]    # set range in seconds
        # self.randomtime = True     
        # maybe set here a bbox to check if generated incident is in Belgium
        
        
        # Prompt
        self.PROMPT = """
            You are a journalist during the Second World War. Randomly select a small town in Belgium (avoid choosing the same town repeatedly). Generate a news message reporting an attack on this town. Include details about the damage, the number of casualties, and any notable locations affected. Ensure the output is formatted strictly as a JSON object, with the following keys:
            - 'lon': Longitude of the town.
            - 'lat': Latitude of the town.
            - 'msg': A detailed message about the attack.

            The response must only contain the JSON object.
        """
        
        self.MODERNPROMPT = """
            You are a journalist reporting live during a fictional conflict that is happening now. Randomly select a small town in Belgium (avoid choosing the same town repeatedly). Generate a news message reporting a recent attack on this town. Include details about the damage, the number of casualties, any notable locations affected, and any ongoing emergency responses. Ensure the output is formatted strictly as a JSON object, with the following keys:
            - 'lon': Longitude of the town.
            - 'lat': Latitude of the town.
            - 'msg': A detailed message about the live event.

            The response must only contain the JSON object.
        """
        # - 'time': The time of the event in the format 'YYYY-MM-DD HH:MM:SS'. Use near real time.
        
        # Supply cities?
        self.cities = [
            {"name": "Bastogne", "lon": 5.714722, "lat": 49.998889},
            {"name": "Dinant", "lon": 4.911667, "lat": 50.261667},
            {"name": "Tournai", "lon": 3.389333, "lat": 50.607722},
            {"name": "Ypres", "lon": 2.889444, "lat": 50.852778},
            {"name": "Mons", "lon": 3.957222, "lat": 50.454167},
            {"name": "Arlon", "lon": 5.816667, "lat": 49.683333},
            {"name": "Nivelles", "lon": 4.330833, "lat": 50.594167},
            {"name": "Malmedy", "lon": 6.027778, "lat": 50.426389},
        ]
    def get_client(self):
        client = Groq(api_key=self.api_key)
        return client
    def extract_and_parse_json(self, suspectedjson):
        # If one bracket misses, still accept
        #json_match = re.search(r'\{.*?\}', suspectedjson, re.DOTALL)
        json_match = re.search(r'\{.*', suspectedjson, re.DOTALL)
        
        
        if not json_match:
            raise ValueError("No JSON object found in the response.")
    
        raw_json = json_match.group()

        try:
            # First, try parsing the extracted JSON as-is
            parsed = json.loads(raw_json)
        except json.JSONDecodeError:
            # If bracket is missing
            fix1 = self.fix_missing_braces(raw_json)
            try:
                parsed = json.loads(fix1)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON even after fixes: {fix1}") from e

        return parsed
    def fix_missing_braces(self, json_text):
        open_braces = json_text.count("{")
        close_braces = json_text.count("}")
        
        # If there are more opening braces, add missing closing braces
        if open_braces > close_braces:
            json_text += "}" * (open_braces - close_braces)
        
        # If there are more closing braces, truncate extra ones
        elif close_braces > open_braces:
            json_text = json_text.rstrip("}" * (close_braces - open_braces))
        
        return json_text
    def generate_random_timestamp(self):
        now = datetime.now()
        random_minutes = random.randint(0, 59)
        random_seconds = random.randint(0, 59)
        random_time = now - timedelta(minutes=random_minutes, seconds=random_seconds)
        return random_time.strftime('%Y-%m-%d %H:%M:%S')
    def generate_json(self, data):
        json_object = {
            "Type": "AbstractIncident",
            "Properties": {
                "entry_id": None, # Get the self.entries here?
                "entity_id": data.get('UserID', None),  # unique MMSI nr
            },
        }
        return json.dumps(json_object, indent=4)