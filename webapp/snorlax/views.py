from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, Http404, JsonResponse

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

from snorlax.models import *

import datetime
from django.utils.timezone import utc
from django.core import serializers
import json
from django.utils import timezone

#for classification
import numpy as np
from sklearn.svm import SVC
from sklearn.utils.validation import NotFittedError

from algorithm import *
import time
import os
import requests
import urllib2
import socket

clf = SVC(C=10, kernel='poly', degree=1, probability=True)
onBedClf = SVC(C=10, kernel='poly', degree=1, probability=True)

colors = []

#True only while debugging alarm
DEBUG_ALARM = False
ON_LABEL = 'on'
OFF_LABEL = 'off'
RPI_SERVER_HOST = "http://128.237.233.205:9999"
RPI_GET_URL = RPI_SERVER_HOST + "/getdata"
ON_OFF_TRAIN_FILE = 'on-off-train.txt'
POSITION_TRAIN_FILE = 'train-position-data.txt'
POSITION_TEST_FILE = 'test-position-data.txt'
MAX_VALUES = 50

context_cache = {}

def home(request):
    return render(request, 'snorlax/dashboard.html')

def base(request):
    return render(request, 'snorlax/base.html')

@transaction.atomic
def alarm(request):
    if request.method == 'GET':
        context = {}

        #Get the last alarm set
        alarms =Alarm.objects.all()
        if len(alarms) > 0:
            context['alarm'] = alarms[0]

        return render(request, 'snorlax/alarm.html', context)

    if request.method == 'POST':
        context = {}

        #Get the last alarm set
        alarms = Alarm.objects.all()
        if len(alarms) > 0:
            alarm = alarms[0]
            if request.POST['isOn'] == 'true':
                alarm.switch = True
            elif request.POST['isOn'] =='false':
                alarm.switch = False
            print alarm.switch
            alarm.save()
            context['alarm'] = alarm

        # return render(request, 'snorlax/alarm.html', context)
        return HttpResponse("Success", status=200)

def logSleepForm(request):
    if request.method == 'GET':
        print request.GET
        if request.GET['date'] == 'test':
            time = timezone.now()
            day = time.day
            month = time.month
            year = time.year
        else:
            date = request.GET['date'].split('-')
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        try:
            logSleep = LogSleep.objects.get(day__exact=day, month__exact=month, year__exact=year)
            context = {}
            print logSleep.dreams
            context['quality'] = logSleep.quality
            context['dreams'] = logSleep.dreams
            context['description'] = logSleep.description
            context['day'] = logSleep.day
            context['month'] = logSleep.month
            context['year'] = logSleep.year
            return JsonResponse(context)
        except LogSleep.DoesNotExist:
            context = {}
            return JsonResponse(context)

@transaction.atomic
def feedback(request):
    if request.method == 'GET':
        if 'date' not in request.GET or request.GET['date'] == 'test':
            time = timezone.now()
            day = time.day
            month = time.month
            year = time.year
        else:
            date = request.GET['date'].split('-')
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        try:
            logSleep = LogSleep.objects.get(day__exact=day, month__exact=month, year__exact=year)
            context = {}
            context['log'] = logSleep
            return render(request, 'snorlax/feedback.html', context)
        except LogSleep.DoesNotExist:
            return render(request, 'snorlax/feedback.html')

    if request.method == 'POST':
        context = {}

        quality = request.POST['quality']
        dream = request.POST['dreams']
        haveDream = False
        if dream == 'True':
            haveDream = True
        elif dream == 'False':
            haveDream = False
        else:
            print 'The was a problem'

        description = request.POST['description']
        if request.POST['date'] == 'test':
            time = timezone.now()
            day = time.day
            month = time.month
            year = time.year
        else:
            date = request.POST['date'].split('-')
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])

        #Log the sleep for the input date
        #Check if a log for that date already exists
        try:
            logSleep = LogSleep.objects.get(day__exact=day, month__exact=month, year__exact=year)
            logSleep.quality = quality;
            logSleep.dreams = haveDream;
            logSleep.description = description;
            print haveDream
            logSleep.save()
            #Update context with the data
            #Populate the html page with the data
            context['log'] = logSleep
            return render(request, 'snorlax/feedback.html', context)
        except LogSleep.DoesNotExist:
            logSleep = LogSleep(day=day, year=year, month=month, quality=quality, dreams=haveDream, description=description)
            logSleep.save()
            #Update context with the data
            #Populate the html page with the data
            context['log'] = logSleep
            return render(request, 'snorlax/feedback.html', context)

