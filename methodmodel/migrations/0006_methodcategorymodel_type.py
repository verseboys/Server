# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-26 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('methodmodel', '0005_auto_20180412_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='methodcategorymodel',
            name='type',
            field=models.IntegerField(choices=[(1, b'\xe6\x96\x87\xe7\xab\xa0'), (2, b'\xe8\xa7\x86\xe9\xa2\x91')], default=1),
        ),
    ]
