from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class SensorData(models.Model):
	value = models.FloatField()
	dataType = models.CharField(max_length=50)
	time = models.DateTimeField()


#####  Next 2 classes for ML Data storage  ######

class LogGroup(models.Model):
	time = models.DateTimeField(auto_now=True)

#Group to store on-off data
class OnOffGroup(models.Model):
	time = models.DateTimeField(auto_now=True)
	#optional label (used for training). Eg. "position_back", "position_front"
	label = models.CharField(max_length=50, null=True, default=None)
	

#points to a LogGroup of readings that represents a threshold
class ThresholdRef(models.Model):
	logGroup = models.ForeignKey(LogGroup)

#multiple sensor readings per group (one-to-many)
class ReadingGroup(models.Model):
	time = models.DateTimeField(auto_now=True)

	#optional label (used for training). Eg. "position_back", "position_front"
	label = models.CharField(max_length=50, null=True, default=None)

class SensorReading(models.Model):
	value = models.IntegerField()
	rgroup = models.ForeignKey(ReadingGroup, null=True, default=None)
	index = models.IntegerField()
	sensorType = models.CharField(max_length=30, null=True, default=None)
	logGroup=models.ForeignKey(LogGroup, null=True, default=None)
	onOffGroup = models.ForeignKey(OnOffGroup, null=True, default=None)
	
###############################################


class Time(models.Model):
	time = models.DateTimeField(auto_now=True)

class AccelerometerData(models.Model):
	sensorId = models.IntegerField()
	xValue = models.IntegerField()
	yValue = models.IntegerField()
	zValue = models.IntegerField()
	time = models.ForeignKey(Time)

class VelostatData(models.Model):
	sensorId = models.IntegerField()
	value = models.IntegerField()
	time = models.ForeignKey(Time)

class MicrophoneData(models.Model):
	sensorId = models.IntegerField()
	value = models.IntegerField()
	time = models.ForeignKey(Time)

class Alarm(models.Model):
	time = models.DateTimeField()
	switch = models.BooleanField(default=True)
	yetToHappen = models.BooleanField(default=True)
	front = models.BooleanField(default=False)
	back = models.BooleanField(default=False)
	right = models.BooleanField(default=False)
	left = models.BooleanField(default=False)

class LogSleep(models.Model):
	#day = models.DateField()
	day = models.IntegerField() #max_length=2
	year = models.IntegerField() #max_length=4
	month = models.IntegerField() #max_length=2
	quality = models.CharField(max_length=15)
	description = models.CharField(max_length=500)
	dreams = models.BooleanField(default=False)
