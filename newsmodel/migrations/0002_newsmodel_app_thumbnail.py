# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-12 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsmodel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsmodel',
            name='app_thumbnail',
            field=models.CharField(max_length=200, null=True, verbose_name=b'\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe'),
        ),
    ]
