from django.shortcuts import render

from django.http import HttpResponse, Http404

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

from snorlax.models import *

import datetime
from django.utils.timezone import utc

def home(request):
    return render(request, 'snorlax/index.html')

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