def profile(request):
    if request.method == 'GET':
        return render(request, 'snorlax/profile.html')

def isAlarmReady(request):
    isReady = False
    if request.method == 'GET':
        #Check whether alarm has been set previously
        alarms = Alarm.objects.all()
        if len(alarms) > 0:
            alarm = alarms[0]
            currTime = timezone.now() - timezone.timedelta(hours=4)

            print "currTime, alarm.time: ",currTime,",",alarm.time
            #Check if alarm was switched on
            if alarm.switch:
                #Check if alarm time has been reached and hasn't happened yet
                print "currTime >= alarm.time, alarm.yetToHappen: ",\
                                    currTime >= alarm.time, alarm.yetToHappen
                if DEBUG_ALARM or (currTime >= alarm.time and alarm.yetToHappen):
                    isReady = True
                    #set to 'happened'
                    alarm.yetToHappen = False
                    alarm.save()
                else:
                    isReady = False
        else:
            #no alarm has been set
            isReady=False

        #return HttpResponse("Success", status=200)
        return HttpResponse(str(isReady))
    else:
        raise Http404

@transaction.atomic
def editAlarm(request):
    if request.method != 'POST':
        raise Http404

    context = {}

    ampm = request.POST['ampm']
    hour = int(request.POST['hour'])
    minute = int(request.POST['min'])
    if ampm == 'PM':
        hour = hour + 12

    time = timezone.now()
    time = time.replace(hour=hour, minute=minute)

    #Check whether alarm has been set previously
    alarms = Alarm.objects.all()
    if len(alarms) > 0:
        alarm = alarms[0]
        alarm.time = time
        alarm.yetToHappen = True
        alarm.save()
    else:
        alarm = Alarm(time=time)
        alarm.save()

    context['alarm'] = alarm

    return render(request, 'snorlax/alarm.html', context)

#get current sensor values from bed
def logCurrOnOffData(request, label=''):
    try:
        dataResp = urllib2.urlopen(RPI_GET_URL, timeout=7)
    except requests.exceptions.ConnectionError:
        print "Exception occurred"
        return HttpResponse("Failure", status=200)
    except urllib2.URLError:
        print "URLError"
        return HttpResponse("URL Error", status=200)
    except socket.timeout:
        print "Timeout occurred"
        return HttpResponse("Timeout", status=200)

    sensorData = json.loads(dataResp.read())
    print "Success. Got response: ",sensorData

    storeVelostatInfo(veloStr=sensorData['velostats'].strip(), label=label,\
        newOnOffGroup=True, newRGroup=False, fileName=ON_OFF_TRAIN_FILE,\
        logThreshold=False)

    learnOnOffClf()

    return HttpResponse("Success",status=200)


#gets the sensor data from the RPi, and logs it as on/off
def storeOnOffData(request):
    if request.method != 'POST':
        raise Http404

    velostatValsStr = request.POST['velostatVals']
    onOffLbl = request.POST['label']

    if not os.path.isfile(ON_OFF_TRAIN_FILE):
        #create file
        trainFile = open(ON_OFF_TRAIN_FILE, 'w+')
    else:
        #append to file
        trainFile = open(ON_OFF_TRAIN_FILE, 'a')

    trainDataStr = onOffLbl + ":" + velostatValsStr.strip()
    trainFile.write(trainDataStr)
    trainFile.close()
    print "Wrote to file: " + trainDataStr
    return HttpResponse("Success", status=200)


