# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-12 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('methodmodel', '0004_keywordgroupmodel_keywordmodel_keywordrelevancearticlemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='bannermodel',
            name='type',
            field=models.IntegerField(choices=[(1, 'PC\u7aef'), (2, '\u79fb\u52a8\u7aef')], default=1),
        ),
        migrations.AddField(
            model_name='methodarticleinfomodel',
            name='app_thumbnail',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='methodarticletopicmodel',
            name='app_thumbnail',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='methodcategorymodel',
            name='banner',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='methodcategorymodel',
            name='link',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]