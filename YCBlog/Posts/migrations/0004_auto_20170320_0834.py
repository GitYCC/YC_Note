# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0003_post_font_board'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='font_board',
            new_name='front_board',
        ),
    ]
