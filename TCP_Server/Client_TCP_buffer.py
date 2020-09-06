#Client_TCP_buffer.py

import socket
import time
import TCP_Message_manager as manage
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8008)
sock.connect(server_address)
msg="close_comm"

running=True
while (running): 
    try:
        # Send the message
        #sock.sendall(msg.encode('utf-8'))

        # Receive the message back
       
        res = sock.recv(1024).decode('utf-8')
        #print ("TCP_Buffer: ",res)
        if res:
            data = manage.getTCPdata(res)
            #print ("data: ", data)
            for i in data:
        
                print ("consumming data", i)
            #TODO: we consume the data of the buffer here
            data.clear()
        else:
            print ("no data")
            time.sleep(2)
        
    except KeyboardInterrupt:
        print ("clossing connection")
        sock.sendall(msg.encode('utf-8'))
        sock.close()

        running=False

    time.sleep(0.01)