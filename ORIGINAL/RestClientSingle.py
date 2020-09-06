#RestClientThreads.py
import requests
import json
import time
import threading




#TYPE: ORIGINAL FILE
#MODIFICATION: This file NEEDS TO BE MODIFIED
    #-According to the layer, a different publishing set of URLs is required 
#DATE: 15-04-2020
#TO-DOs: 
#   -Testing not updated
#   -Implement a logic to publish only in the current server
#   - Implement a hand-off delay 

#       Hand-off delay means that after we get the event mobility (change of PoA in AdvantEDGE),
#       it is required to "wait" for some time until we start publishinig in the correspondent server.
#       This time must be configurable 
"""
DESCRIPTION:
#This script attempts to create an independent thread used to publish to each given URL. 
#in single approach we just publish to one server at a given time

"""   


detected_hazards_urls=['http://192.168.122.104:15151/detected_hazard'] #MODIFICATION-URL of the server NOT using AdvantEDGE
#detected_hazards_urls=['http://192.168.122.104:30151/detected_hazard'] #URL of the server using AdvantEDGE
url_vehicles='http://192.168.122.104:15151/vehiclelist'
#define the headers to be sent in the post request
headers={'accept':'application/json','content-type':'application/json'}

#generates the message to be posted -->returns: payload
#Parameters:
#h_identifier=a unique identifier o the hazard 
#h_name= a given information of the hazard (not used now)
#h_type=a 2 char string to say the type of hazard (an-->animal, ph-->pothole, pd-->pedestrian...)
#h_location= the location of where the car started to "detect" the hazard
def set_payload(h_identifier,h_name, h_type, h_location):
	payload='''{
	"id": "''' + str(h_identifier)+ '''",
	"sn": "'''+ str(h_name) + '''",
	"ht": "''' + str(h_type)+ '''",
	"l": "'''+ str(h_location)[0:10]+ '''"
	}'''

	return payload
#posts a generic essage on the server -->returns: payload
#Parameters:
#url:  server url where to post
#payload: the string to post
def post_server (url,payload):
	response=requests.post(url,data=(payload),headers=headers)
	print (response)
 
#registers the vehicle in the server
#Parameters:
#V_id: the identifier of the vehicle (v001-v002...)
#port_v: the port the vehicle uses for the communication 
def post_vehicle_registration (V_id, port_v):


    payload='''{
	"id": "''' + str(V_id)+ '''",
	"port": "'''+ str(port_v) + '''"
	}'''

    response=requests.post(url_vehicles,data=(payload),headers=headers)
    #print (response)

#gets the list of vehicles registered in the server 
#returns--> string containing the vehicles iniformation
def get_vehicle_list():
	r = requests.get(url_vehicles) 
	#r.text returns the data given by the server (corresponding to the information asked)
	return r.text

#The method creates and independent thread for each server where we want to post	
#Parameters:
#h_identifier=a unique identifier o the hazard 
#h_name= a given information of the hazard (not used now)
#h_type=a 2 char string to say the type of hazard (an-->animal, ph-->pothole, pd-->pedestrian...)
#h_location= the location of where the car started to "detect" the hazard
def post_hazard (h_identifier,h_name, h_type, h_location,PoA):
    payload=set_payload(h_identifier,h_name, h_type, h_location)
    #response=requests.post(detected_hazards_url,data=(payload),headers=headers)
    #TODO: determine in which server to post based on the PoA
    for url in detected_hazards_urls:
    
        x0_vehicle_movement = threading.Thread(target=poster, args=(payload,url))
        x0_vehicle_movement.daemon = True
        x0_vehicle_movement.start()

    
#post a hazard in the server. 
#Parameters:
#payload: the formated data to be posted
#url: the server url
def poster (payload,url):
    #print("starting thread:", url)
    #posting_time=time.time() 
    response=requests.post(url,data=(payload),headers=headers)
    #end_posting_time=time.time() 
    #print ("time: ",url,end_posting_time-posting_time)
 

#gets the list of  registered  hazardsin the server 
#returns--> string containing the hzd iniformation 
def get_hazards_list():
	r = requests.get(detected_hazards_url) 
	#r.text returns the data given by the server (corresponding to the information asked)
	return r.text
    
#deletes a given hazard in the server DB
#returns --> 204 on success   
def delete_hazard(identifier):
	url=detected_hazards_url+"/"+str(identifier)
	r = requests.delete(url) 
	#r.text returns the data given by the server (corresponding to the information asked)
	return r	







	
#TODO: TESTING NOT UPDATED		
if __name__ == "__main__":
    post_vehicle_registration("v001",5005)
    print (get_vehicle_list())
    while True:
        start_time = time.time()
        print ("posting test hazard 1-test")
        resp= post_hazard ("h100","Testing_hazard1", "Test1", 1234)
        end_time = time.time()
        print ("Post time: ", end_time - start_time)

        time.sleep(2)