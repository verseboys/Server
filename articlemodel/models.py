#coding:utf-8
'''
2017-4-21  zhangxiao
	1、PC网站文章模型

'''
#
# from django.db import models
# from frontmodel.models import FrontUserModel
# from django.contrib.auth.models import User
# import time
#
# #文章模型
# #20171211在研究方法3.0版本以后,此模型将废弃
# class ArticleModel(models.Model):
# 	title = models.CharField(max_length = 200)
# 	summary = models.TextField(null=True) #简介
# 	content = models.TextField()
# 	thumbnail = models.CharField('缩略图',max_length = 200,null=True) #缩略图
# 	#thumbnail = models.ImageField(upload_to='article_images',null=True,storage=ImageStorage()) #缩略图
# 	publish_time = models.DateTimeField(null=True) #发表时间
# 	#modify_time = models.DateTimeField('修改时间',auto_now = True) #修改时间
# 	author = models.ForeignKey(User,null = True) #管理员作者 ，文章允许管理员和用户都发布
# 	front_author = models.ForeignKey(FrontUserModel,null=True) #前台作者，文章允许管理员和用户都发布
# 	section = models.ForeignKey('SectionModel',default=1) #所属版块
# 	tags = models.ManyToManyField('TagsModel')
# 	status = models.SmallIntegerField(default = 0) #文章状态 0：删除 1:发布 2：推荐 3：草稿
#
# 	class Meta:
# 		db_table = 'y_articles'
# 		ordering = ['-publish_time']
#
# #评论模型
# # 20171211在研究方法3.0版本以后,此模型将废弃
# class CommentModel(models.Model):
# 	author = models.ForeignKey(FrontUserModel,null = True) #对应的作者
# 	article = models.ForeignKey('ArticleModel',null = True) #对应的文章
# 	comment = models.TextField()
# 	create_time = models.DateTimeField(auto_now_add = True)
# 	status = models.IntegerField(default=1,null=True) #评论状态 0:删除 1：显示
# 	relevance_comment = models.ForeignKey('CommentModel',null=True) #关联的评论
#
# 	class Meta:
# 		db_table = 'y_comments'
# 		ordering = ['-create_time']
#
# #文章阅读计数
# class ReadArticleCountModel(models.Model):
# 	article = models.ForeignKey('ArticleModel')
# 	read_count = models.IntegerField('阅读数量',default=0)
#
# 	class Meta:
# 		db_table = 'y_read_article_count'
#
# #版块模型
# class SectionModel(models.Model):
# 	section = models.CharField(max_length=70)
#
# 	class Meta:
# 		db_table = 'y_sections'
#
# #标签模型
# class TagsModel(models.Model):
# 	tag = models.CharField(max_length=50,unique=True)
# 	grade = models.IntegerField(null=True)#层级
# 	relevance_tag = models.ForeignKey('TagsModel',null=True) #关联的标签
#
# 	class Meta:
# 		db_table = 'y_tags'



	
