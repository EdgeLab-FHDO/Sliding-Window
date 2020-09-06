#client_tester.py

import TCPClientManager as tcp_handler
import time

service_ports=[8008]
address="127.0.0.1"


for port in service_ports:
    tcp_handler.CreateConnection(address,port)
    


while True:

    #pass
    print ("my data: ", tcp_handler.getdataserver())
    time.sleep(0.1)


