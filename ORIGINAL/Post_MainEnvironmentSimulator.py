#Post_MainEnvironmentSimulator.py
#Version:4
#Date:2020-04-14
#Author: Jaime Burbano

#Description: This file is the MAIN to run the PUBLISHER application of the HNA (Hazard Notification App)
#runs with python 3
        #python3 MainEnvironmentSimulator v001
        
#TYPE: ORIGINAL FILE
#MODIFICATION: This file NEEDS TO BE MODIFIED
    # Change log configurations to set a new log-file (must be the same as Receive_MainEnvironmentSimulator)
    #Change the hazard_generator  to change the generation type and distance between hazards
    #uncomment/comment in the import the RestClient to import  to use window or single-server approach
    
    #-------------Hint: to find the lines you need to modify, search for "MODIFICATION"------------
import argparse
import threading
import time
import queue
from datetime import datetime
import ScenarioReader  #reads the variables of the scenario
import VehicleMovemenManager as movement #Converts the speed of the car to   X ms/s
import HazardManager
import PoAManager#Manages the change of PoA
import logging
import RestClientSingle as RESTclient #Interacts with the REST-Server        #MODIFICATION-UNCOMMENT to use single server approach
#import RestClientWindow as RESTclient #Interacts with the REST-Server      #MODIFICATION-UNCOMMENT to use Window approach

#----Argument Receiver----
#Receives as an argument the ID of the vehicle
parser = argparse.ArgumentParser()
parser.add_argument("Vehicle_ID", help="type the vehicle ID (V001,V002...)")
args = parser.parse_args()

App_ID=args.Vehicle_ID #the given Vehicle ID must match with the one of the scenario and also the UE name on AdvantEDGE

#----Configuration of the logging file----
#MODIFICATION-Change the path or file name to store the data in a different file
log_path='/home/jaime/Desktop/code/AdvantEDGE/2020-04-11/code/ORIGINAL/logger/'
log_file_name='HNA_ORIGINAL_TEST.log'
log_file=log_path+log_file_name
logging.basicConfig(level=logging.INFO, filename=log_file, filemode='a', format='%(name)s - %(levelname)s - %(message)s')

"""
SCRIPT VARIABLES
"""
end_flag=1 #Determines when to finish the simulation
synch_delay=1#time to wait in minutes before running the script in order to synch all the clients
detection_range=1 #The detection range in meters in which the car can detect a hazzard 
simulation_speed=10 #determines the speed of the vehicle in ms. This value must match with the time.sleep of the movement thread
hazard_generator=['equidistant',20] #sets how to create the hazard and the separation distance
#MODIFICATION - change the generation type above
"""
QUEUE DECLARATION
"""
q_hazard = queue.Queue() #Queue used to send data from the movement thread to the hazard publisher thread
q_PoA = queue.LifoQueue() #Queue used to notify the thread_PoA_change

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
my_hazard_generator=HazardManager.hazard_generator(max_Distance,vehicle_speed,vehicle_init_pos) #coverage_area,car_speed,car_init_position
print ('generating list by equidistant distance')
my_hazard_generator.generate_hazard_list(hazard_generator[0],hazard_generator[1])
my_hazard_detector=HazardManager.hazard_detector()

#print ("simulating scenario for vehicle:" , App_ID)
#print ("vehicle_speed: ",vehicle_speed )
#print ("vehicle_init_pos: ", vehicle_init_pos )
#print ("max_Distance: ", max_Distance )
#print ("number_APs: ",number_APs )

"""
REGISTERING THE VEHICLE AND SETTING THE SCENARIO
"""

print("poA limits: ", myPoA_manager.get_coord_coverage()) #show the coverage area of the PoA defined in the scenario file
print ("the PoA is: ", myPoA_manager.Determine_AP (vehicle_init_pos)) #shows the PoA where the vehicle is connected initially
myPoA_manager.change_PoA(App_ID, myPoA_manager.Determine_AP (vehicle_init_pos)) #call mobility event on AdvantEDGE
#to move the vehicle to the initial PoA before starting with the simulation


#--------------------------------------------------------------
#FUNCTIONS
#--------------------------------------------------------------	
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

        if my_hazard_detector.detect_hazard(actual_position_car,detection_range):
            q_hazard.put(actual_position_car)#Call RESTCliet thread
			
        actual_position_car=actual_position_car+m_Xms #moves the car with real speed each Xms
											
		#TODO: make sure the complete loops is 10ms --> use waitUntil

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
        
#Thread to publish the hazard in the server
#Parameters:
#Vehicle_ID: the ID of the current vehicle (defined as a parameter)		
def thread_hazard_notifier(vehicle_ID):
    global counter_hazard
    global end_flag
    global a1
    sequence_number=-1#to put a number to the hazard to be posted
    while True:	
        sequence_number+=1
        actual_position_car = q_hazard.get() #get the position of the car when it detected the hazard
        h_location=actual_position_car
        h_type="TT" #just to test the type of hazard detected
        id_hazard= vehicle_ID+ "-"+str(sequence_number) #to show the ID of the car that has detected the hazard
		
        posting_time=time.time() #take the time before posting
        print ("hazard: ", h_location, "number:", sequence_number )
        #-->POST HAZARD TO SERVER
        RESTclient.post_hazard (id_hazard,"00", h_type, h_location,a1) #calls the function to post the hazard
        #end_posting_time=time.time()        
        #print("time: ", end_posting_time-posting_time)
        logging.info("*{'V_ID':'%s','det_time':'%s','h_ID':'%s','type':'%s', 'location':%s}",vehicle_ID, posting_time,id_hazard, h_type, h_location)
		
        if end_flag==0:
            break

    time.sleep(0.01)	

		
#--------------------------------------------------------------
#MAIN
#--------------------------------------------------------------		
if __name__ == "__main__":

	#SET HERE THE START TIME OF THE SIMULATION --> 2 MINUTES AFTER THE ACTUAL TIME 


    a = datetime.now()
    actual_time= datetime.now().minute
    if actual_time==59:
        d= datetime(datetime.now().year, datetime.now().month, datetime.now().day,datetime.now().hour+1 ,0)
    else:
        execution_time = actual_time+synch_delay
        d= datetime(datetime.now().year, datetime.now().month, datetime.now().day,datetime.now().hour ,execution_time)
    print("init time: ",d )

    while True: #stays in the loop until the program must start
        a = datetime.now()

        if d<=a :
            print (a,"---------POSTER------------", d )
            break	
        time.sleep(0.001)
    #STARTING ALL THREADS 
    x0_vehicle_movement = threading.Thread(target=thread_vehicle_movement, args=(App_ID,vehicle_init_pos,vehicle_speed))
    x0_vehicle_movement.daemon = True
    x0_vehicle_movement.start()
	
    x0_hazard_notifier = threading.Thread(target=thread_hazard_notifier, args=(App_ID,))
    x0_hazard_notifier.daemon = True
    x0_hazard_notifier.start()

    x0_PoA_change = threading.Thread(target=thread_PoA_change, args=(App_ID,))
    x0_PoA_change.daemon = True
    x0_PoA_change.start()


	

    while True:
        if end_flag==0:
            
            break
        time.sleep(0.2)