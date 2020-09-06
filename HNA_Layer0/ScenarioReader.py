#ScenarioReader.py
import os
import json

scenario_path="/home/jaime/Desktop/code/AdvantEDGE/2020-04-11/code/HNA_Individual_Test_Case/individual_scenarios/MT_Scenario_x-1.json" 
#Change above the name of the scenario file you want to read

#Opens the scenario file specified in <scenario_path>
with open(scenario_path) as json_file:
    data = json.load(json_file)

class car_info(object):
    def __init__(self, App_ID='v001'):
        self.set_vehicle_speed( App_ID)
        self.set_car_initPosition( App_ID)        
        #self.VehicleData(App_ID)
     
    def set_vehicle_speed(self, App_ID):
        for individualInfo in data["carInfo"]:
            try:
             self._vehicle_speed= individualInfo[App_ID]['carSpeed']
            except:
                pass

    def set_car_initPosition(self, App_ID):

        for individualInfo in data["carInfo"]:
            try:
             self._vehicle_init_pos= individualInfo[App_ID]["initPosition"]
            except:
                pass      
                
    def get_vehicle_speed(self):
        return self._vehicle_speed
        
    def get_car_initPosition(self):
        return self._vehicle_init_pos     


class poa_info(object):
    def __init__(self ):
        self.set_coverage_area()
        self.set_number_APs()

    def set_coverage_area(self):
        self._coverage_area=data["APsInfo"]["coverageArea"] #in meters
        
    def set_number_APs(self):
        self._number_APs=data["APsInfo"]["numberAPs"] #in meters
    
    def get_coverage_area (self):
        return self._coverage_area
        
    def get_number_APs (self):
        return self._number_APs
        
    def get_separation_APs (self):
        separation_APs=self.get_coverage_area () / self.get_number_APs ()
        return separation_APs

    def get_coverage_ranges(self):
        coverage_ranges=[]
        for i in range (0,self.get_coverage_area (),int(self.get_separation_APs ())):
            coverage_ranges.append(i)
        return coverage_ranges
        

	
if __name__ == "__main__":
    App_ID="v002"
    my_car_info=car_info(App_ID)
    my_poa_info=poa_info()   

    print ("setting the data from: ", App_ID)
    print ("Speed of the Vehicle: ",my_car_info.get_vehicle_speed()) 
    print ("Initial position: ", my_car_info.get_car_initPosition())
    print ("distance to be simulated: " ,my_poa_info.get_coverage_area())
    print ("Number of PoA in the scenario: ", my_poa_info.get_number_APs())
    print ("Separation of PoA in the scenario: ", my_poa_info.get_separation_APs())    
    print ("ranges of coverage in the scenario: ", my_poa_info.get_coverage_ranges())    
