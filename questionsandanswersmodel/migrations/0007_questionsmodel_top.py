# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-01-29 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionsandanswersmodel', '0006_questionsmodel_read_counts'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionsmodel',
            name='top',
            field=models.SmallIntegerField(default=0, null=True),
        ),
    ]