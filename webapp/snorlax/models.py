from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class SensorData(models.Model):
	value = models.FloatField()
	dataType = models.CharField(max_length=50)
	time = models.DateTimeField()