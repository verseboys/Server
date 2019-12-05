#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from frontmodel.models import FrontUserModel
import json
from django.conf import settings




# 勋章列表模型

class medalModel(models.Model):
    # uid = (
    #     ('old_bird','原早鸟勋章，后更名为医咖会见证者勋章'),
    #     ('sci_god','SCI勋章'),
    #     ('yizhu_friend','朋友勋章'),
    #     ('positive_man','积极分子勋章')
    # )

    # 勋章类型将来会有扩展
    type_choices = (
        (0,'普通勋章'),
        (1, '周年勋章'),
    )
    name = models.CharField('勋章名',max_length = 191,unique = True)
    uid = models.CharField('勋章uid',max_length = 20,unique = True)
    is_valid = models.BooleanField('是否启用',default = True)
    medal_type = models.CharField('勋章类型',choices = type_choices,max_length = 10,default = 0)
    pic_url = models.URLField('勋章图路径')
    description = models.CharField('勋章描述',max_length = 200,blank = True)
    pic_ss_key = models.CharField(max_length=50,blank=True)
    pic_negative_ss_key = models.CharField(max_length=50,blank=True)
    class Meta:
		db_table = 'y_medal'

    @property
    def ss_pic_url(self):
        return settings.STORAGE_SERVICE_FILE_URL.format(self.pic_ss_key)

    @property
    def ss_pic_nagative_url(self):
        return settings.STORAGE_SERVICE_FILE_URL.format(self.pic_negative_ss_key)

#用户勋章模型

class userMedalModel(models.Model):
    medal = models.ForeignKey('medalModel',on_delete = models.CASCADE)
    user = models.ForeignKey(FrontUserModel,on_delete = models.CASCADE)
    create_time = models.DateTimeField(auto_now_add = True)
    is_disabled = models.BooleanField('是否被剥夺勋章',default = False)

    class Meta:
        db_table = 'y_user_medal'
        unique_together = ('medal','user')

#周年收集数据模型

class anniversaryModel(models.Model):
    user = models.ForeignKey(FrontUserModel,on_delete = models.CASCADE)
    anniversary_times = models.IntegerField(default = 2)
    data = models.TextField(blank = True)

    class Meta:
        db_table = 'y_anniversary'

    # 以下信息在data字段中以JSON存储
    # magazine:sci期刊名  
    # sci_mobile:sci联系方式
    # friend_mobile:医咖会朋友联系方式
    # is_writer:是否为撰稿人{0:否,1:是}
    # is_liaison:是否为联络员{0:否,1:是}
    # is_learner:是否为学习者{0:否,1:是}

    # TODO:sci_status = models.BooleanField('SCI拉黑状态',default = False)


class specialTopicCommentModel(models.Model):
    user = models.ForeignKey(FrontUserModel,on_delete = models.CASCADE)
    topic_type = models.CharField('活动类型',max_length = 20,default = 'twoYear')
    comments = models.CharField('活动留言',max_length = 2000)
    create_time = models.DateTimeField(auto_now_add = True)
    is_publish = models.BooleanField('是否展示',default = False)
    class Meta:
        db_table = 'y_special_topic_comment'

class specialTopicCommentLikeModel(models.Model):
    user = models.ForeignKey(FrontUserModel,on_delete = models.CASCADE)
    comment =  models.ForeignKey('specialTopicCommentModel',on_delete = models.CASCADE)
    class Meta:
        db_table = 'y_special_topic_comment_like'
        unique_together = ('user','comment')

class specialTopicCommentReplyModel(models.Model):
    comment =  models.OneToOneField('specialTopicCommentModel',on_delete = models.CASCADE)
    reply_content = models.CharField('留言回复',max_length = 2000)
    reply_user = models.CharField('回复人昵称',max_length = 20,default = u'小咖')
    create_time = models.DateTimeField(auto_now_add = True)
    class Meta:
        db_table = 'y_special_topic_comment_replay'






