#TCP_Message_manager.py

import time

TCP_Buffer= "0014Testing_Buffer0010my message0008the-rest0002hi0005heo"

header_length=4
init_position=0
TCP_messages=[ ]


def getTCPdata(TCP_Buffer):
    TCP_messages.clear()
    while TCP_Buffer:
        char_to_read=int (TCP_Buffer[init_position: header_length])
        
        if len(TCP_Buffer)-header_length>char_to_read-1:
            TCP_message=TCP_Buffer[header_length:header_length+char_to_read]
            TCP_messages.append(TCP_message)
            TCP_Buffer=TCP_Buffer[header_length+char_to_read: len(TCP_Buffer)]
        else:
            print ("less chars")
            break
        
        
        #time.sleep(1)

    return TCP_messages
        
if __name__ == "__main__":

    getTCPdata(TCP_Buffer)