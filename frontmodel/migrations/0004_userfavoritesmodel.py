# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-25 14:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('questionsandanswersmodel', '0008_auto_20180130_1705'),
        ('frontmodel', '0003_auto_20171031_0158'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavoritesModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('favorite_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionsandanswersmodel.UserCollectCategoryModel')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontmodel.FrontUserModel')),
            ],
            options={
                'db_table': 'y_user_favorites',
            },
        ),
    ]
