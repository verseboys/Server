# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-07-28 11:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videomodel', '0013_auto_20180502_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videomodel',
            name='create_time',
            field=models.DateTimeField(null=True),
        ),
    ]
