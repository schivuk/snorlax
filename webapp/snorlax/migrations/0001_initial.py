# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccelerometerData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sensorId', models.IntegerField()),
                ('xValue', models.IntegerField()),
                ('yValue', models.IntegerField()),
                ('zValue', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('switch', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='LogGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LogSleep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.IntegerField(max_length=2)),
                ('year', models.IntegerField(max_length=4)),
                ('month', models.IntegerField(max_length=2)),
                ('quality', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=500)),
                ('dreams', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MicrophoneData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sensorId', models.IntegerField()),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ReadingGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(default=None, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('dataType', models.CharField(max_length=50)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='SensorReading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('index', models.IntegerField()),
                ('sensorType', models.CharField(default=None, max_length=30, null=True)),
                ('logGroup', models.ForeignKey(default=None, to='snorlax.LogGroup', null=True)),
                ('rgroup', models.ForeignKey(default=None, to='snorlax.ReadingGroup', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VelostatData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sensorId', models.IntegerField()),
                ('value', models.IntegerField()),
                ('time', models.ForeignKey(to='snorlax.Time')),
            ],
        ),
        migrations.AddField(
            model_name='microphonedata',
            name='time',
            field=models.ForeignKey(to='snorlax.Time'),
        ),
        migrations.AddField(
            model_name='accelerometerdata',
            name='time',
            field=models.ForeignKey(to='snorlax.Time'),
        ),
    ]
