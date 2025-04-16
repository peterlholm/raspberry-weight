#!/bin/python3
import sys
import signal
from time import sleep
from datetime import datetime
#import time
from bluetooth import BluetoothSocket, RFCOMM, BluetoothError
import requests

SEND_SMALL_MESSAGES = False

_DEBUG = False

MY_DEVICE = '00:18:12:51:81:07'
#MyDevice = '00:18:12:22:01:3B'
#MyDevice = '00:18:12:22:01:19'
#MyDevice = 'CC:B1:1A:01:41:C5'

DB_HOST = "http://holmnet.dk/"

def receive_signal(signal_number, frame):
    "signal handling"
    if signal_number ==signal.SIGINT:
        print("Received SIGINT - terminating")
        sys.exit(0)
    elif signal_number==signal.SIGTERM:
        print("Receiving signal", signal.SIGTERM, " - Terminating")
        sys.exit(0)
    else:
        print(f'Received Signal: {signal_number} {frame}')
        sys.exit(signal_number)

current_time = datetime.now()

print(str(datetime.now()), "Weight starting " + str(current_time))

# initialization
signal.signal(signal.SIGTERM, receive_signal)
signal.signal(signal.SIGINT, receive_signal)

while True:
    FOUND = True

########################################################

    print(str(datetime.now()), "Connecting to device:", MY_DEVICE)

    CONNECTED = False
    while not CONNECTED:
        try:
            if _DEBUG:
                print(str(datetime.now()),"connecting...")
            client = BluetoothSocket(RFCOMM)
            client.connect((MY_DEVICE, 1))
        except IOError as ex:
            if _DEBUG:
                print(str(datetime.now()),"unable to connect:" + str(ex))
                print(str(datetime.now()),"Sleeping..")
                sys.stdout.flush()
            sleep(5)
        except Exception as ex:     # pylint: disable=broad-except
            print(str(datetime.now()),'Error: Connected exception: ' + str(ex))
        else:
            CONNECTED = True
    current_time = datetime.now()
    print (str(current_time),'Connected')

#################################################

    Message = bytearray([])
    COUNT = 0
    sys.stdout.write(str(datetime.now()) + " Receiving.. ")
    while COUNT<21:
        try:
            data = client.recv(21-COUNT)
            if not data:
                print("Not data")
                break
            if _DEBUG:
                sys.stdout.write('.')
            Message += data
            COUNT += len(data)
        except BluetoothError as ex:
            print ("Exception  BlueToothError: " + str(ex) )
            break
        except IOError as ex:
            print ("Exception  IOerror: " + str(ex) + str(type(ex)))
            #print ("I/O error({0}): {1}".format(ex.errno, ex.strerror))
            print(f"I/O error({ex.errno}):{ex.strerror}")
            #print(ex.message)
            print(ex)
            print ('vars')
            print(vars(ex))
            print ('dir')
            break
        except Exception as ex:     # pylint: disable=broad-except
            print ("Exception: " + str(ex) + str(type(ex)))
            break
    client.close()

    print("")

    if COUNT>=21:
        if _DEBUG:
            print("Decoding")
        YEAR=Message[0]*256+Message[1]
        if _DEBUG:
            print(f"{YEAR}, {Message[0]}, {Message[0]}" )
        YEAR=2025
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

        print(f"Weight: {Weight:2.1f} kg")
        if _DEBUG:
            print(f"Age: {Age}, Height: {Height}")
            print(f"Fat {Fat:2.1f} % Bone {Bone:2.1f} kg Muscle {Muscle:2.1f} kg Vfat {Vfat:3d} Moist {Moisture:2.1f} % Cal {Calorie:3d}")

        # DateTime = "{:04d}-{:02d}-{:02d}%20{:02d}:{:02d}:{:02d}".format(YEAR, Month, Day, Hour, Min, Sec)
        # Date = "{:4d}-{:02d}-{:02d}".format(YEAR, Month, Day)
        DateTime = f"{YEAR:04d}-{Month:02d}-{Day:02d} {Hour:02d}:{Min:02d}:{Sec:02d}"
        Date = f"{YEAR:4d}-{Month:02d}-{Day:02d}"
        if _DEBUG:
            print(DateTime)

        with open('data.csv', 'a', encoding="UTF-8") as fp:
            # fp.write("%04d-%02d-%02d %02d:%02d:%02d," % (YEAR, Month, Day, Hour, Min, Sec))
            # fp.write("%2.1f, %2.1f, %2.1f," % (Weight, Fat, Bone))
            # fp.write("%2.1f, %3d, %2.1f, %3d \n" % (Muscle, Vfat, Moisture, Calorie))
            fp.write(DateTime)
            fp.write(f" {Age}, {Height}, ")
            fp.write(f"{Weight:2.1f}, {Fat:2.1f}, {Bone:2.1f},")
            fp.write(f"{Muscle:2.1f}, {Vfat:3d}, {Moisture:2.1f}, {Calorie:3d}\n")
            #fp.close()

        if Fat > 0.1 or SEND_SMALL_MESSAGES:
            # send message
            url= (DB_HOST +"motion/save.php?save&DateTime="+DateTime+"&Date="+Date+ \
                "&Weight={:03.1f}&Height={:03d}&Fat={:03.1f}&Bone={:03.1f}&Muscle={:03.1f}&Vfat={:03d}&Moisture={:03.1f}&Calorie={:04.0f}&Age={:02d}").format(
                    Weight, Height, Fat, Bone, Muscle, Vfat, Moisture, Calorie, Age)
            #print(url)
            r = requests.get(url, timeout=10) #, auth=('user', 'pass'))
            #print (r.status_code)
            #print (r.text)
            if _DEBUG:
                print (r)
        else:
            if _DEBUG:
                print("skipping message")
        sleep(25)
current_time = datetime.now()
print (str(current_time) + ' Finish')
print ("FINISH")
