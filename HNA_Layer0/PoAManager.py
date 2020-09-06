#PoAManager.py

import requests
import json
import time
url = 'http://localhost:30000/v1/events/MOBILITY'
max_Distance=1
number_APs=1
separation_APs=1


class PoA_Manager(object):
    def __init__(self, m_Distance, n_APs ):
        global max_Distance
        global number_APs
        global separation_APs
		
        max_Distance=m_Distance
        number_APs=n_APs
        separation_APs=max_Distance/number_APs #calculates the coverage area of each AP


    #Determines the current AP the vehicle is "connected" to, based in the current position of the IV
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


#Returns a list containing the boundaries of the APs --> to have an idea until what distance a determined AP covers	
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
    def change_PoA (self,UE_ID,PoA):
        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        payload='''{"name": "name","type": "MOBILITY","eventMobility": {"elementName": "'''+str(UE_ID)+'''","dest": "poa'''+str(PoA)+'''"}}'''
        ##response = requests.post(url, data=(payload), headers=headers)
        print ("No AdvantEdge--PoA:",PoA)
        ##print ("PoA: ",PoA,response)

	
	

if __name__ == "__main__":
    PoA_mod=2
    myPoA_manager=PoA_Manager(3000,10 )
    for i in range(0,9):
        print("poA: ", PoA_mod)
        print ("posting event")
        myPoA_manager.change_PoA("v001",PoA_mod)
        PoA_mod=PoA_mod+1
        time.sleep(5)
