# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-03-07 16:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('frontmodel', '0003_auto_20171031_0158'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HoldNewsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(default=1)),
                ('arrange', models.SmallIntegerField(null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-create_time'],
                'db_table': 'y_hold_news',
            },
        ),
        migrations.CreateModel(
            name='NewsCategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=70)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'y_news_category',
            },
        ),
        migrations.CreateModel(
            name='NewsCommentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontmodel.FrontUserModel')),
            ],
            options={
                'ordering': ['-create_time'],
                'db_table': 'y_news_comment',
            },
        ),
        migrations.CreateModel(
            name='NewsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(null=True)),
                ('content', models.TextField()),
                ('thumbnail', models.CharField(max_length=200, null=True, verbose_name=b'\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe')),
                ('create_time', models.DateTimeField(null=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('file_name', models.CharField(max_length=1000, null=True)),
                ('read_counts', models.IntegerField(default=0, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='newsmodel.NewsCategoryModel')),
            ],
            options={
                'ordering': ['-create_time'],
                'db_table': 'y_news',
            },
        ),
        migrations.CreateModel(
            name='NewsRelatedReadingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_reading_article', models.SmallIntegerField(null=True)),
                ('type', models.SmallIntegerField(default=2)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('related_news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_news', to='newsmodel.NewsModel')),
            ],
            options={
                'ordering': ['-create_time'],
                'db_table': 'y_news_related_reading',
            },
        ),
        migrations.AddField(
            model_name='newscommentmodel',
            name='news',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='newsmodel.NewsModel'),
        ),
        migrations.AddField(
            model_name='holdnewsmodel',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsmodel.NewsModel'),
        ),
    ]