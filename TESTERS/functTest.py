#raceConditionLock.py

import threading
import time 
import random
url_root="advantEDGE:"
url="url:"
lock = threading.Lock()
def taskofPoster(lock):
    global url
    while True:
        lock.acquire()
        print ("posting to: ", url)
        lock.release()
        time.sleep(0.01)
        


def taskofHandOff(lock,off_time,PoA):
    global url
    time.sleep(off_time)
    url_new=url_root+str(PoA)
    print ("updating url to:", url_new)
    lock.acquire()
    url=url_new
    lock.release()
    



def poster( ):
    global lock

    t1 = threading.Thread(target = taskofPoster, args = (lock,))
    t1.daemon = True
    t1.start()
    #t1.join()

#       x0_vehicle_movement = threading.Thread(target=thread_vehicle_movement, args=(App_ID,vehicle_init_pos,vehicle_speed))
#   x0_vehicle_movement.daemon = True
#    x0_vehicle_movement.start()
   
   
def handoff(PoA):
    global lock
    t2 = threading.Thread(target = taskofHandOff, args = (lock,0.01,PoA))
    t2.start()
    #t2.join()

if __name__ == "__main__":

    poster( )
    for i in range(50):

        handoff(i)
        time.sleep(random.randint(10,100)/1000)
      
      
      