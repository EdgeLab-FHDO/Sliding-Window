#TCPClientManager.py

import TCP_Message_manager as manage
from datetime import datetime
from json import loads, dumps
from pprint import pprint
import socket
from threading import Thread
import time
import sys
import queue

server_data="test"
q_receive= queue.Queue() #Queue used to notify the thread_PoA_change
class ThreadedClient(Thread):

    def __init__(self, host, port, timeout=60, debug=False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.debug = debug
        Thread.__init__(self)

    # run by the Thread object
    def run(self):
        if self.debug:
            print(datetime.now())
            print('CLIENT Starting...', '\n')

        self.ConnectServers(self.host, self.port)

    def ConnectServers(self, host, port):
        #global q_receive
        #global q_receive
        # create an instance of socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host, self.port) #set of ports 
        self.sock.connect(server_address)
        
        if self.debug:
            print(datetime.now())
            print('CONNECTED TO SERVER TESTING', self.host, self.port, '\n')



        msg="close_comm"
        while True:
            try:
                # try to receive data from the client
                server_data = self.sock.recv(1024).decode('utf-8')

                #if server_data:
                    #data = manage.getTCPdata(server_data)

                    #server_data=data
                print ("data into queue: ", data, self.port)
                q_receive.put(server_data)
                    #print ("in class:", q_receive.empty())
                    #for i in data:
        
                        #print ("consumming data TEST", i,"server:",  self.port)
                    #TODO: we consume the data of the buffer here
                    #data.clear()
                     

            except :
                print ("clossing connection")
                self.sock.sendall(msg.encode('utf-8'))
                self.sock.close()
                return False


    def getdata(self ):
        #global data
        #print ("outside: ",q_receive.empty())
        #data=q_receive.get()
        print ("data in receive internal:")


def CreateConnection(address, port):

    x0_ThreadedClient=ThreadedClient(address, port, timeout=86400, debug=True)
    x0_ThreadedClient.daemon = True
    x0_ThreadedClient.start()
def getdataserver():
    #global q_receive
    datas =q_receive.get()
    return datas

if __name__ == "__main__":
    server_ports=[8008,8009,8010,8011,8012]
    #server_ports=[8008]
    for port in server_ports:
        CreateConnection('127.0.0.1', port)
    while True:
        try: 
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit()
