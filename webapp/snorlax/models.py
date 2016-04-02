from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class SensorData(models.Model):
	value = models.FloatField()
	dataType = models.CharField(max_length=50)
	time = models.DateTimeField()

class AccelerometerData(models.Model):
	sensorId = models.IntegerField()
	xValue = models.IntegerField()
	yValue = models.IntegerField()
	zValue = models.IntegerField()

class VelostatData(models.Model):
	sensorId = models.IntegerField()
	value = models.IntegerField()

class MicrophoneData(models.Model):
	sensorId = models.IntegerField()
	value = models.IntegerField()

class Time(models.Model):
	time = models.DateTimeField()
	velostats = models.ManyToManyField(VelostatData)
	accelerometers = models.ManyToManyField(AccelerometerData)
	microphones = models.ManyToManyField(MicrophoneData)
