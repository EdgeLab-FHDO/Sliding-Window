#VehicleMovemenManager.py
import time
#Coverts the speed of the car from Km/h to m/seg
def speed_m_seg(speed_km_h):
	speed=0
	speed_km_h=float(speed_km_h)
	speed=float(speed_km_h*1000/(3600))
	return speed

#rate_ms indicates the rate of the number of miliseconds we want to get the speed in
#How many meters does the car moves in <rate_ms>ms
def speed_m_mseg(speed_km_h, rate_ms):

	m_s= speed_m_seg(speed_km_h)
	div=1000/rate_ms
	speed= m_s/div 
	
	return speed


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
    speed =speed_m_mseg(speed_km_h, 100)
    for i in range (0,25):
        actual_position_car=move_vehicle(last_position_car,speed)
        last_position_car=actual_position_car
        print ("position vehicle: ",actual_position_car)
        time.sleep(0.09)
        