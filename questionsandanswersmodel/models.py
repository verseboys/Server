#coding:utf-8
#@author:zhangx

from django.db import models
from frontmodel.models import FrontUserModel
from methodmodel.models import MethodArticleInfoModel

#webapp问答板块模型

#问题模型
class QuestionsModel(models.Model):
	author = models.ForeignKey(FrontUserModel,null=True)
	content = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)
	is_removed = models.SmallIntegerField(null=True,default= 0) #是否删除问题,0：未删除 1：已删除
	last_answer_time = models.DateTimeField(null=True) #最新回答的时间
	category = models.ForeignKey('QuestionCategoryModel',null=True) #问题分类
	relevance_method_article = models.ForeignKey(MethodArticleInfoModel,null=True) #关联研究方法文章
	read_counts = models.IntegerField(null=True, default=0)  # 阅读数统计
	top = models.SmallIntegerField(null=True) #置顶

	class Meta:
		db_table = 'y_questions'

	def read_count(self):
		self.read_counts +=1
		self.save(update_fields=['read_counts'])

	@property
	def latest_answer(self):
		if not hasattr(self, '_latest_answer'):
			self._latest_answer = max(self.answersmodel_set.all(), key=lambda answer: answer.create_time)
		return self._latest_answer


#回答模型
class AnswersModel(models.Model):
	author = models.ForeignKey(FrontUserModel,null=True,related_name='answers_user')
	questions = models.ForeignKey('QuestionsModel',on_delete= models.CASCADE,null=True)
	comment = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)
	is_removed = models.SmallIntegerField(null=True, default=0)  # 是否删除回答,0：未删除 1：已删除
	relevance_answer = models.ForeignKey('AnswersModel',null=True,max_length=9999)# 关联的回答
	relay_to = models.ForeignKey(FrontUserModel,null=True,related_name='relay_to_user') #此评论是回复谁的,主要针对2级回复
	class Meta:
		db_table = 'y_answers'
		#ordering = ['-create_time']

'''
	date: 20170816
	author: zhangx
	mark:
		PC版中的问答板块，增加5个模型
		1、关注问题模型
		2、收藏问题模型
		3、点赞回答模型
		4、收藏回答模型
		5、给问题增加分类模型
'''

#关注问题模型
class AttentionQuestionModel(models.Model): #attention [ə'tenʃ(ə)n] 注意力，关心
	username = models.ForeignKey(FrontUserModel)
	attention_question = models.ForeignKey('QuestionsModel')

	class Meta:
		db_table = 'y_attention_question'

# #收藏问题模型
# class CollectQuestionModel(models.Model): #collect 收集,募捐
# 	username = models.ForeignKey(FrontUserModel)
# 	user_collect_category = models.ForeignKey('UserCollectCategoryModel',null=True)
# 	collect_question = models.ForeignKey('QuestionsModel')
#
# 	class Meta:
# 		db_table = 'y_collect_question'

#点赞回答模型
class PraiseAnswerModel(models.Model): #praise [preɪz] 赞扬,称赞
	username = models.ForeignKey(FrontUserModel)
	praise_answer = models.ForeignKey('AnswersModel')

	class Meta:
		db_table = 'y_praise_answer'

#收藏回答模型
class CollectAnswerModel(models.Model):
	username = models.ForeignKey(FrontUserModel)
	collect_answer = models.ForeignKey('AnswersModel')
	collect_category = models.ForeignKey('UserCollectCategoryModel',null=True)

	class Meta:
		db_table = 'y_collect_answer'

#问题分类
class QuestionCategoryModel(models.Model):
	category = models.CharField(max_length=200)
	summary = models.TextField()
	class Meta:
		db_table = 'y_question_category'

#用户自定义收藏分类
class UserCollectCategoryModel(models.Model):
	author = models.ForeignKey(FrontUserModel)
	collect_category = models.CharField(max_length=200)
	summary = models.TextField(null=True)

	class Meta:
		db_table = 'y_user_collect_category'

#我的问题回复消息模型
class MyMessagesModel(models.Model):
	replay_name = models.ForeignKey(FrontUserModel,related_name='replay_name') #回复者
	replay_answer = models.ForeignKey(AnswersModel) #回复的内容id
	question = models.ForeignKey(QuestionsModel)
	is_read = models.SmallIntegerField(default=0) #是否已查看 0：未查看 1:已查看
	create_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'y_my_messages'
		ordering = ['-create_time']

#我的关注人消息模型


#我的点赞消息模型

