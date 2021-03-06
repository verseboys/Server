# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-06-21 08:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('models', '0027_auto_20190318_1052'),
    ]

    operations = [
        migrations.CreateModel(
            name='COPDLive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=191, verbose_name=b'\xe7\x9b\xb4\xe6\x92\xad\xe6\xa0\x87\xe9\xa2\x98')),
                ('plan_begin', models.DateTimeField(verbose_name=b'\xe7\x9b\xb4\xe6\x92\xad\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88\xe8\xae\xa1\xe5\x88\x92\xef\xbc\x89')),
                ('plan_end', models.DateTimeField(verbose_name=b'\xe7\x9b\xb4\xe6\x92\xad\xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4\xef\xbc\x88\xe8\xae\xa1\xe5\x88\x92\xef\xbc\x89')),
                ('introduction', models.TextField(verbose_name=b'\xe7\x9b\xb4\xe6\x92\xad\xe7\xae\x80\xe4\xbb\x8b')),
                ('host', models.CharField(max_length=191, verbose_name=b'\xe4\xb8\xbb\xe5\x8a\x9e\xe6\x96\xb9')),
                ('is_active', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\x91\xe5\xb8\x83')),
                ('show_in_list', models.BooleanField(default=False, verbose_name=b'\xe5\x88\x97\xe8\xa1\xa8\xe9\xa1\xb5\xe6\x98\xbe\xe7\xa4\xba')),
                ('display_order', models.IntegerField(default=0, verbose_name=b'\xe6\x8e\x92\xe5\xba\x8f')),
                ('vhall_roomid', models.CharField(max_length=255, verbose_name=b'\xe5\xbe\xae\xe5\x90\xbc\xe6\x88\xbf\xe9\x97\xb4\xe5\x8f\xb7')),
            ],
            options={
                'db_table': 'y_copdlive',
            },
        ),
        migrations.CreateModel(
            name='COPDLiveTalker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('live', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.COPDLive')),
            ],
            options={
                'db_table': 'y_copdlive_talker',
            },
        ),
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=191, verbose_name=b'\xe5\xa7\x93\xe5\x90\x8d')),
                ('introduction', models.TextField(verbose_name=b'\xe7\xae\x80\xe4\xbb\x8b')),
                ('organization', models.CharField(max_length=191, verbose_name=b'\xe5\x8d\x95\xe4\xbd\x8d')),
            ],
            options={
                'db_table': 'y_expert',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=128, unique=True)),
                ('local_path', models.TextField()),
                ('filename', models.TextField()),
                ('title', models.TextField()),
                ('content_type', models.TextField()),
                ('size', models.IntegerField()),
                ('md5sum', models.TextField()),
                ('bucket', models.TextField()),
                ('deleted_at', models.DateTimeField(null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'y_media_image',
            },
        ),
        migrations.AddField(
            model_name='expert',
            name='picture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='models.Image', verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f'),
        ),
        migrations.AddField(
            model_name='copdlivetalker',
            name='talker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Expert'),
        ),
        migrations.AddField(
            model_name='copdlive',
            name='talkers',
            field=models.ManyToManyField(through='models.COPDLiveTalker', to='models.Expert', verbose_name=b'\xe8\xae\xb2\xe5\xb8\x88'),
        ),
        migrations.AddField(
            model_name='copdlive',
            name='thumbnail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='models.Image', verbose_name=b'\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe'),
        ),
    ]