#Store position data
@transaction.atomic
def storeData(request):
    filename = 'accOutput2016-04-30Small.txt'

    if request.method != 'POST':
        raise Http404

    velostatVals = str(request.POST['velostatVals']).split(',')
    velostatIDs = str(request.POST['velostatIDs']).split(',')
    accelerometerVals = str(request.POST['accelerometerVals']).split(',')
    accelerometerIDs = str(request.POST['accelerometerIDs']).split(',')
    # microphoneVals = str(request.POST['microphoneVals']).split(',')
    # microphoneIDs = str(request.POST['microphoneIDs']).split(',')
    time = float(request.POST['time'])

    timestamp = Time(time=datetime.datetime.fromtimestamp(time))

    out_data = str(request.POST['accelerometerVals']) + ',' + str(request.POST['velostatVals']) + ',' + str(time) + '\n'
    out_file = open(filename, 'a')
    out_file.write(out_data)
    out_file.close()

    # timestamp.save()

    # for i in xrange(len(velostatIDs)):
    #     velostatData = VelostatData(sensorId=velostatIDs[i], value=velostatVals[i])
    #     velostatData.save()
    #     timestamp.velostats.add(velostatData)

    # for i in xrange(len(accelerometerIDs)):
    #     accelerometerData = AccelerometerData(sensorId=accelerometerIDs[i],
    #                                           xValue=accelerometerVals[3*i],
    #                                           yValue=accelerometerVals[3*i+1],
    #                                           zValue=accelerometerVals[3*i+2])
    #     accelerometerData.save()
    #     timestamp.accelerometers.add(accelerometerData)

    # for i in xrange(len(microphoneIDs)):
    #     microphoneData = MicrophoneData(sensorId=microphoneIDs[i], value=microphoneVals[i])
    #     microphoneData.save()
    #     timestamp.microphones.add(microphoneData)

    # timestamp.save()

    return HttpResponse("Success", status=200)

#resets classifier
def resetTraining(request):
    clf = SVC(C=10, kernel='poly', degree=1, probability=True)
    ReadingGroup.objects.all().delete()
    return HttpResponse("Success", status=200)

#render the page with training options
def trainOptions(request):
    return render(request, 'snorlax/train.html', {} )

#query RPi for current position, then train for the specified label
def trainCurrentPosition(request,label=''):

    print "Sending request to RPI_URL"
    try:
        dataResp = urllib2.urlopen(RPI_GET_URL, timeout=7)
    except requests.exceptions.ConnectionError:
        print "Exception occurred"
        return HttpResponse("Failure", status=200)
    except urllib2.URLError:
        print "URLError"
        return HttpResponse("URL Error", status=200)
    except socket.timeout:
        print "Timeout occurred"
        return HttpResponse("Timeout", status=200)

    #read response as JSON
    sensorData = json.loads(dataResp.read())
    print "Success. Got response: ",sensorData

    storeVelostatInfo(veloStr=sensorData['velostats'].strip(), label=label,\
        newOnOffGroup=False, newRGroup=True, fileName=POSITION_TRAIN_FILE,\
        logThreshold=False)

    return HttpResponse("Success",status=200)



#helper function to store velostat information from a comma-separated string,
#returning an array of raw integer values
#newOnOffGroup: boolean specifying whether new OnOffGroup needs to be created
#newRGroup: boolean specifying whether new ReadingGroup needs to be created
#logThreshold: boolean specifying if current dataset should be logged as the
#              threshold value
def storeVelostatInfo(veloStr, label='', newOnOffGroup=False, newRGroup=False, \
            fileName='', logThreshold=False):
    velostatValsStr = veloStr.split(',')

    print "velo values: " + str(velostatValsStr)
    veloVals = map(int, velostatValsStr)

    #create new OnOffGroup if specified
    if newOnOffGroup:
        onOffGroup = OnOffGroup(label=label)
        onOffGroup.save()
    else:
        onOffGroup=None

    #create new ReadingGroup if specified
    if newRGroup:
        rgroup = ReadingGroup(label=label)
        rgroup.save()
    else:
        rgroup=None

    #alway create new LogGroup
    logGroup = LogGroup()
    logGroup.save()

    index=0
    for veloVal in veloVals:
        index += 1
        reading = SensorReading(value=veloVal, onOffGroup=onOffGroup, rgroup=rgroup,\
                                logGroup=logGroup, index=index)
        reading.save()

    #If specified, log as threshold
    if logThreshold:
        thresholdRef = ThresholdRef(logGroup=logGroup)
        thresholdRef.save()

    if fileName:
        #write information to file
        if not os.path.isfile(fileName):
            #create file
            trainFile = open(fileName, 'w+')
        else:
            #append to file
            trainFile = open(fileName, 'a')

        trainFile.write(label + ":" + veloStr.strip())
        trainFile.close()

