# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snorlax', '0001_initial'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='sensorreading',
            name='logGroup',
            field=models.ForeignKey(default=None, to='snorlax.LogGroup', null=True),
        ),
    ]
