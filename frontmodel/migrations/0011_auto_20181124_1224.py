# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-11-24 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontmodel', '0010_auto_20180605_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frontusermodel',
            name='gender',
            field=models.IntegerField(choices=[(0, '\u7537'), (1, '\u5973'), (2, '\u4fdd\u5bc6')], default=0),
        ),
    ]