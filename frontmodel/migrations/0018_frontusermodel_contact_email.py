# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-27 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontmodel', '0017_auto_20190624_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontusermodel',
            name='contact_email',
            field=models.EmailField(max_length=200, null=True),
        ),
    ]
