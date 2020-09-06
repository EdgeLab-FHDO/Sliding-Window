
#clienttcp.py

import TCP_Message_manager as manage
from datetime import datetime
import socket
import threading
import time
import sys
import queue

server_data="test"
q_receive= queue.Queue() #Queue used to notify the thread_PoA_change


msg="close_comm"
def ConnectServers(port, host, debug=True):
        #global q_receive
        #global q_receive
        # create an instance of socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port) #set of ports 
    sock.connect(server_address)
        
    if debug:
        print(datetime.now())
        print('CONNECTED TO SERVER TESTING', host, port, '\n')

    while True:
        try:
                # try to receive data from the client
            server_data = sock.recv(1024).decode('utf-8')

            if server_data:
                #data = manage.getTCPdata(server_data)

                #my_data=data
                #print ("data into queue: ", data, port)
                q_receive.put(server_data)
                    #print ("in class:", q_receive.empty())
                    #for i in data:
        
                        #print ("consumming data TEST", i,"server:",  self.port)
                    #TODO: we consume the data of the buffer here
                #data.clear()
                     

        except :
            print ("clossing connection")
            sock.sendall(msg.encode('utf-8'))
            sock.close()
            return False


def getdata( ):
    while True:

        data_obtained=q_receive.get()
        data = manage.getTCPdata(data_obtained)
        print ("data in receive internal:" , data)


def CreateConnection(address, port):

    #x0_ThreadedClient=ThreadedClient(address, port, timeout=86400, debug=True)
    #x0_ThreadedClient.daemon = True
    #x0_ThreadedClient.start()
    x0_ThreadedClient = threading.Thread(target=ConnectServers, args=(port,address,))
    x0_ThreadedClient.daemon = True
    x0_ThreadedClient.start() 
    
    
    
    x0_ThreadedData = threading.Thread(target=getdata, args=())
    x0_ThreadedData.daemon = True
    x0_ThreadedData.start() 
    #x0_PoA_change = threading.Thread(target=thread_PoA_change, args=(App_ID,))


if __name__ == "__main__":
    #server_ports=[8008,8009,8010,8011,8012]
    server_ports=[30151,30152,30153,30154,30155]
    for port in server_ports:
        print ("connecting to server: ", port)
        CreateConnection('127.0.0.1', port)
    while True:
        try: 
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit()