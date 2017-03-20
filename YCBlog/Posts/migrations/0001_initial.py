# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField(blank=True)),
                ('file', models.URLField(blank=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('post_time', models.DateTimeField()),
                ('isPublic', models.BooleanField()),
                ('kind', models.CharField(max_length=60)),
                ('tags', models.CharField(max_length=200, blank=True)),
                ('author', models.CharField(max_length=100)),
            ],
        ),
    ]
