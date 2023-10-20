from time import sleep
from datetime import datetime
import time
from bluetooth import *
import requests	
	
Test = 1

#MyDevice = '00:18:12:22:01:3B'
MyDevice = '00:18:12:22:01:19'
#MyDevice = '00:18:12:51:81:17'
#MyDevice = 'CC:B1:1A:01:41:C5'
#MyDevice = '00:18:12:22:01:26' smidt ud

current_time = datetime.now()

print(str(current_time) + " Weight starting ")  
	
while True:
    Found = True

########################################################

    print("Connecting to device")
    
    Connected = False
    while not Connected:
        try:
            if Test: print("waiting connecting...")
            client = BluetoothSocket(RFCOMM)
            client.bind((("",PORT_ANY)))
            client.listen(1)
            client_sock, client_info = client.accept()
            print("Accepted connection from", client_info)
            #client.connect((MyDevice,1))
        except IOError as ex:
            if Test:
                print ("unable to connect:" + str(ex))
                print("Sleeping..")
                sys.stdout.flush()
            sleep(5)
        except Exception as ex:
            print('Connected exception: ' + str(ex))
        else:
            Connected = True
    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print("Received", data)
    except OSError:
        pass
    current_time = datetime.now()
    print (str(current_time) + ' connected')
    exit
#################################################

    Message = bytearray([])
    Count = 0
    sys.stdout.write("receiving.. ")


current_time = datetime.now()
print (str(current_time) + ' Finish')
print ("FINISH")

