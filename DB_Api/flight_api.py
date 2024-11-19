import time
from API_c2c import Plane_API

# Used API's
P_API = Plane_API()

BBOX = (-31.5, 34.5, 39.5, 71.2)

def main():
    while True:
        response = P_API.get_bbox_call(BBOX)
        
        if response is not None:
            states = response.states
            #gp1_planes = P_API.generate_multiple_json(states[:1000]) "We put a certain limitation --> why ? "
            gp1_planes = P_API.generate_multiple_json(states)
            print(gp1_planes)
        else:
            print("No planes found in this area.")
            
        time.sleep(5)
            
        
        
if _name_ == '_main_':
    main()