#check if the current position (IE request.POST['velostatVals']) classifies as
#ON or OFF
def checkOnOff(request):
    print "Called checkOnOff"
    if request.method != 'POST':
        raise Http404

    print "checkOnOff called; velostatVals: ",request.POST['velostatVals']
    veloVals = map(int,request.POST['velostatVals'].split(","))

    print "estimating on/off..."

    try:
        onOffEstArr = onBedClf.predict([veloVals])
        print "Estimated onoff: ",onOffEstArr[0]
        return HttpResponse(onOffEstArr[0], status=200)

    except NotFittedError:
        #on off has not yet been calibrated
        print "got NotFittedError at onBedClf"
        return HttpResponse("Error: Classifier not updated.",status=200)


def trainPosition(request):
    print "Called trainPosition"
    if request.method != 'POST':
        raise Http404

    storeVelostatInfo(veloStr=request.POST['velostatVals'], \
        label=request.POST['label'],newOnOffGroup=False, newRGroup=True, \
            fileName=POSITION_TRAIN_FILE, logThreshold=False)

    return HttpResponse("Success", status=200)


def normalize(veloVals):
    allThresObjs = ThresholdRef.objects.all()
    if len(allThresObjs) == 0:
        return veloVals #nothing to be done

    lgp = allThresObjs[0].logGroup

    thresholdValsObj = SensorReading.objects.filter(logGroup=lgp).order_by('index')
    thresVals = map(lambda obj : obj.value , thresholdValsObj)

    normalizedVals = []
    for i in xrange(len(veloVals)):
        normalizedVals.append(veloVals[i] - thresVals[i])

    return normalizedVals

#train classifier based on all data
def learnPositions(request):
    print "Called learnPositions"
    xVector = []
    labelVector = []

    for rgroup in ReadingGroup.objects.all():
        veloValsStr = SensorReading.objects.filter(rgroup=rgroup).order_by('index')
        rawVeloVals = map(lambda obj : obj.value , veloValsStr)

        normalVeloVals = normalize(rawVeloVals)
        xVector.append(normalVeloVals)
        labelVector.append(rgroup.label)

    print "xvector: " + str(xVector)
    print "len(xVector): " + str(len(xVector))
    print "training for labels: " + str(labelVector)
    print "len(labelVector): " + str(len(labelVector))
    #learn

    try:
        clf.fit(np.array(xVector), np.array(labelVector))
    except ValueError:
        return HttpResponse("Need at least one sample of each position for calibration.")
    print "done."
    return HttpResponse("Success", status=200)

#for Pi chart showing ratio of sleeping positions
def getPositionRatios(request):
    #TODO only get logs from last night
    lgroups = LogGroup.objects.all()
    labels = map(lambda lg:lg.estLabel, lgroups)
    labelCounts = {}
    for lbl in labels:
        if lbl in labelCounts:
            labelCounts[lbl] += 1
        else:
            labelCounts[lbl] = 1

    return json.dumps(labelCounts)


def getNumReadingGroups(request):
    numGroups = len(ReadingGroup.objects.all())
    return HttpResponse(str(numGroups), status=200)


def getNumOnOffGroups(request):
    numGroups = len(OnOffGroup.objects.all())
    return HttpResponse(str(numGroups), status=200)

