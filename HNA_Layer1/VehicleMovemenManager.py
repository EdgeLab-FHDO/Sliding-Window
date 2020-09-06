#VehicleMovemenManager.py
import time


#TYPE: HNA-LAYER-1
#MODIFICATION: This file does  NOT need to change
#DATE: 15-04-2020
"""
DESCRIPTION:
#Coverts the speed of the car from Km/h to m/seg --> m/millisecond
"""   

def speed_m_seg(speed_km_h):
	speed=0
	speed_km_h=float(speed_km_h)
	speed=float(speed_km_h*1000/(3600))
	return speed

#Transforms the speed from km/h into m/ (x) millisecond
#return--> float speed in m/ (x) milliseconds
#Parameters:
#speed_km_h: speed of the vehicle in km/h
#rate_ms indicates the rate of the number of miliseconds we want to get the speed in
    #How many meters does the car move in <rate_ms>ms
def speed_m_mseg(speed_km_h, rate_ms):

	m_s= speed_m_seg(speed_km_h)
	div=1000/rate_ms
	speed= m_s/div 
	
	return speed

#updates the current position of the vehicle. It is called once per iteration (the iteration time must be equal to the <rate_ms>ms
#last_position_car: position of the car before moving it
#speed: distance it moves in (x) milliseconds --> obtained using  speed_m_mseg( )
def move_vehicle(last_position_car, speed):
    actual_position_car=last_position_car+speed #moves the car with real speed each Xms
    return actual_position_car
	
if __name__ == "__main__":
    speed_km_h=50
	
    print ("50km/h speed in m/ms: ", speed_m_mseg(speed_km_h, 1))
    print ("50km/h speed in m/5ms: ", speed_m_mseg(speed_km_h, 5))
    print ("50km/h speed in m/10ms: ", speed_m_mseg(speed_km_h, 10)) #How many meters does the car moves in 10ms
    print ("50km/h speed in m/100ms: ", speed_m_mseg(speed_km_h, 100))
    last_position_car=0
    mov_time=100
    speed =speed_m_mseg(speed_km_h, mov_time)
    print( "moving the vehicle each", mov_time, "ms, at a speed of",speed_km_h, "km/h-->" ,speed,"m/",mov_time,"ms")
    for i in range (0,25):

        actual_position_car=move_vehicle(last_position_car,speed)
        last_position_car=actual_position_car
        print("time: " , time.time())
        print ("position vehicle: ",actual_position_car)
        time.sleep(0.1)
        