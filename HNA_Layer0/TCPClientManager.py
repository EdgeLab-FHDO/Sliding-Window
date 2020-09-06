#TCPClientManager.py

import TCP_Message_manager as manage
from datetime import datetime
from json import loads, dumps
from pprint import pprint
import socket
from threading import Thread


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
                res = self.sock.recv(1024).decode('utf-8')

                if res:
                    data = manage.getTCPdata(res)
                #print ("data: ", data)
                    for i in data:
        
                        print ("consumming data TEST", i)
                    #TODO: we consume the data of the buffer here
                    data.clear()

                else:
                    raise error('Client disconnected')

            except KeyboardInterrupt:
                print ("clossing connection")
                sock.sendall(msg.encode('utf-8'))
                sock.close()
                return False
def CreateConnection(address, port):
    x0_ThreadedClient=ThreadedClient(address, port, timeout=86400, debug=True)
    #x0_ThreadedClient.daemon = True
    x0_ThreadedClient.start()


if __name__ == "__main__":
   CreateConnection('127.0.0.1', 8008)
