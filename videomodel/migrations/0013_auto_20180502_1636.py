# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-05-02 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videomodel', '0012_auto_20180502_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videomodel',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
