from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class SensorData(models.Model):
	value = models.FloatField()
	dataType = models.CharField(max_length=50)
	time = models.DateTimeField()

#multiple sensor readings per group (one-to-many)
class ReadingGroup(models.Model):
	time = models.DateTimeField(auto_now=True)

	#optional label (used for training). Eg. "position_back", "position_front"
	label = models.CharField(max_length=50, null=True, default=None)

class SensorReading(models.Model):
	value = models.FloatField()
	rgroup = models.ForeignKey(ReadingGroup, null=True, default=None)
	index = models.IntegerField()
	sensorType = models.CharField(max_length=30, null=True, default=None)
