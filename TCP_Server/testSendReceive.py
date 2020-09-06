import json
import socket
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8008)
sock.connect(server_address)

# Create the data and load it into json
data = {
	'cmd': 'test',
	'data': ['foo', 'bar'],
}
msg = json.dumps(data)
running=True
while (running): 
    try:
        # Send the message
        #sock.sendall(msg.encode('utf-8'))

        # Receive the message back
        print ("receiving data from server")
        res = sock.recv(1024).decode('utf-8')
        #data = json.loads(res)
        print(res)	
    except KeyboardInterrupt:
        print ("clossing connection")

        sock.close()

        running=False

    time.sleep(0.01)