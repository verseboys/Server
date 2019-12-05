#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class ContentRecommend(models.Model):
    class Meta:
        db_table='y_content_recommend'

    title = models.CharField(max_length=191, unique=True)
    content_from = models.IntegerField(choices={
        (1,'首页Banner'),
        (2,'首页最新进展'),
        (3,'首页精品教程'),
    },default=1)
    introduction = models.TextField(blank=True)
    url = models.TextField(null=False)
    display_order = models.IntegerField(default=0)
    image_url_key = models.CharField(max_length=191,blank=True)
    author = models.ForeignKey(User, null=True)  # 管理员作者 ，文章允许管理员发布
    content_time = models.DateTimeField(auto_now_add=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)