#get current velostat data from RPi, log it as threshold (base values)
def logCurrentAsThreshold(request):
    try:
        dataResp = urllib2.urlopen(RPI_GET_URL, timeout=7)
    except requests.exceptions.ConnectionError:
        print "Exception occurred"
        return HttpResponse("Failure", status=200)
    except urllib2.URLError:
        print "URLError"
        return HttpResponse("URL Error", status=200)
    except socket.timeout:
        print "Timeout occurred"
        return HttpResponse("Timeout", status=200)

    sensorData = json.loads(dataResp.read())
    print "Success. Got response: ",sensorData

    veloVals = map(int,sensorData['velostats'].split(","))


    ThresholdRef.objects.all().delete()
    storeVelostatInfo(veloStr=sensorData['velostats'].strip(),\
        label='', newOnOffGroup=False, newRGroup=False, fileName='',\
        logThreshold=True)

    return HttpResponse("Success", status=200)


def logToFile(fileName, text):
    if not os.path.isfile(fileName):
        #create file
        testFile = open(fileName, 'w+')
    else:
        #append to file
        testFile = open(fileName, 'a')

    testFile.write(text)
    testFile.close()

def getCurrentPosition(request):
    try:
        dataResp = urllib2.urlopen(RPI_GET_URL, timeout=7)
    except requests.exceptions.ConnectionError:
        print "Exception occurred"
        return HttpResponse("Failure", status=200)
    except urllib2.URLError:
        print "URLError"
        return HttpResponse("URL Error", status=200)
    except socket.timeout:
        print "Timeout occurred"
        return HttpResponse("Timeout", status=200)

    sensorData = json.loads(dataResp.read())
    print "Success. Got response: ",sensorData

    veloVals = map(int,sensorData['velostats'].split(","))

    storeVelostatInfo(veloStr=sensorData['velostats'].strip(),\
        label='', newOnOffGroup=False, newRGroup=False, fileName='',\
        logThreshold=False)

    print "Writing to test file..."

    logToFile(POSITION_TEST_FILE, sensorData['velostats'] + "\n")

    try:
        onOffEstArr = onBedClf.predict([veloVals])
        #check for position only if on the bed
        print "Estimated onoff: ",onOffEstArr[0]
        checkPosition = onOffEstArr[0] == ON_LABEL

    except NotFittedError:
        #on off has not yet been calibrated
        print "got NotFittedError at onBedClf"
        checkPosition = True

    if not checkPosition:
        return HttpResponse(OFF_LABEL, status=200)

    #position needs to be checked
    try:
        print "Checking position..."
        estimateArr = clf.predict([veloVals])
    except NotFittedError:
        print "NotFittedError occurred on position clf"
        return HttpResponse("Position tracker needs to be calibrated at least once!")

    print "Estimate: " + str(estimateArr[0])
    return HttpResponse(estimateArr[0])



def getPosition(request):
    if request.method != 'POST':
        raise Http404

    velostatValsStr = request.POST['velostatVals'].split(',')

    veloVals = map(int, velostatValsStr)
    print "velo values: " + str(veloVals)

    storeVelostatInfo(veloStr=request.POST['velostatVals'].strip(),\
        label='', newOnOffGroup=False, newRGroup=False, fileName='',\
        logThreshold=False)

    print "estimating values..."
    try:
        estimateArr = clf.predict([veloVals])
    except NotFittedError:
        return HttpResponse("Not yet trained", status=200)
    print "Estimate: " + str(estimateArr[0])
    return HttpResponse(estimateArr[0], status=200)


def clearAllOnOff(request):
    #delete all records

    for oog in OnOffGroup.objects.all():
        SensorReading.objects.filter(onOffGroup=oog).delete()

    OnOffGroup.objects.all().delete();
    #reset classifier
    onBedClf = SVC(C=10, kernel='poly', degree=1, probability=True)
    return HttpResponse("Success", status=200)

#delete all training data (to start a new session)
def clearAll(request):

    #SensorReading.objects.all().delete()
    ReadingGroup.objects.all().delete()
    #reset classifier
    clf = SVC(C=10, kernel='poly', degree=1, probability=True)
    print "All objects (not really) deleted"
    return HttpResponse("Success", status=200)


