# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-31 01:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontmodel', '0003_auto_20171031_0158'),
        ('questionsandanswersmodel', '0002_auto_20170610_0126'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttentionQuestionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attention_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionsandanswersmodel.QuestionsModel')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontmodel.FrontUserModel')),
            ],
            options={
                'db_table': 'y_attention_question',
            },
        ),
        migrations.CreateModel(
            name='CollectAnswerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'y_collect_answer',
            },
        ),
        migrations.CreateModel(
            name='CollectQuestionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collect_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionsandanswersmodel.QuestionsModel')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontmodel.FrontUserModel')),
            ],
            options={
                'db_table': 'y_collect_question',
            },
        ),
        migrations.CreateModel(
            name='PraiseAnswerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'y_praise_answer',
            },
        ),
        migrations.CreateModel(
            name='QuestionCategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200)),
                ('summary', models.TextField()),
            ],
            options={
                'db_table': 'y_question_category',
            },
        ),
        migrations.CreateModel(
            name='UserCollectCategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collect_category', models.CharField(max_length=200)),
                ('summary', models.TextField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontmodel.FrontUserModel')),
            ],
            options={
                'db_table': 'y_user_collect_category',
            },
        ),
        migrations.AddField(
            model_name='answersmodel',
            name='relay_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relay_to_user', to='frontmodel.FrontUserModel'),
        ),
        migrations.AlterField(
            model_name='answersmodel',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers_user', to='frontmodel.FrontUserModel'),
        ),
        migrations.AddField(
            model_name='praiseanswermodel',
            name='praise_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionsandanswersmodel.AnswersModel'),
        ),
        migrations.AddField(
            model_name='praiseanswermodel',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontmodel.FrontUserModel'),
        ),
        migrations.AddField(
            model_name='collectanswermodel',
            name='collect_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionsandanswersmodel.AnswersModel'),
        ),
        migrations.AddField(
            model_name='collectanswermodel',
            name='collect_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='questionsandanswersmodel.UserCollectCategoryModel'),
        ),
        migrations.AddField(
            model_name='collectanswermodel',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontmodel.FrontUserModel'),
        ),
        migrations.AddField(
            model_name='questionsmodel',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='questionsandanswersmodel.QuestionCategoryModel'),
        ),
    ]
