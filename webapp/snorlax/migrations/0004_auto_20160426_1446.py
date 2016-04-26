# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snorlax', '0003_auto_20160423_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnOffGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(default=None, max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='sensorreading',
            name='onOffGroup',
            field=models.ForeignKey(default=None, to='snorlax.OnOffGroup', null=True),
        ),
    ]
