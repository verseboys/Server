# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-05 17:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontmodel', '0010_auto_20180605_1745'),
        ('supervisormodel', '0003_userfeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeedback',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontmodel.FrontUserModel'),
        ),
    ]
