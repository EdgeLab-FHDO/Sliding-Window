#PoAManager.py

import requests
import json
import time
from datetime import datetime

#TYPE: HNA-LAYER-2
#MODIFICATION: This file does NOT change
#DATE: 05-05-2020
"""
DESCRIPTION:
This file is used to handle the switch of PoA 
"""   

#do not change this url
url = 'http://localhost:30000/v1/events/MOBILITY' #the URL where we need to post the event so AdvantEDGE recognizes it
max_Distance=1 #initialize the variable
number_APs=1 #initialize the variable
separation_APs=1 #initialize the variable


class PoA_Manager(object):
#Parameters:
#m_Distance: the coverage area of all the PoA
# n_APs: the number of PoA in the scenario   
    def __init__(self, m_Distance, n_APs ):
        global max_Distance
        global number_APs
        global separation_APs
		
        max_Distance=m_Distance
        number_APs=n_APs
        separation_APs=max_Distance/number_APs #calculates the coverage area of each AP

#Determines the current AP the vehicle is "connected" to, based in the current position of the IV
#-->returns the current PoA where the car is connected
#Parameters:
#position_UE: the  current position of the vehicle    
    
    def Determine_AP (self,position_UE):
        global max_Distance
        global number_APs
        global separation_APs
        numberAP=0 #internal variable
        myAP=0 #current AP variable
        for i in range (0,max_Distance,int(separation_APs)):
            numberAP+=1
            min_coverage=i
            max_coverage=i+separation_APs
	
            if position_UE>min_coverage and position_UE<max_coverage:
                myAP=numberAP
            elif position_UE==min_coverage:
                myAP=numberAP -1
        return myAP

#Determines the boundaries of the PoA, to have an idea until what distance a determined AP covers	
#-->returns a list with the boundaries 
    def get_coord_coverage(self):
        global max_Distance
        global number_APs
        global separation_APs
        k=0
        Coord_Coverage_APs= [None] * (number_APs +1)
        for i in range (0,int(max_Distance+separation_APs) ,int(separation_APs)):
            Coord_Coverage_APs [k]=i
            k+=1
        return Coord_Coverage_APs

#Post the event mobility on AdvantEDGE
#Parameters:
#UE_ID: the ID of the UE. Must be the same as in AdvantEDGE
#PoA: The PoA we attempt to connect 
    def change_PoA (self,UE_ID,PoA):
        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        payload='''{"name": "name","type": "MOBILITY","eventMobility": {"elementName": "'''+str(UE_ID)+'''","dest": "poa'''+str(PoA)+'''"}}'''
        response = requests.post(url, data=(payload), headers=headers) #sends the event mobility request. Just works when AdvantEDGE is active
        #print ("No AdvantEdge--PoA:",PoA) #UNCOMMENT to avoid using AdvantEDGE
        print ("PoA: ",PoA,response, datetime.now())

	
	

if __name__ == "__main__":
    PoA_mod=2
    myPoA_manager=PoA_Manager(3000,10 )
    for i in range(0,9):
        print("poA: ", PoA_mod)
        print ("posting event")
        myPoA_manager.change_PoA("v001",PoA_mod)
        PoA_mod=PoA_mod+1
        time.sleep(1)
