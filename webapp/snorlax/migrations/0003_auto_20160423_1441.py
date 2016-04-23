# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snorlax', '0002_auto_20160423_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logsleep',
            name='day',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='logsleep',
            name='month',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='logsleep',
            name='year',
            field=models.IntegerField(),
        ),
    ]
