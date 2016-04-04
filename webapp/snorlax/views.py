from django.shortcuts import render

from django.http import HttpResponse, Http404

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

from snorlax.models import *

import datetime
from django.utils.timezone import utc

MAX_VALUES = 50

def home(request):
    return render(request, 'snorlax/index.html')

@transaction.atomic
def storeData(request):
    if request.method != 'POST':
        raise Http404

    val = float(request.POST['value'])
    valType = request.POST['dataType']
    currTime = datetime.datetime.utcnow().replace(tzinfo=utc)

    sensorData = SensorData(value=val, dataType=valType, time=currTime)

    sensorData.save()

    return HttpResponse("Success", status=200)


def trainPosition(request):
	if request.method != 'POST':
		raise Http404

	print "POST params:"
	print str(request.POST.items())

	sensorType = request.POST['sensorType'] if 'sensorType' in request.POST else ''  
	label = request.POST['label'] if 'label' in request.POST else '' 
	
	rgroup = ReadingGroup(label=label)
	rgroup.save()

	for i in xrange(MAX_VALUES):
		paramKey = "value" + str(i)
		
		if paramKey in request.POST:
			currValue = request.POST[param]
			print "got param: " + currValue
			
			reading = SensorReading(value=float(currValue), rgroup=rgroup,\
								index=i, sensorType=sensorType)
			reading.save()
		

	return HttpResponse("Success", status=200)	
