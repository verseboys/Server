# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-01-30 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionsandanswersmodel', '0007_questionsmodel_top'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionsmodel',
            name='top',
            field=models.SmallIntegerField(null=True),
        ),
    ]