#show a template with a chart with data
def showRawData(request):
    return render(request, 'snorlax/rawdata.html', {})

#JSON response for AJAX calls
def getLatestReading(request):
    orderedGroups = LogGroup.objects.all().order_by('-time')

    if len(orderedGroups) < 1:
        print "no data available for reading groups"
        #no data available
        return  HttpResponse(serializers.serialize('json', {}),\
                                        content_type='application/json')

    firstGroup = orderedGroups[0]
    latestReadings = map(lambda sr : sr.value, \
        SensorReading.objects.filter(logGroup=firstGroup).order_by('index'))
    response_text = json.dumps(latestReadings)
    return HttpResponse(response_text, content_type='application/json')

    return render(request, 'snorlax/rawdata.html', {})


def analyzeSleepCycle(request):

    filename = str('accOutput' + request.GET['date'] + 'Small.txt')

    if os.path.isfile(filename) == False:
        context = {}
        context['file_exists'] = False
        return JsonResponse(context)

    if filename in context_cache and filename != 'accOutput2016-04-30Small.txt':
        return JsonResponse(context_cache[filename])

    posDict = {}
    with open(filename) as f:
        x_vals = []
        y_vals = []
        z_vals = []
        timestamps = []

        context = {}

        for line in f.readlines():
            data = line.strip('\n').split(',')
            veloVals = map(int, data[8:32])

            try:
                estimateArr = clf.predict([veloVals])
                lbl = estimateArr[0]
                if lbl in posDict:

                    posDict[lbl] +=1
                else:
                    posDict[lbl] = 1

            except NotFittedError:
                #return HttpResponse("Not yet trained", status=200)
                1+1

            x = data[0]
            y = data[1]
            z = data[2]
            timestamp = data[32]

            x_vals.append(int(x))
            # y_vals.append(int(y))
            # z_vals.append(int(z))
            timestamps.append(float(timestamp))

        total_count = sum(posDict.values())
        context['position_front'] = float(posDict.get('front',0)) / total_count
        context['position_back'] = float(posDict.get('back',0)) / total_count
        context['position_right'] = float(posDict.get('right',0)) / total_count
        context['position_left'] = float(posDict.get('left',0)) / total_count

        int_timestamps = range(0,len(x_vals))
        x_peaks, x_restful_indices = acc_algorithm(x_vals,timestamps)
        x_nonrestful_indices = set(int_timestamps).difference(x_restful_indices)

        total_nonrestful_time = 0
        total_restful_time = 0

        nonrestful_to_restful_transitions = []
        restful_to_nonrestful_transitions = []

        all_transitions = [timestamps[0]]
        y_axis = [1]
        curr_state = 'nonrestful'

        x_nonrestful_indices = set(x_nonrestful_indices)
        x_restful_indices = set(x_restful_indices)

        for i in xrange(2,len(x_vals)):
            if i-1 in x_nonrestful_indices and i in x_restful_indices:
                # light_to_deep_transitions.append(timestamps[i])
                nonrestful_to_restful_transitions.append(timestamps[i])
                all_transitions.append(timestamps[i])
                y_axis.append(2)
                curr_state = 'restful'
            elif i-1 in x_restful_indices and i in x_nonrestful_indices:
                restful_to_nonrestful_transitions.append(timestamps[i])
                all_transitions.append(timestamps[i])
                y_axis.append(1)
                curr_state = 'nonrestful'

            if curr_state == 'nonrestful':
                total_nonrestful_time += 1
            elif curr_state == 'restful':
                total_restful_time += 1

        # No transition at the end of the sleep cycle but we still need to graph it
        all_transitions.append(timestamps[-1])
        if curr_state == 'nonrestful':
            y_axis.append(1)
        elif curr_state == 'restful':
            y_axis.append(2)

    even_y_axis = []
    even_transitions = []

    for i in xrange(1, len(all_transitions)):
        for j in xrange(int(all_transitions[i-1]),int(all_transitions[i])):
            if j % 50 == 0:
                even_y_axis.append(y_axis[i-1])
                even_transitions.append(j)

    context['file_exists'] = True
    context['data'] = even_y_axis
    context['labels'] = even_transitions
    context['total_nonrestful_time'] = '%.2f'%(float(total_nonrestful_time) / len(timestamps))
    context['total_restful_time'] = '%.2f'%(float(total_restful_time) / len(timestamps))

    # Calculate total restful and total nonrestful time.
    restful_time = 0
    nonrestful_time = 0
    for i in xrange(1, len(y_axis)):
        if y_axis[i-1] == 1 and y_axis[i] == 2:
            nonrestful_time += (all_transitions[i] - all_transitions[i-1])
        elif y_axis[i-1] == 2 and y_axis[i] == 1:
            restful_time += (all_transitions[i] - all_transitions[i-1])

    context['nonrestful_time'] = nonrestful_time
    context['restful_time'] = restful_time

    # Calculate sleep efficiency
    total_sleep_time = (timestamps[-1] - timestamps[0]) / 60
    time_to_fall_asleep = 25
    time_awakened = 25
    total_time_asleep = total_sleep_time - time_to_fall_asleep - time_awakened
    sleep_efficiency = (round(float(total_time_asleep) / total_sleep_time, 3) * 100)

    context['sleep_efficiency'] = sleep_efficiency
    context['duration'] = nonrestful_time + restful_time

    # Store in cache
    context_cache[filename] = context

    return JsonResponse(context)

