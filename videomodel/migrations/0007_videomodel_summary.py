# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-26 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videomodel', '0006_auto_20180426_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='videomodel',
            name='summary',
            field=models.TextField(null=True),
        ),
    ]