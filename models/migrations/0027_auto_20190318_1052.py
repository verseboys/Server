# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-03-18 10:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0026_auto_20190219_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='networkcourse',
            name='data_collection',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='networkcourse',
            name='order',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='networkcourse',
            name='public_scope',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='networkcourse',
            name='serial_state',
            field=models.CharField(choices=[('loading', '\u8fde\u8f7d\u4e2d'), ('finished', '\u5df2\u5b8c\u7ed3')], default='loading', max_length=10),
        ),
    ]
