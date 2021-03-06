# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-02-19 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0025_network_notice_default_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='networknotice',
            name='read_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='contentrecommend',
            name='content_from',
            field=models.IntegerField(choices=[(1, '\u9996\u9875Banner'), (3, '\u9996\u9875\u7cbe\u54c1\u6559\u7a0b'), (2, '\u9996\u9875\u6700\u65b0\u8fdb\u5c55')], default=1),
        ),
        migrations.AlterField(
            model_name='edcstudy',
            name='level_type',
            field=models.IntegerField(choices=[(3, '\u56fd\u5bb6\u7ea7'), (0, '\u9662\u7ea7'), (1, '\u5e02\u7ea7'), (2, '\u7701\u90e8\u7ea7')], default=0),
        ),
        migrations.AlterField(
            model_name='edcstudyrole',
            name='type',
            field=models.TextField(choices=[('researcher', '\u7814\u7a76\u8005'), ('expertComm', '\u4e13\u5bb6\u59d4\u5458\u4f1a'), ('pi', 'PI')], default='researcher'),
        ),
        migrations.AlterField(
            model_name='networknotice',
            name='status',
            field=models.IntegerField(choices=[(0, '\u8349\u7a3f'), (1, '\u5df2\u53d1\u5e03')], default=0),
        ),
    ]
