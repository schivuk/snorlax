from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, Http404

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

from snorlax.models import *

import datetime
from django.utils.timezone import utc
from django.utils import timezone

#for classification
import numpy as np
from sklearn.svm import SVC

clf = SVC(C=10, kernel='poly', degree=1, probability=True)

#latestDataJson =     

MAX_VALUES = 50

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
        alarms =Alarm.objects.all()
        if len(alarms) > 0:
            alarm = alarms[0]
            alarm.switch = not alarm.switch
            print alarm.switch
            alarm.save()
            context['alarm'] = alarm

        return render(request, 'snorlax/alarm.html', context)

def feedback(request):
    if request.method == 'GET':
        return render(request, 'snorlax/feedback.html')

def profile(request):
    if request.method == 'GET':
        return render(request, 'snorlax/profile.html')

@transaction.atomic
def editAlarm(request):
    if request.method != 'POST':
        raise Http404

    context = {}

    ampm = request.POST['ampm']
    hour = int(request.POST['hour'])
    minute = int(request.POST['min'])


    print request.POST['ampm']
    print request.POST['hour']
    print request.POST['min']

    time = timezone.now()
    #Try time.date
    #Try time.time
    time = time.replace(hour=hour, minute=minute)

    #Check whether alarm has been set previously
    alarms = Alarm.objects.all()
    if len(alarms) > 0:
        alarm = alarms[0]
        alarm.time = time
        alarm.save()
    else:
        alarm = Alarm(time=time)
        alarm.save()    

    context['alarm'] = alarm

    return render(request, 'snorlax/alarm.html', context)

@transaction.atomic
def storeData(request):
    if request.method != 'POST':
        raise Http404

    velostatVals = str(request.POST['velostatVals']).split(',')
    velostatIDs = str(request.POST['velostatIDs']).split(',')
    accelerometerVals = str(request.POST['accelerometerVals']).split(',')
    accelerometerIDs = str(request.POST['accelerometerIDs']).split(',')
    microphoneVals = str(request.POST['microphoneVals']).split(',')
    microphoneIDs = str(request.POST['microphoneIDs']).split(',')
    time = float(request.POST['time'])

    timestamp = Time(time=datetime.datetime.fromtimestamp(time))
    timestamp.save()

    for i in xrange(len(velostatIDs)):
        velostatData = VelostatData(sensorId=velostatIDs[i], value=velostatVals[i])
        velostatData.save()
        timestamp.velostats.add(velostatData)

    for i in xrange(len(accelerometerIDs)):
        accelerometerData = AccelerometerData(sensorId=accelerometerIDs[i],
                                              xValue=accelerometerVals[3*i],
                                              yValue=accelerometerVals[3*i+1],
                                              zValue=accelerometerVals[3*i+2])
        accelerometerData.save()
        timestamp.accelerometers.add(accelerometerData)

    for i in xrange(len(microphoneIDs)):
        microphoneData = MicrophoneData(sensorId=microphoneIDs[i], value=microphoneVals[i])
        microphoneData.save()
        timestamp.microphones.add(microphoneData)

    timestamp.save()

    return HttpResponse("Success", status=200)


def trainPosition(request):
    print "Called trainPosition"
    if request.method != 'POST':
        raise Http404


    velostatValsStr = request.POST['velostatVals'].split(',')
    
    print "velo values: " + str(velostatValsStr)
    veloVals = map(int, velostatValsStr)

    rgroup = ReadingGroup(label=request.POST['label'])
    rgroup.save()

    index=0
    for veloVal in veloVals:
        index += 1 
        reading = SensorReading(value=veloVal, rgroup=rgroup,\
                                index=index)
        reading.save()
        

    return HttpResponse("Success", status=200)    


#train classifier based on all data
def learnPositions(request):
    print "Called learnPositions"
    xVector = []
    labelVector = []

    for rgroup in ReadingGroup.objects.all():
        veloVals = SensorReading.objects.filter(rgroup=rgroup).order_by('index')
        xVector.append(map(lambda obj : obj.value , veloVals))
        labelVector.append(rgroup.label)

    print "xvector: " + str(xVector)
    print "len(xVector): " + str(len(xVector))
    print "training for labels: " + str(labelVector)
    print "len(labelVector): " + str(len(labelVector))
    #learn
    clf.fit(np.array(xVector), np.array(labelVector))
    print "done."
    return HttpResponse("Success", status=200)    


def getPosition(request):
    if request.method != 'POST':
        raise Http404

    velostatValsStr = request.POST['velostatVals'].split(',')    
    
    veloVals = map(int, velostatValsStr)
    print "velo values: " + str(veloVals)
   
    print "estimating values..."
    estimateArr = clf.predict([veloVals])
    print "Estimate: " + str(estimateArr[0])

    return render(request, 'snorlax/position.html', {'position': estimateArr[0]} )

#delete all training data (to start a new session)
def clearAll(request):
    SensorReading.objects.all().delete()
    ReadingGroup.objects.all().delete()
    print "All objects deleted"
    return redirect('home')

#show a template with a chart with data
def showRawData(request):
    orderedGroups = ReadingGroup.objects.all().order_by('-time')
    if len(orderedGroups) < 1:
        return  HttpResponse("No readings present", content_type='text/plain')

    firstGroup = orderedGroups[0]

    return render(request, 'snorlax/rawdata.html', {})


#def getLastReading(request):

