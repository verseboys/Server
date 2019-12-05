#coding:utf-8

'''
	author:zhangx
	date: 20180201
	mark:
		1、研究进展改版新需求

'''

from django.db import models
from frontmodel.models import FrontUserModel
from django.contrib.auth.models import User
import time


#研究进展分类模型
class NewsCategoryModel(models.Model):
	category = models.CharField(max_length=70) #分类名称
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table ='y_news_category'

#研究进展文章模型
class NewsModel(models.Model):
	title = models.CharField(max_length=200)
	category = models.ForeignKey('NewsCategoryModel',null=True)
	summary = models.TextField(null=True)  # 简介
	content = models.TextField()
	thumbnail = models.CharField('缩略图', max_length=200, null=True)  # 缩略图
	app_thumbnail = models.CharField('缩略图', max_length=200, null=True) #移动端缩略图
	create_time = models.DateTimeField(null=True)  # 发表时间
	author = models.ForeignKey(User, null=True)  # 管理员作者 ，文章允许管理员和用户都发布
	status = models.SmallIntegerField(default=1)  # 文章状态 0：删除 1:发布 2：推荐 3：草稿
	file_name = models.CharField(max_length=1000, null=True)  # 附件地址
	read_counts = models.IntegerField(null=True, default=0)

	class Meta:
		db_table = 'y_news'
		ordering = ['-create_time']

	def read_count(self):
		self.read_counts += 1
		self.save(update_fields=['read_counts'])

#研究进展评论模型
class NewsCommentModel(models.Model):
	author = models.ForeignKey(FrontUserModel, null=True)  # 对应的作者
	news = models.ForeignKey('NewsModel', null=True)  # 对应的文章
	comment = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(default=1, null=True)  # 评论状态 0:删除 1：显示

	class Meta:
		db_table = 'y_news_comment'
		ordering = ['-create_time']

#研究进展热文推荐模型
class HoldNewsModel(models.Model):
	news = models.ForeignKey('NewsModel')
	type = models.SmallIntegerField(default=1) #热文推荐，默认是右侧推荐列表，type=2的时候推荐到banner
	arrange = models.SmallIntegerField(null=True) #自定义排序
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'y_hold_news'
		ordering = ['-create_time']

#研究进展相关阅读模型
class NewsRelatedReadingModel(models.Model):
	related_news = models.ForeignKey('NewsModel',related_name='related_news')
	related_reading_article = models.SmallIntegerField(null=True) #这里写入的是文章id,且根据类型区分是研究方法还是研究进展
	type = models.SmallIntegerField(default=2) # type=1:研究方法 type=2:研究进展 区分文章属于研究方法还是研究进展
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'y_news_related_reading'
		ordering = ['-create_time']
