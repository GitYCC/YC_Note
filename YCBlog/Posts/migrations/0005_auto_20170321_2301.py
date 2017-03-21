# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0004_auto_20170320_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='file',
            field=models.URLField(max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='front_board',
            field=models.URLField(max_length=500, blank=True),
        ),
    ]
