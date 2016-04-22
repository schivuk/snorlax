#!/usr/bin/env python
 
# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain
 
import time
import os
import requests
import RPi.GPIO as GPIO
import threading
 
#time between 
LOG_INTERVAL_SECS = 50.0/1000.0

GPIO.setmode(GPIO.BCM)


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
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
 

out_file = open(filename, 'a')
num_reads = 0


def logSensorData():
    raw_input('Press any key to record and send data:\n')
    velostatVals = []
    SPICS = 25
    GPIO.setup(SPICS, GPIO.OUT)
    
    for i in xrange(8):
        out = readadc(i, SPICLK, SPIMOSI, SPIMISO, SPICS)
        velostatVals.append(str(out))
	
    SPICS = 19
    GPIO.setup(SPICS, GPIO.OUT)

    for i in xrange(8):
        out = readadc(i, SPICLK, SPIMOSI, SPIMISO, SPICS)
        velostatVals.append(str(out))

    SPICS = 26
    GPIO.setup(SPICS, GPIO.OUT)

    for i in xrange(8):
        out = readadc(i, SPICLK, SPIMOSI, SPIMISO, SPICS)
        velostatVals.append(str(out))

    num_reads += 1

    #print num_reads,out0,out1,out2,out3,out4,out5,out6,out7,time.time()

    #out_data = '{0},{1},{2},{3},{4},{5},{6},{7}.{8}\n'.format(
    #	out0,out1,out2,out3,out4,out5,out6,out7,time.time()
    #    )
    out_data = ','.join(velostatVals) + ',' + str(time.time()) + '\n'

    out_file.write(out_data)
    if num_reads % 100 == 0:
	out_file.close()
	out_file = open(filename, 'a')

    url = "http://128.237.186.149:8000/storeData"
    payload = {
        'velostatIDs': '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20',
        'velostatVals': ','.join(velostatVals),
        'time': time.time()
	#'value': "{0},{1},{2},{3}".format(out0,out1,out2,time.time()),
    }

    try:
	   requests.post(url=url, data=payload)
    except:
        continue

    #set timer for this function after LOG_INTERVAL_SECS
    threading.Timer(LOG_INTERVAL_SECS, logSensorData).start()
	
def pollAlarm():
    return True

logSensorData()
pollAlarm()
