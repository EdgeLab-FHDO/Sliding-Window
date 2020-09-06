#Receive_MainEnvironmentSimulator.py
#Environment simulator + REST-Server + AdvantEDGE
#Version:4
#Date:2020-04-15
#Author: Jaime Burbano

#Description: This set of files are used to run the first simulation of the system using AdvantEDGE
#runs with python 3
        #python3 MainEnvironmentSimulator v002

#TYPE: HNA-INDIVITUAL-TEST-CASE
#MODIFICATION: This file NEEDS TO BE MODIFIED
    # Change log configurations to set a new log-file (must be the same as Receive_MainEnvironmentSimulator)
    #Change the ports of the servers to listen according to the scenario
    
    
    
import argparse
import threading
import time
import queue
from datetime import datetime
import ScenarioReader #Reads the scenario.json file and gets the individual data
import VehicleMovemenManager as movement #Converts the speed of the car to   X ms/s
import PoAManager#Manages the change of PoA
import logging
import TCP_Message_manager as manage #to handle the TCP buffer
import socket
import sys


#Receives as an argument the ID of the vehicle
parser = argparse.ArgumentParser()
parser.add_argument("Vehicle_ID", help="type the vehicle ID (V001,V002...)")
args = parser.parse_args()

App_ID=args.Vehicle_ID #the given Vehicle ID must match with the one of the scenario

#----Configuration of the logging file----
#MODIFICATION-Change the path or file name to store the data in a different file
log_path='/home/jaime/Desktop/code/AdvantEDGE/2020-04-11/code/HNA_Individual_Test_Case/loggers/'
log_file_name='HNA-WINDOW-L2-TOTAL.log'
log_file=log_path+log_file_name
logging.basicConfig(level=logging.INFO, filename=log_file, filemode='a', format='%(name)s - %(levelname)s - %(message)s')

"""
SCRIPT VARIABLES
"""
#server_ports=[14151] # MODIFICATION - contains the port of each server the app connectes before-hand
server_ports=[30171,30172,30173] # MODIFICATION 
end_flag=1 #Determines when to finish the simulation
synch_delay=1 #time to wait in minutes before running the script in order to synch all the clients
simulation_speed=10 #determines the speed of the vehicle in ms. This value must match with the time.sleep of the movement thread
msg="close_comm" #message sent to server when clossing socket (server must have the same config)
"""
QUEUE DECLARATION
"""
q_PoA = queue.LifoQueue() #Queue used to notify the thread_PoA_change
q_receive= queue.Queue() #Queue used to notify the thread_receiver
"""
SETTING THE SYSTEM
"""
my_car_info=ScenarioReader.car_info(App_ID)
my_poa_info=ScenarioReader.poa_info() 

vehicle_speed=my_car_info.get_vehicle_speed()
vehicle_init_pos= my_car_info.get_car_initPosition()
max_Distance=my_poa_info.get_coverage_area()
number_APs= my_poa_info.get_number_APs()

myPoA_manager=PoAManager.PoA_Manager(max_Distance,number_APs ) #creates an object of the PoA_Manager class

"""
REGISTERING THE VEHICLE AND SETTING THE SCENARIO
"""
print ("simulating scenario for vehicle:" , App_ID)
print("poA limits: ", myPoA_manager.get_coord_coverage())
print ("the PoA is: ", myPoA_manager.Determine_AP (vehicle_init_pos))
myPoA_manager.change_PoA(App_ID, myPoA_manager.Determine_AP (vehicle_init_pos)) #call mobility event on AdvantEDGE

#Function to open the socket with a  given server and start listening to it
#Parameters:
#port: the port the server is listening to 
#host: the IP of the server
#debug: to print debug messages
def ConnectServers(port, host, debug=True):

    # create an instance of socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port) #set of ports 
    sock.connect(server_address)
        
    if debug:
        #print(datetime.now())
        print('CONNECTED TO SERVER ', host, port, '\n')

    while True:
        try:
            # try to receive data from the client
            server_data = sock.recv(1024).decode('utf-8')
            if server_data:
                #All listener threads put the data in the same queue and just 1 reader gets from there
                q_receive.put(server_data) #if we receive any data we put in a queue so the consumer can read it
        except :
            print ("clossing connection")
            sock.sendall(msg.encode('utf-8'))
            sock.close()
            return False

#Function to consume the incomming data from the server(s)
#Parameters:
#Vehicle_ID: the ID of the current vehicle (defined as a args parameter)
def getdata( vehicle_ID):
    myHazardList=['v0'] #initialize the variable
    while True:

        data_obtained=q_receive.get() #get the data from the common queue
        received_time= time.time()#takes the receiving time
        data = manage.getTCPdata(data_obtained) #process the header of the data
        position=get_car_position() #gets the position of the car
        dict_data=eval(data[0]) #Converts the received data to a dictionary
       #print("received_",dict_data)
        if dict_data["id"][0:4] != vehicle_ID: #Validate if the ID of the received message is equal to the actual car ID
            #print (vehicle_ID, "-->", dict_data)
            print ("rec: ",dict_data["id"],dict_data["sn"]) #if not the same vehicle, print the incomming hazard
            #Check if the hazard has been already received from any other server
            for item in myHazardList:
                if item==dict_data["id"]:
                    log_flag=False
                    break
                else :
                    log_flag=True
            if log_flag:
                myHazardList.append(dict_data["id"]) #put the new data in the internal list
                logging.info("*{'V_ID':'%s','rec_time':'%s','h_ID':'%s','type':'%s', 'location':%s, 'server':'%s'}", vehicle_ID,received_time,dict_data["id"], dict_data['ht'],position,dict_data['sn'])
        
        data.clear() #Clean the buffer because the data has been allready consumed
        