#train the onBedClf using all on-off samples
def learnOnOffClf():
    xVector = []
    labelVector = []

    for oogroup in OnOffGroup.objects.all():
        veloVals = SensorReading.objects.filter(onOffGroup=oogroup).order_by('index')
        xVector.append(map(lambda obj : obj.value , veloVals))
        labelVector.append(oogroup.label)

    print "Training onoff\nxvector: " + str(xVector)
    print "len(xVector): " + str(len(xVector))
    print "training for labels: " + str(labelVector)
    print "len(labelVector): " + str(len(labelVector))
    #learn

    try:
        onBedClf.fit(np.array(xVector), np.array(labelVector))
    except ValueError:
        return False
    return True

def showCurrentPosition(request):
    return render(request, 'snorlax/showposition.html', {})

@transaction.atomic
def storePosBuzz(request):
    if request.method != 'POST':
        raise Http404

    context = {}

    print request.POST['pos']
    print request.POST['isOn']
    pos = int(request.POST['pos'])
    isOn = request.POST['isOn']

    #Get the last alarm set
    alarms = Alarm.objects.all()
    if len(alarms) > 0:
        alarm = alarms[0]
        if pos == 1:
            #Front
            alarm.front = isOn == 'true'

        elif pos == 2:
            #Back
            alarm.back = isOn == 'true'

        elif pos == 3:
            #Right
            alarm.right = isOn == 'true'

        elif pos == 4:
            #Left
            alarm.left = isOn == 'true'

        alarm.save()
        context['alarm'] = alarm
    else:
        if pos == 1:
            #Front
            alarm = Alarm(front = isOn=='true')
        elif pos == 2:
            #Back
            alarm = Alarm(back = isOn=='true')

        elif pos == 3:
            #Right
            alarm = Alarm(right = isOn=='true')

        elif pos == 4:
            #Left
            alarm = Alarm(left = isOn=='true')
        alarm.save()

    return HttpResponse("Success", status=200)


def getPositionBuzz(request):
    if request.method != 'GET':
        raise Http404

    buzzPositions = ''

    #Check whether alarm has been set previously
    alarms = Alarm.objects.all()
    if len(alarms) > 0:
        alarm = alarms[0]
        if alarm.front:
            buzzPositions = buzzPositions + 'front,'
        if alarm.back:
            buzzPositions = buzzPositions + 'back,'
        if alarm.right:
            buzzPositions = buzzPositions + 'right,'
        if alarm.left:
            buzzPositions = buzzPositions + 'left,'

    if buzzPositions != '':
        #everything but the trailing ','
        buzzPositions = buzzPositions[:-1]

    return HttpResponse(buzzPositions)
