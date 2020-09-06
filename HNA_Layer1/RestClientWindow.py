#RestClientThreads.py
import requests
import json
import time
import threading

#TYPE: HNA-LAYER-1
#MODIFICATION: This file NEEDS TO BE MODIFIED
    #-According to the layer, a different NUMBER_POA_SCENARIO  is required 
#DATE: 15-04-2020
#TO-DOs: 
#   -Testing not updated

"""
DESCRIPTION:
#Implements the window approach, were a car publishes to the current server, the prevous one and the next one
#This script attempts to creates 3 independent thread3 used to publish to each given URL. 
#in single approach we just publish to one server at a given time

"""   


NUMBER_POA_SCENARIO=5  #MODIFICATION-this must be the same number of active servers in the scenario
detected_hazards_urls=['http://192.168.122.104:30121/detected_hazard','http://192.168.122.104:30121/detected_hazard','http://192.168.122.104:30121/detected_hazard'] #URL of the server when using AdvantEDGE

url_vehicles='http://192.168.122.104:30121/vehiclelist'
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

#posts a generic message on the server -->returns: payload
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

   
    if PoA==1:
        detected_hazards_urls[0]='http://192.168.122.104:301'+str(PoA+20)+'/detected_hazard'
        detected_hazards_urls[1]='http://192.168.122.104:301'+str(PoA+20)+'/detected_hazard'
        detected_hazards_urls[2]='http://192.168.122.104:301'+str(PoA+21)+'/detected_hazard' 

        #detected_hazards_urls[0]='http://192.168.122.104:151'+str(PoA+50)+'/detected_hazard'
        #detected_hazards_urls[1]='http://192.168.122.104:151'+str(PoA+50)+'/detected_hazard'
        #detected_hazards_urls[2]='http://192.168.122.104:151'+str(PoA+51)+'/detected_hazard' 
        
    elif PoA==NUMBER_POA_SCENARIO:
        detected_hazards_urls[0]='http://192.168.122.104:301'+str(PoA+20)+'/detected_hazard'
        detected_hazards_urls[1]='http://192.168.122.104:301'+str(PoA+19)+'/detected_hazard'
        detected_hazards_urls[2]='http://192.168.122.104:301'+str(PoA+20)+'/detected_hazard' 
        
        #detected_hazards_urls[0]='http://192.168.122.104:151'+str(PoA+50)+'/detected_hazard'
        #detected_hazards_urls[1]='http://192.168.122.104:151'+str(PoA+49)+'/detected_hazard'
        #detected_hazards_urls[2]='http://192.168.122.104:151'+str(PoA+50)+'/detected_hazard''
    else:
        detected_hazards_urls[0]='http://192.168.122.104:301'+str(PoA+20)+'/detected_hazard'
        detected_hazards_urls[1]='http://192.168.122.104:301'+str(PoA+19)+'/detected_hazard'
        detected_hazards_urls[2]='http://192.168.122.104:301'+str(PoA+21)+'/detected_hazard' 

        #detected_hazards_urls[0]='http://192.168.122.104:151'+str(PoA+50)+'/detected_hazard'
        #detected_hazards_urls[1]='http://192.168.122.104:151'+str(PoA+49)+'/detected_hazard'
        #detected_hazards_urls[2]='http://192.168.122.104:151'+str(PoA+51)+'/detected_hazard'     
    #print(detected_hazards_urls) 
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
    posting_time=time.time() 
    response=requests.post(url,data=(payload),headers=headers)
    end_posting_time=time.time() 
    #print ("time: ",url)

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