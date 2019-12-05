#coding:utf-8
'''
	author:zhangx
	date: 20171206
	mark :
		1、研究方法3.0版本相关的模型

'''

from django.db import models
from frontmodel.models import FrontUserModel
from django.contrib.auth.models import User
from django.shortcuts import reverse

#研究方法的分类模型
class MethodCategoryModel(models.Model):
	type = (
		(1, '文章'),
		(2, '视频'),
	)
	category = models.CharField(max_length=70) #分类名称
	grade = models.IntegerField(null=True) #层级
	relevance_category = models.ForeignKey('MethodCategoryModel',null=True) #关联的分类
	create_time = models.DateTimeField(auto_now_add=True)
	is_active = models.SmallIntegerField(null=True,default=1) #是否显示 0：不显示 1:显示
	rank = models.SmallIntegerField(default=1) #自定义排序展示,用于在前台中此分类展示的顺序
	column = models.SmallIntegerField(null=True) #由于前台分类展示布局的特性,特增加此字段来识别当前分类展示在哪一列
	link = models.CharField(max_length=1000,null=True) #链接
	banner = models.CharField(max_length=200,null=True) #移动端的banner
	type = models.IntegerField(choices=type, default=1)  # 类型是视频还是文章

	class Meta:
		db_table ='y_method_category'

'''
	author: zhangx
	date: 20171206
	mark：
		1、由于研究方法文章内容是由不同版块构成的特性，因此将每篇文章的标题属性和内容拆分存储
		2、研究方法的文章标题和属性模型：MethodArticleInfoModel
		   研究方法的文章内容模型：MethodArticleContentModel
		   研究方法的文章内容版块模型：MethodArticleContentSectionModel
'''

#研究方法的文章标题和属性模型
class MethodArticleInfoModel(models.Model):
	title = models.CharField(max_length=200)
	summary = models.TextField(null=True) #摘要
	thumbnail = models.CharField(max_length=200,null=True) #缩略图
	app_thumbnail = models.CharField(max_length=200,null=True) #移动端缩略图
	author = models.ForeignKey(User, null=True)  # 管理员作者 , 文章允许管理员和用户都发布
	front_author = models.ForeignKey(FrontUserModel, null=True)  # 前台作者，文章允许管理员和用户都发布
	category = models.ForeignKey('MethodCategoryModel',null=True) #所属分类
	rank = models.SmallIntegerField(null=True) # 文章的级别，1:最新 2:简单 3:详细 4:无
	status = models.SmallIntegerField(default=3) #文章状态 0：删除  1:发布  2：推荐 3：草稿
	file_name = models.CharField(max_length=1000,null=True) #附件地址
	arrange = models.SmallIntegerField(null=True) #自定义文章排序
	create_time = models.DateTimeField(null=True) #创建时间
	read_counts = models.IntegerField(null=True, default=0)

	class Meta:
		db_table = 'y_method_article_info'
		ordering = ['-create_time']

	def read_count(self):
		self.read_counts += 1
		self.save(update_fields=['read_counts'])

	@property
	def url(self):
		urlname = 'front_method_topic_article_detail' if self.category_id == 13 else 'front_method_article_detail'
		return reverse(urlname, kwargs={'article_id': self.id})

#研究方法的文章内容模型
class MethodArticleContentModel(models.Model):
	article = models.ForeignKey('MethodArticleInfoModel') #对应的文章标题和属性
	content = models.TextField()
	section = models.ForeignKey('MethodArticleContentSectionModel') #版块
	is_login = models.SmallIntegerField(default=0) #是否需要登录后才能查看  0：不需要登录  1：需要登录
	rank = models.SmallIntegerField(null=True) #自定义内容版块排序
	create_time = models.DateTimeField(null=True) #跟研究方法文章标题的时间同步

	class Meta:
		db_table = 'y_method_article_content'

#研究方法的文章内容版块模型
class MethodArticleContentSectionModel(models.Model):
	section = models.CharField(max_length=200)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'y_method_article_content_section'

#文章相关阅读版块模型
class MethodArticleRelatedReadingModel(models.Model):
	'''
		当文章有相关阅读版块时,需要给当前文章关联一部分文章来展示到相关阅读版块
	'''
	relevance_article = models.ForeignKey('MethodArticleInfoModel',related_name='relevance_article')  #关联文章id
	related_reading_article = models.ForeignKey('MethodArticleInfoModel',related_name='related_reding_article') #关联的更多阅读文章id
	arrange = models.SmallIntegerField(default=1) #自定义相关阅读文章排序
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'y_method_article_related_reading'
		ordering = ['-create_time']

#banner图
class BannerModel(models.Model):
	source_type = (
		(1,u'PC端'),
		(2,u'移动端')
	)
	name = models.CharField(max_length=1000)
	is_active = models.SmallIntegerField(default=0) #默认0不显示 ，1显示
	rank = models.SmallIntegerField(default=1) #自定义banner排序
	link = models.CharField(max_length=1000,null=True) #链接
	create_time = models.DateTimeField(auto_now_add=True)
	type = models.IntegerField(choices=source_type,default=1)
	class Meta:
		db_table = 'y_banner'

#研究方法专题模型
class MethodArticleTopicModel(models.Model):
	title = models.CharField(max_length=200) #名称
	summary = models.TextField() #摘要
	status = models.SmallIntegerField(default=1) #状态 1：隐藏  2：发布
	arrange = models.SmallIntegerField(null=True) #专题排序
	create_time = models.DateTimeField(null=True)
	read_counts = models.IntegerField(default=0) #专题访问总数
	thumbnail = models.CharField(max_length=1000,null=True) #封面图
	app_thumbnail = models.CharField(max_length=1000, null=True)  # 封面图
	class Meta:
		db_table = 'y_method_article_topic'
		ordering = ['-create_time']

	def read_count(self):
		self.read_counts += 1
		self.save(update_fields=['read_counts'])

#专题相关研究方法文章模型
class TopicRelatedMethodArticleModel(models.Model):
	topic = models.ForeignKey('MethodArticleTopicModel')  #专题id
	article = models.ForeignKey('MethodArticleInfoModel') #文章id
	arrange = models.SmallIntegerField(null=True) #专题相关文章自定义排序
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'y_topic_related_method_article'
		ordering = ['-create_time']

'''
	author:zhangx
	date:20180313
	mark:
		下面是提问时关键词检索模型
'''

#关键词分组模型
class KeyWordGroupModel(models.Model):
	group_name = models.CharField(max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'y_key_word_group'
		ordering = ['-create_time']

#关键词
class KeyWordModel(models.Model):
	group_name = models.ForeignKey('KeyWordGroupModel')
	key_word = models.CharField(max_length=100)
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'y_key_word'
		ordering = ['-create_time']

#关键词分组下关联的文章模型
class KeyWordRelevanceArticleModel(models.Model):
	article_type = (
		(1,u'研究方法'),
		(2,u'专题合集')
	)
	group_name = models.ForeignKey('KeyWordGroupModel')
	article = models.SmallIntegerField(null=True)
	type = models.SmallIntegerField(choices=article_type,null=True) #区分是研究方法还是专题合集
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table ='y_key_word_relevance_article'
		ordering = ['-create_time']
