#!/bin/python3
import sys
import signal
from time import sleep
from datetime import datetime
#import time
from bluetooth import BluetoothSocket, RFCOMM, BluetoothError
import requests

TEST = 1

#MyDevice = '00:18:12:22:01:3B'
#MyDevice = '00:18:12:22:01:19'
MY_DEVICE = '00:18:12:51:81:07'
#MyDevice = '00:18:12:51:81:17'
#MyDevice = 'CC:B1:1A:01:41:C5'
#MyDevice = '00:18:12:22:01:26' smidt ud

DB_HOST = "http://motion.holmnet.dk/"


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

print("Weight starting " + str(current_time))

# initialization
signal.signal(signal.SIGTERM, receive_signal)
signal.signal(signal.SIGINT, receive_signal)

while True:
    FOUND = True

########################################################

    print("Connecting to device")

    CONNECTED = False
    while not CONNECTED:
        try:
            if TEST:
                print("connecting...")
            client = BluetoothSocket(RFCOMM)
            client.connect((MY_DEVICE, 1))
        except IOError as ex:
            if TEST:
                print("unable to connect:" + str(ex))
                print("Sleeping..")
                sys.stdout.flush()
            sleep(5)
        except Exception as ex:
            print('Connected exception: ' + str(ex))
        else:
            CONNECTED = True
    current_time = datetime.now()
    print (str(current_time) + ' connected')

#################################################

    Message = bytearray([])
    COUNT = 0
    sys.stdout.write("receiving.. ")
    while COUNT<21:
        try:
            data = client.recv(21-COUNT)
            if not data:
                print("Not data")
                break
            if TEST:
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
        except Exception as ex:
            print ("Exception: " + str(ex) + str(type(ex)))
            break
    client.close()

    print("")

    if COUNT>=21:
        if TEST:
            print("Decoding")
        YEAR=Message[0]*256+Message[1]
        YEAR=2024
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
        if TEST:
            print(f"Fat {Fat:2.1f} %% Bone {Bone:2.1f} kg Muscle {Muscle:2.1f} kg Vfat {Vfat:3d} Moist {Moisture:2.1f} %% Cal {Calorie:3d}")

        # DateTime = "{:04d}-{:02d}-{:02d}%20{:02d}:{:02d}:{:02d}".format(YEAR, Month, Day, Hour, Min, Sec)
        # Date = "{:4d}-{:02d}-{:02d}".format(YEAR, Month, Day)
        DateTime = f"{YEAR:04d}-{Month:02d}-{Day:02d}%20{Hour:02d}:{Min:02d}:{Sec:02d}"
        Date = f"{YEAR:4d}-{Month:02d}-{Day:02d}"
        if TEST:
            print(DateTime)

        with open('data.csv', 'a', encoding="UTF-8") as fp:
            # fp.write("%04d-%02d-%02d %02d:%02d:%02d," % (YEAR, Month, Day, Hour, Min, Sec))
            # fp.write("%2.1f, %2.1f, %2.1f," % (Weight, Fat, Bone))
            # fp.write("%2.1f, %3d, %2.1f, %3d \n" % (Muscle, Vfat, Moisture, Calorie))
            fp.write(DateTime)
            fp.write(f"{Weight:2.1f}, {Fat:2.1f}, {Bone:2.1f},")
            fp.write(f"{Muscle:2.1f}, {Vfat:3d}, {Moisture:2.1f}, {Calorie:3d}\n")
            #fp.close()

        url= (DB_HOST +"motion/save.php?save&DateTime="+DateTime+"&Date="+Date+ \
              "&Weight={:03.1f}&Height={:03d}&Fat={:03.1f}&Bone={:03.1f}&Muscle={:03.1f}&Vfat={:03d}&Moisture={:03.1f}&Calorie={:04.0f}&Age={:02d}").format(
                  Weight, Height, Fat, Bone, Muscle, Vfat, Moisture, Calorie, Age)
        #print(url)
        r = requests.get(url, timeout=10) #, auth=('user', 'pass'))
        #print (r.status_code)
        #print (r.text)

        if TEST:
            print (r)
        sleep(25)
current_time = datetime.now()
print (str(current_time) + ' Finish')
print ("FINISH")
