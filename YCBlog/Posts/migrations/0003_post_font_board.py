# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0002_auto_20170319_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='font_board',
            field=models.URLField(blank=True),
        ),
    ]
