#!/usr/bin/env python
 
# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain
 
import time
import os
import requests
import RPi.GPIO as GPIO

#time.sleep(10)

GPIO.setmode(GPIO.BCM)

TARGET_HOST = "128.237.168.133:8000"

filename = '/home/pi/accOutput.txt'
TRAIN_URL = "http://" + TARGET_HOST + "/trainPosition"
LEARN_URL = "http://" + TARGET_HOST + "/learnPositions"
PREDICT_URL = "http://" + TARGET_HOST + "/getPosition"
DELETE_URL = "http://" + TARGET_HOST + "/clearAll"

NUM_TRAIN_SAMPLES = 10

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

#Delete all prior data

print "Deleting data..."
try:
    r = requests.post(url=DELETE_URL, data={})
except Exception as e:
    print "Exception sending request:"
    print e

print "done"


while True:
    for i in xrange(NUM_TRAIN_SAMPLES):
        currLabel = raw_input('Enter label to train for:\n')
        velostatVals = []
        SPICS = 25
        GPIO.setup(SPICS, GPIO.OUT)
        
        for i in xrange(8):
            out = readadc(i, SPICLK, SPIMOSI, SPIMISO, SPICS)
            velostatVals.append(str(out))
        #out1 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out2 = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out3 = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out4 = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out5 = readadc(4, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out6 = readadc(5, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out7 = readadc(6, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out8 = readadc(7, SPICLK, SPIMOSI, SPIMISO, SPICS)
            
        SPICS = 19
        GPIO.setup(SPICS, GPIO.OUT)

        for i in xrange(8):
            out = readadc(i, SPICLK, SPIMOSI, SPIMISO, SPICS)
            velostatVals.append(str(out))
        #out9 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out10 = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out11 = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out12 = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out13 = readadc(4, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out14 = readadc(5, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out15 = readadc(6, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out16 = readadc(7, SPICLK, SPIMOSI, SPIMISO, SPICS)

        SPICS = 26
        GPIO.setup(SPICS, GPIO.OUT)

        for i in xrange(8):
            out = readadc(i, SPICLK, SPIMOSI, SPIMISO, SPICS)
            velostatVals.append(str(out))
        #out17 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out18 = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out19 = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out20 = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out21 = readadc(4, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out22 = readadc(5, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out23 = readadc(6, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #out24 = readadc(7, SPICLK, SPIMOSI, SPIMISO, SPICS)

        num_reads += 1

        #print num_reads,out0,out1,out2,out3,out4,out5,out6,out7,time.time()

        #out_data = '{0},{1},{2},{3},{4},{5},{6},{7}.{8}\n'.format(
        #	out0,out1,out2,out3,out4,out5,out6,out7,time.time()
        #   )
        out_data = ','.join(velostatVals) + ',' + str(time.time()) + '\n'

        out_file.write(out_data)
        if num_reads % 100 == 0:
            out_file.close()
            out_file = open(filename, 'a')

        url = TRAIN_URL
        payload = {
            'velostatIDs': '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20',
            'velostatVals': ','.join(velostatVals),
            'time': time.time(),
            'label': currLabel
            #'value': "{0},{1},{2},{3}".format(out0,out1,out2,time.time()),
        }

        print "Sending request"
        try:
            r = requests.post(url=url, data=payload)
            print "*"*50 + "\n\n" + r.text + "\n\n" + "*"*50
        except Exception as e:
            print "Exception sending request:"
            print e
            continue
        
        print "done"

        time.sleep(50.0/1000.0)
        #time.sleep(75.0/1000.0)
    try:
        r = requests.post(url=LEARN_URL, data=payload)
        print r.text + "\n\n"
    except Exception as e:
        print "Exception sending learn request:"
        print e
    
    print "Done training. Beginning prediction. Press <enter> to predict current position, enter 'end' to end this session"

    while True:
        inp = raw_input()

        if inp == 'end':
            break
        
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


        out_data = ','.join(velostatVals) + ',' + str(time.time()) + '\n'
        
        payload = {
            'velostatIDs': '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20',
            'velostatVals': ','.join(velostatVals),
            'time': time.time(),
        }

        print "Sending PREDICT request"
        try:
            r = requests.post(url=PREDICT_URL, data=payload)
            print "\n\n" + r.text + "\n\n"
        except Exception as e:
            print "Exception:"
            print e
            continue
        print "done"

        time.sleep(50.0/1000.0)


