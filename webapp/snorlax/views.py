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

    val = float(request.POST['value'])
    valType = request.POST['dataType']
    currTime = datetime.datetime.utcnow().replace(tzinfo=utc)

    sensorData = SensorData(value=val, dataType=valType, time=currTime)

    sensorData.save()

    return HttpResponse("Success", status=200)

