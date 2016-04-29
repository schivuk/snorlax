# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snorlax', '0004_auto_20160426_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThresholdRef',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('logGroup', models.ForeignKey(to='snorlax.LogGroup')),
            ],
        ),
        migrations.AddField(
            model_name='alarm',
            name='back',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alarm',
            name='front',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alarm',
            name='left',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alarm',
            name='right',
            field=models.BooleanField(default=False),
        ),
    ]
