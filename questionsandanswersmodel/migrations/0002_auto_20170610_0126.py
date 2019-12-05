# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-10 01:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionsandanswersmodel', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionsmodel',
            options={},
        ),
        migrations.AddField(
            model_name='answersmodel',
            name='relevance_answer',
            field=models.ForeignKey(max_length=9999, null=True, on_delete=django.db.models.deletion.CASCADE, to='questionsandanswersmodel.AnswersModel'),
        ),
        migrations.AddField(
            model_name='questionsmodel',
            name='last_answer_time',
            field=models.DateTimeField(null=True),
        ),
    ]
