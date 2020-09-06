#Hazard_Manager.py

import random
import time

#DESCRIPTION
    #LALYER 0
    #Does NOT change in each layer
"""
This file is used to generate the hazards in the scenario. It has 3 types 
of generation
"""
"""generation_types: 
    'equidistant' --> the hazards are generated each {x} distance
    'random' --> a determined number of hazards are randomly generated
    'time' --> calculates the equivalence in distance in order to generate a hazard that will appear each {x} ms approx
"""   

#generated_hazard_list=[]

class hazard_generator(object):

    def __init__(self, coverage ,speed, init_position):
        global coverage_area
        global car_speed 
        global car_init_position
        coverage_area=coverage
        car_speed=speed
        car_init_position=init_position


    def generate_hazard_list(self, generate_type='equidistant', value=10):        
        global coverage_area
        global car_speed 
        global car_init_position        
        global generated_hazard_list
        if  generate_type == 'equidistant':
             generated_hazard_list=self.generate_equidistant(coverage_area, value,car_init_position)
        elif generate_type== 'random':
             generated_hazard_list=self.generate_random(coverage_area, value,car_init_position)
        else:
            generated_hazard_list=self.generate_by_time(coverage_area, value,car_speed,car_init_position)
        return  generated_hazard_list
     
    def generate_equidistant(self,coverage_area, distance,car_init_position):
        hazard_list=[]    
        for equidistant_hazard in range(car_init_position+10,coverage_area,distance):
            hazard_list.append(equidistant_hazard)
        return hazard_list
 
    def generate_random(self,coverage_area, number_hazards,car_init_position):
        hazard_list=[]       
        for i in range(0,number_hazards):
            random_hazard=random.randint(car_init_position+10,coverage_area)
            while  random_hazard in hazard_list:
                # A hazard in that position exists already, generating a new one
                random_hazard=random.randint(car_init_position+10,coverage_area)
            hazard_list.append(random_hazard)
        hazard_list.sort()
        return hazard_list
      
    def generate_by_time(self,coverage_area, time, car_speed,car_init_position):
        hazard_list=[]       
        speed_ms=car_speed/3600 #--> speed in milliseconds
        distance = speed_ms*time
        for equidistant_hazard in range(car_init_position+10,coverage_area,int(distance)):
            hazard_list.append(equidistant_hazard)
        return hazard_list



class hazard_detector(object):

    def __init__(self ):
        global generated_hazard_list
        global list_of_hazards        
        list_of_hazards=generated_hazard_list

        
    def detect_hazard(self, car_position, range_of_anticipation):
        global list_of_hazards 
        
        detection=False
        if  list_of_hazards:
            if  car_position+range_of_anticipation>=list_of_hazards[0]: #Hazard detected
                detection =True 
                #print ("hazard detected")

                list_of_hazards.remove(list_of_hazards[0])
                #print ("new list:", list_of_hazards)
        return detection








if __name__ == "__main__":

    my_hazard_generator=hazard_generator(800,140,200) #coverage_area,car_speed,car_init_position
    print ('generating list by equidistant distance')
    print (my_hazard_generator.generate_hazard_list('equidistant',100))
    #print ('generating random list ')
    #print (my_hazard_generator.generate_hazard_list('random',100))
    #print ('generating list by time')
    #print (my_hazard_generator.generate_hazard_list('time',100))
    
    #  THE HAZARD LIST MUST BE ALWAYS GENERATED BEFOREHAND
    
    my_hazard_detector=hazard_detector()
    car_position=200
    range=1 #-->range in meters
    while coverage_area> car_position:
        my_hazard_detector.detect_hazard(car_position,range)
        car_position+=1
        print (car_position)
        time.sleep(0.1)
        
        
        
        
