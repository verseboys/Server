# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-17 21:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontmodel', '0015_auto_20190611_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontusermodel',
            name='email_need_validate',
            field=models.BooleanField(default=False),
        ),
    ]
