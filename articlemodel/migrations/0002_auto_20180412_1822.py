# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-04-12 18:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articlemodel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlemodel',
            name='author',
        ),
        migrations.RemoveField(
            model_name='articlemodel',
            name='front_author',
        ),
        migrations.RemoveField(
            model_name='articlemodel',
            name='section',
        ),
        migrations.RemoveField(
            model_name='articlemodel',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='commentmodel',
            name='article',
        ),
        migrations.RemoveField(
            model_name='commentmodel',
            name='author',
        ),
        migrations.RemoveField(
            model_name='commentmodel',
            name='relevance_comment',
        ),
        migrations.RemoveField(
            model_name='readarticlecountmodel',
            name='article',
        ),
        migrations.RemoveField(
            model_name='tagsmodel',
            name='relevance_tag',
        ),
        migrations.DeleteModel(
            name='ArticleModel',
        ),
        migrations.DeleteModel(
            name='CommentModel',
        ),
        migrations.DeleteModel(
            name='ReadArticleCountModel',
        ),
        migrations.DeleteModel(
            name='SectionModel',
        ),
        migrations.DeleteModel(
            name='TagsModel',
        ),
    ]
