#RestClientThreads.py
import requests
import json
import time
import threading

#Date:15-04-2020
#Description
#This script attempts to create an independent thread used to publish to each URL. 


detected_hazards_urls=['http://192.168.122.104:15151/detected_hazard'] #URL of the server NOT using AdvantEDGE
#detected_hazards_urls=['http://192.168.122.104:30151/detected_hazard'] #URL of the server using AdvantEDGE
url_vehicles='http://192.168.122.104:15151/vehiclelist'
#define the headers to be sent in the post request
headers={'accept':'application/json','content-type':'application/json'}


def set_payload(h_identifier,h_name, h_type, h_location):
	
	
	payload='''{
	"id": "''' + str(h_identifier)+ '''",
	"sn": "'''+ str(h_name) + '''",
	"ht": "''' + str(h_type)+ '''",
	"l": "'''+ str(h_location)[0:10]+ '''"
	}'''

	return payload

def post_server (url,payload):
	response=requests.post(url,data=(payload),headers=headers)
	print (response)
    
def post_vehicle_registration (V_id, port_v):


    payload='''{
	"id": "''' + str(V_id)+ '''",
	"port": "'''+ str(port_v) + '''"
	}'''

    response=requests.post(url_vehicles,data=(payload),headers=headers)
    #print (response)

def get_vehicle_list():
	r = requests.get(url_vehicles) 
	#r.text returns the data given by the server (corresponding to the information asked)
	return r.text
	
def post_hazard (h_identifier,h_name, h_type, h_location,PoA):
    payload=set_payload(h_identifier,h_name, h_type, h_location)
    #response=requests.post(detected_hazards_url,data=(payload),headers=headers)
    for url in detected_hazards_urls:
    
        x0_vehicle_movement = threading.Thread(target=poster, args=(payload,url))
        x0_vehicle_movement.daemon = True
        x0_vehicle_movement.start()

    

def poster (payload,url):
    #print("starting thread:", url)
    #posting_time=time.time() 
    response=requests.post(url,data=(payload),headers=headers)
    #end_posting_time=time.time() 
    #print ("time: ",url,end_posting_time-posting_time)
    
def get_hazards_list():
	r = requests.get(detected_hazards_url) 
	#r.text returns the data given by the server (corresponding to the information asked)
	return r.text
def delete_hazard(identifier):
	url=detected_hazards_url+"/"+str(identifier)
	r = requests.delete(url) 
	#r.text returns the data given by the server (corresponding to the information asked)
	return r	







	
	
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