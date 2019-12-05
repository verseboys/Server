#coding:utf-8

from django.db import models
from django.contrib.auth.models import User
from frontmodel.models import FrontUserModel,UserFavoritesModel,UserBuyOrderModel,UserPraiseModel
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from methodmodel.models import  MethodCategoryModel


'''
	author:zhangx
	date:20180424
	mark:
		1、视频模块的模型

'''

#视频模型
class VideoModel(models.Model):
	status_type = (
		(0,'已删除'),
		(1,'已发布'),
		(2,'草稿'),
	)
	is_pay_type = (
		(0,'免费课程'),
		(1,'付费课程'),
		(2,'更新中'),
	)
	author = models.ForeignKey(User,null=True)
	title = models.CharField(max_length=200) #标题
	course = models.ForeignKey(MethodCategoryModel,null=True) #视频所属课程
	course_main = models.TextField(null=True) #课程要点
	summary = models.TextField(null=True) #摘要
	polyv_vid = models.CharField(max_length=200,null=True) #保利威视关联的视频id
	status = models.IntegerField(choices=status_type,default=2) #视频发布状态
	is_pay = models.IntegerField(choices=is_pay_type,default=0) #是否收费
	video_time = models.CharField(max_length=20,null=True) #视频时长
	thumbnail = models.CharField(max_length=200, null=True)  # 缩略图
	create_time = models.DateTimeField(auto_now_add=False,null=True)
	user_buy_order = GenericRelation(UserBuyOrderModel)
	user_favorites = GenericRelation(UserFavoritesModel)
	teacher_introduction = models.TextField(blank=True)

	class Meta:
		db_table = 'y_video'

#课程模型
class CourseModel(models.Model):
	course = models.ForeignKey(MethodCategoryModel,null=True) #老师关联的课程
	course_intro = models.TextField(max_length=2000, null=True)  # 课程简介
	thumbnail = models.CharField(max_length=200, null=True)  # 缩略图
	teach_intro = models.TextField(max_length=2000, null=True)  # 讲者简介
	price = models.DecimalField(max_digits=20, decimal_places=2,null=True)  # 金额
	create_time = models.DateTimeField(auto_now_add=True)
	class Meta:
		db_table = 'y_course'

#视频资料模型
class VideoRelatedDataModel(models.Model):
	video = models.ForeignKey(VideoModel)
	file_name = models.CharField(max_length=300,null=True) #附件名称
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'y_video_realted_data'

#视频评论模型
class VideoCommentModel(models.Model):
	username = models.ForeignKey(FrontUserModel)
	video = models.ForeignKey(VideoModel)
	comment = models.TextField()
	relevance_comment = models.ForeignKey('VideoCommentModel',null=True)
	create_time = models.DateTimeField(auto_now_add=True)
	user_praise = GenericRelation(UserPraiseModel)

	class Meta:
		db_table = 'y_video_comment'
		ordering = ['-create_time']


