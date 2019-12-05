# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-12-05 21:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontmodel', '0003_auto_20171031_0158'),
        ('supervisormodel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GetResourceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_send', models.IntegerField(default=1)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supervisormodel.ArticleIndexModel')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontmodel.FrontUserModel')),
            ],
            options={
                'ordering': ['-create_time'],
                'db_table': 'wp_get_resource',
            },
        ),
    ]