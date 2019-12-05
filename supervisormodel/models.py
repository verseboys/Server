#coding:utf-8

from django.db import models
from frontmodel.models import FrontUserModel

'''
##############  微信自定义菜单模型  #################

'''
#文章分类菜单
class ArticleCategoryMenuModel(models.Model):
	category = models.CharField(max_length=100)
	summary = models.TextField()
	create_time = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'wp_article_category_menu'
		ordering = ['-create_time']

#文章索引
class ArticleIndexModel(models.Model):
	title = models.CharField(max_length=200)
	category = models.ForeignKey('ArticleCategoryMenuModel')
	index = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'wp_article_index'
		ordering = ['-create_time']


'''
##############  获取文章资源模型  #################

'''
#获取文章资源模型
class GetResourceModel(models.Model):
	#email = models.CharField(max_length=200)
	username = models.ForeignKey(FrontUserModel)
	article_id = models.ForeignKey('ArticleIndexModel')
	is_send = models.IntegerField(default=1) #1:未发送 2：已发送
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'wp_get_resource'
		ordering = ['-create_time']

#用户意见反馈
class UserFeedBack(models.Model):
	username = models.ForeignKey(FrontUserModel,null=True)
	content = models.TextField()
	image = models.CharField(max_length=100)
	iphone = models.CharField(max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'y_user_feed_back'
		ordering = ['-create_time']

