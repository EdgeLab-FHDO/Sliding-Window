#TCP_Message_manager.py

import time

#TYPE: ORIGINAL FILE
#MODIFICATION: This file does NOT need to change
#DATE: 15-04-2020
#TO-DOs: 
#   -Handle the data if the message has arrived partially  -->till now i havent have that problem but should be done in the future
"""
DESCRIPTION:
This file is used to read the data from the TCP buffer and split it according to the header of the message

Example:
    original message= helloworld
    server  sends = 0010helloworld --> header equals to the message lenght
    
based on the header it is possible to determine if the message has arrived complete or not
and if more than one message has arrived to the buffer 
"""   



TCP_Buffer= "0014Testing_Buffer0010my message0008the-rest0002hi0005heo"

header_length=4
init_position=0
TCP_messages=[ ]

#get the splited data based in the incomming message
#returns--> a list containing the separated messages as elements
#if more than one element , it means that the socket received  more than one message
#Parameters:
#TCP_Buffer: is the raw message we receive from the server (socket)
def getTCPdata(TCP_Buffer):

    while TCP_Buffer:
        char_to_read=int (TCP_Buffer[init_position: header_length])
        
        if len(TCP_Buffer)-header_length>char_to_read-1:
            TCP_message=TCP_Buffer[header_length:header_length+char_to_read]
            TCP_messages.append(TCP_message)
            TCP_Buffer=TCP_Buffer[header_length+char_to_read: len(TCP_Buffer)]
        else:
            print ("less chars-->partial message", TCP_Buffer)
            break
        
        
        #time.sleep(1)

    return TCP_messages
        
if __name__ == "__main__":

    print(getTCPdata(TCP_Buffer))