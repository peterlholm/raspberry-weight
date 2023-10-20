#!/bin/python3
import sys
from time import sleep
from datetime import datetime
#import time
from bluetooth import *
import requests	
	
Test = 1

#MyDevice = '00:18:12:22:01:3B'
#MyDevice = '00:18:12:22:01:19'
MyDevice = '00:18:12:51:81:07'
#MyDevice = '00:18:12:51:81:17'
#MyDevice = 'CC:B1:1A:01:41:C5'
#MyDevice = '00:18:12:22:01:26' smidt ud

DB_HOST = "http://motion.holmnet.dk/"

current_time = datetime.now()

print(str(current_time) + " Weight starting ")  
	
while True:
    Found = True

########################################################

    print("Connecting to device")
    
    Connected = False
    while not Connected:
        try:
            if Test:
                print("connecting...")
            client = BluetoothSocket(RFCOMM)
            client.connect((MyDevice, 1))
        except IOError as ex:
            if Test:
                print("unable to connect:" + str(ex))
                print("Sleeping..")
                sys.stdout.flush()
            sleep(5)
        except Exception as ex:
            print('Connected exception: ' + str(ex))
        else:
            Connected = True
    current_time = datetime.now()
    print (str(current_time) + ' connected')

#################################################

    Message = bytearray([])
    Count = 0
    sys.stdout.write("receiving.. ")
    while Count<21:
        try:
            data = client.recv(21-Count)
            if not data:
                print("Not data")
                break
            else:
                if Test: sys.stdout.write('.')
                Message += data
                Count += len(data)
        except BluetoothError as ex:
            print ("Exception  BlueToothError: " + str(ex) )
            break
        except IOError as ex:
            print ("Exception  IOerror: " + str(ex) + str(type(ex)))
            print ("I/O error({0}): {1}".format(ex.errno, ex.strerror))
            print(ex.message)
            print ('vars')
            print(vars(ex))
            print ('dir')
            break
        except Exception as ex:
            print ("Exception: " + str(ex) + str(type(ex)))
            break
    client.close()

    print("")
    
    if Count>=21:
        if Test: print("Decoding")
        Year=Message[0]*256+Message[1]
        Year=2023
        Month = Message[2]
        Day = Message[3]
        Hour = Message[4]
        Min = Message[5]
        Sec = Message[6]
        Age = Message[7] & 0x7F
        Height = Message[8]
        Weight = (Message[9]*256+Message[10])/10.0
        Fat = (Message[11]*256+Message[12])/10.0
        Bone = Message[13]/10.0
        Muscle = (Message[14]*256+Message[15])/10.0
        Vfat = Message[16]
        Moisture = (Message[17]*256+Message[18])/10.0
        Calorie = Message[19]*256+Message[20]

        
        print("Weight: %2.1f kg" % (Weight))
        if Test: print("Fat %2.1f %% Bone %2.1f kg Muscle %2.1f kg Vfat %3d Moist %2.1f %% Cal %3d" % (Fat, Bone, Muscle,Vfat, Moisture,Calorie))

        DateTime = "{:04d}-{:02d}-{:02d}%20{:02d}:{:02d}:{:02d}".format(Year, Month, Day, Hour, Min, Sec)
        Date = "{:4d}-{:02d}-{:02d}".format(Year, Month, Day)

        if Test: print(DateTime)
        
        fp=open('data.csv', 'a')
        fp.write("%04d-%02d-%02d %02d:%02d:%02d," % (Year, Month, Day, Hour, Min, Sec))
        fp.write("%2.1f, %2.1f, %2.1f," % (Weight, Fat, Bone))
        fp.write("%2.1f, %3d, %2.1f, %3d \n" % (Muscle, Vfat, Moisture, Calorie))
        fp.close()

        url= (DB_HOST +"motion/save.php?save&DateTime="+DateTime+"&Date="+Date+ \
              "&Weight={:03.1f}&Height={:03d}&Fat={:03.1f}&Bone={:03.1f}&Muscle={:03.1f}&Vfat={:03d}&Moisture={:03.1f}&Calorie={:04.0f}&Age={:02d}").format(
                  Weight, Height, Fat, Bone, Muscle, Vfat, Moisture, Calorie, Age)
        #print(url)
        r = requests.get(url) #, auth=('user', 'pass'))
        #print (r.status_code)
        #print (r.text)

        if Test: print (r)
        sleep(25) 
current_time = datetime.now()
print (str(current_time) + ' Finish')
print ("FINISH")

