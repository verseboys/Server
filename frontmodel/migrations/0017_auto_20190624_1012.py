# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-24 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontmodel', '0016_frontusermodel_email_need_validate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frontusermodel',
            name='gender',
            field=models.IntegerField(choices=[(0, '\u7537'), (1, '\u5973'), (2, '\u4fdd\u5bc6')], default=2),
        ),
    ]
