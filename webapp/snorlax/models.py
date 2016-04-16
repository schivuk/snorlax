from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class SensorData(models.Model):
	value = models.FloatField()
	dataType = models.CharField(max_length=50)
	time = models.DateTimeField()


#####  Next 2 classes for ML Data storage  ######


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

class LogSleep(models.Model):
	day = models.DateField()
	quality = models.CharField(max_length=15)
	description = models.CharField(max_length=500)
	dreams = models.BooleanField(default=False)
