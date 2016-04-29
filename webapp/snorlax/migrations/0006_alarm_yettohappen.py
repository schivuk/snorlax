# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snorlax', '0005_auto_20160428_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='yetToHappen',
            field=models.BooleanField(default=True),
        ),
    ]
