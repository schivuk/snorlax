#!/usr/bin/env python
 
# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain
 
import time
import os
import requests
import RPi.GPIO as GPIO
import threading
import SocketServer
import json
import pygame

GPIO.setmode(GPIO.BCM)

DATA_SERVER_PORT = 9999
OFF_LABEL = 'off'
#time between logs
LOG_INTERVAL_SECS = 75.0/1000.0

#Period between alarm queries
ALARM_QUERY_INTERVAL_SECS = 30.
TARGET_HOST = "128.237.160.128:8000"

STORE_DATA_URL = "http://" + TARGET_HOST + "/storeData"

ONOFF_STORE_URL = "http://" + TARGET_HOST + "/storeOnOffData"
CHECK_ALARM_URL = "http://" + TARGET_HOST + "/isAlarmReady"
CHECK_ON_OFF = "http://" + TARGET_HOST + "/checkOnOff"
GET_POS_URL = "http://" + TARGET_HOST + "/getPosition"
CHECK_POS_URL = "http://" + TARGET_HOST + "/getPositionBuzz"

#Alarm sound file path
SOUND_FILE_PATH = 'alarm.wav'

#Buzzer sound file path (alert user for wrong sleeping positions)
BUZZER_FILE_PATH = 'buzzer.wav'

filename = '/home/pi/accOutput.txt'
 
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
            return -1
    GPIO.output(cspin, True)

    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here
    for i in range(5):
            if (commandout & 0x80):
                    GPIO.output(mosipin, True)
            else:
                    GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                    adcout |= 0x1

    GPIO.output(cspin, True)
    
    adcout >>= 1       # first bit is 'null' so drop it
    return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 14
SPIMISO = 15
SPIMOSI = 18
SPICS = 23

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
 

#out_file = open(filename, 'a')
num_reads = 0

#use SPI to get ADC data. Return value is a tuple of data strings
# 0-2: Accelerometer
# 3-6: xxxx
# 7: Mic
# 8 - 
def getSensorData():
    allVals = []
    microphoneVals, accelerometerVals, velostatVals = [],[],[]

    SPICLK = 14
    SPIMISO = 15
    SPIMOSI = 18
    SPICS = 23
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    
    for i in xrange(8):
        out = readadc(i, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #velostatVals.append(str(out))
        allVals.append(str(out))
    
    SPICLK = 24
    SPIMISO = 25
    SPIMOSI = 8
    SPICS = 7
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)

    for i in xrange(8):
        out = readadc(i, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #velostatVals.append(str(out))
        velostatVals.append(str(out))

    SPICLK = 12
    SPIMISO = 16
    SPIMOSI = 20
    SPICS = 21
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)

    for i in xrange(8):
        out = readadc(i, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #velostatVals.append(str(out))
        velostatVals.append(str(out))
    
    SPICLK = 6
    SPIMISO = 13
    SPIMOSI = 19
    SPICS = 26
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    
    for i in xrange(8):
        out = readadc(i, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #velostatVals.append(str(out))
        velostatVals.append(str(out))

    microphoneVals = str(readadc(7, SPICLK, SPIMOSI, SPIMISO, SPICS))
    accelerometerX = str(readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS))
    accelerometerY = str(readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS))
    accelerometerZ = str(readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS))
    accelerometerVals = accelerometerX + ',' + accelerometerY + ',' + accelerometerZ

    return velostatVals, microphoneVals, accelerometerVals



def logSensorData():
    velostatVals, microphoneVals, accelerometerVals = getSensorData()
    
    out_data = ','.join(velostatVals) + ',' + microphoneVals + ',' +\
                        accelerometerVals + ',' + str(time.time()) + '\n'

    print out_data
    #out_file.write(out_data)
    #if num_reads % 100 == 0:
    #    out_file.close()
    #out_file = open(filename, 'a')

    payload = {
        'velostatIDs': '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24',
        'velostatVals': ','.join(velostatVals),
        'accelerometerIDs': '1',
        'accelerometerVals': accelerometerVals,
        'microphoneIDs': '1',
        'microphoneVals': microphoneVals,
        'time': time.time()
        #'value': "{0},{1},{2},{3}".format(out0,out1,out2,time.time()),
    }
    
    try:
        requests.post(url=STORE_DATA_URL, data=payload)
    except:
        print "Exception occured during store data request"
    threading.Timer(LOG_INTERVAL_SECS, logSensorData).start()

def isOffBed():
    velostatVals, _, _ = getSensorData()
    
    out_data = ','.join(velostatVals) + ',' + microphoneVals + ',' +\
                        accelerometerVals + ',' + str(time.time()) + '\n'

    print out_data
   
    payload = {
        'velostatVals': ','.join(velostatVals),
    }
    
    try:
        requests.post(url=CHECK_ON_OFF, data=payload)
    except:
        print "Exception occured during checkOnOff"

    print "Got response: " + request.text
    return request.text == OFF_LABEL


def checkAlarmStatus():
    googleReq = requests.get("http://google.com")
    print "Google req'd. resp: ", googleReq.status_code
    alarmReq = requests.get(CHECK_ALARM_URL)

    print "alarm req'd"
    if alarmReq.status_code==200 and alarmReq.text=='True':
        #Start alarm. Play the alarm sound file
        pygame.mixer.init()
        pygame.mixer.music.load(SOUND_FILE_PATH)
        pygame.mixer.music.play(-1) #Play indefinitely, until user gets off bed
        

        while True:
            #Check if person is off the bed
            if isOffBed():
                pygame.mixer.music.stop()
                break    
            time.sleep(2)

    threading.Timer(ALARM_QUERY_INTERVAL_SECS, checkAlarmStatus).start()

def checkPositionBuzzer():
    googleReq = requests.get("http://google.com")
    print "Google req'd. resp: ", googleReq.status_code
    buzzerReq = requests.get(CHECK_POS_URL)

    velostatVals, _, _ = getSensorData()
    
    out_data = ','.join(velostatVals) + ',' + microphoneVals + ',' +\
                        accelerometerVals + ',' + str(time.time()) + '\n'

    print out_data
   
    payload = {
        'velostatVals': ','.join(velostatVals),
    }
    
    try:
        requests.post(url=GET_POS_URL, data=payload)
    except:
        print "Exception occured during checkOnOff"

    print "Got response: " + request.text

    buzzPositions = request.text.split(',')

    if buzzerReq.status_code==200 and buzzerReq.text in buzzPositions:
        #Start buzzer. Play the buzzer sound file
        pygame.mixer.init()
        pygame.mixer.music.load(BUZZER_FILE_PATH)
        pygame.mixer.music.play()       #Play once (Buzzer file should be 2 secs)

    threading.Timer(ALARM_QUERY_INTERVAL_SECS, checkPositionBuzzer).start()

#Configured so that on GET request, it returns a JSON containing sensor data
class DataServer(SocketServer.BaseRequestHandler):
    def handle(self):
        data=self.request.recv(1024)
        print "req:  ",data
        velostatVals, microphoneVals, accelerometerVals = getSensorData()
        sensorData = {"velostats": ','.join(velostatVals),\
                    "mic":microphoneVals,\
                    "acc":accelerometerVals}

        self.request.send(json.dumps(sensorData))

server = SocketServer.TCPServer(("0.0.0.0", DATA_SERVER_PORT), DataServer)

threading.Thread(target=logSensorData).start()
threading.Thread(target=server.serve_forever).start()
threading.Thread(target=checkAlarmStatus).start()
threading.Thread(target=checkPositionBuzzer).start()