#Function used to create individual threads to connect to each server
#Parameters:
#port: the port the server is listening to 
#address: the IP of the server
def CreateConnection(address, port):

    x0_ThreadedClient = threading.Thread(target=ConnectServers, args=(port,address,))
    x0_ThreadedClient.daemon = True
    x0_ThreadedClient.start() 
    
#Function used to create the listener thread    
#App_ID: the ID of the current vehicle (defined as a args parameter)
def CreateListener(App_ID):
    x0_ThreadedData = threading.Thread(target=getdata, args=(App_ID,))
    x0_ThreadedData.daemon = True
    x0_ThreadedData.start() 


#Thread to control the movement of the vehicle
#Parameters:
#Vehicle_ID: the ID of the current vehicle (defined as a parameter)
#vehicle_init_pos: initial point  ( read from the scenario)
#vehicle_speed:  ( read from the scenario)
def thread_vehicle_movement(vehicle_ID, vehicle_init_pos, vehicle_speed):
    global end_flag
    global actual_position_car
    global a1
    c=0
    a0=1#to check the when to change of PoA
    a1=1#to check the when to change of PoA

    m_Xms=movement.speed_m_mseg(vehicle_speed,simulation_speed) #Change the 2nd parameter to the number of ms 
    actual_position_car=vehicle_init_pos

    while True:
        start=time.time()
        #determine if the simulation must be finished
        if actual_position_car> max_Distance:
            print ('---------simulation finished---------')
            end_flag=0 #sets the flag to close the main file also
            break
            
        a1=myPoA_manager.Determine_AP (actual_position_car) #Determine current PoA
        if a1!=a0: #Excecute just when the current AP is different to the previous
            q_PoA.put(a1) #Call change of PoA thread
            a0=a1 #Update value of the last registered AP

        actual_position_car=actual_position_car+m_Xms #moves the car with real speed each Xms
											
		#TODO: make sure the complete loops is 10ms --> use waitUntil
        #print (actual_position_car)
        time.sleep(0.01) #should be 10ms --> make sure it is always the same
        end=time.time()
        #print ("time: ", end-start)
		
		
#Thread to trigger the AP switching
#Parameters:
#Vehicle_ID: the ID of the current vehicle (defined as a parameter)
def thread_PoA_change(vehicle_ID):
	global end_flag

	while True:	
		PoA=q_PoA.get()
		myPoA_manager.change_PoA(vehicle_ID, PoA) #call mobility event ond AdvantEDGE
		if end_flag==0:
			break
		time.sleep(0.01)

#Get the current position of the vehicle 
#-->returns the position 
def get_car_position():
	global actual_position_car
	car_position=actual_position_car
	return car_position 
	
		
#--------------------------------------------------------------
#MAIN
#--------------------------------------------------------------		
if __name__ == "__main__":

    #SET HERE THE START TIME OF THE SIMULATION --> 2 MINUTES AFTER THE ACTUAL TIME 
    a = datetime.now()
    actual_time= datetime.now().minute
    if actual_time==59:#validates the time in case it must start at 00 of the next hour
        d= datetime(datetime.now().year, datetime.now().month, datetime.now().day,datetime.now().hour+1 ,0)
    else:
        execution_time = actual_time+synch_delay
        d= datetime(datetime.now().year, datetime.now().month, datetime.now().day,datetime.now().hour ,execution_time)
    print("init time: ",d )
    #CREATING TCP CONNECTION TO ALL THE REGISTERED SERVERS
    #Interates trough the given servers and creates a socket to connect and listen to each one
    for port in server_ports:
        print ("connecting to server: ", port)
        CreateConnection('127.0.0.1', port) #Creates an individual thread to listen each server
        #CreateConnection('192.168.122.104', port) #Creates an individual thread to listen each server
        #192.168.122.104
    CreateListener(App_ID) #Creates the listener thread

    while True: #stays in the loop until the program must start
        a = datetime.now()
        if d<=a :
            print (a,"---------RECEIVER------------", d )
            break	
        time.sleep(0.001)
    #STARTING THE MOVEMENT THREADS 
    x0_vehicle_movement = threading.Thread(target=thread_vehicle_movement, args=(App_ID,vehicle_init_pos,vehicle_speed))
    x0_vehicle_movement.daemon = True
    x0_vehicle_movement.start()

    x0_PoA_change = threading.Thread(target=thread_PoA_change, args=(App_ID,))
    x0_PoA_change.daemon = True
    x0_PoA_change.start()

    while True:
        if end_flag==0:
			
            break
        time.sleep(0.2)
