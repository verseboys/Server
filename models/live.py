# coding: utf-8
from django.db import models

"""
慢阻肺直播相关的 model

设计文档：https://confluence.natureself.site/pages/viewpage.action?pageId=34898532
原型图：https://iw2n5c.axshare.com/#g=1&p=回放-更多
设计图：https://app.zeplin.io/project/59a37c1e1d67d1f72d98c3f3/dashboard?tag=慢阻肺直播
"""

class Expert(models.Model):
    """
    讲师（直播讲师，但这里暂时不限定直播讲师，因为该 Model 将来可以在其他地方复用）

    关于命名的说明：
    * talker，讲者，会限制将来的用途
    * teacher，老师，也会一定程度上限制用途，同时 teacher 这个词太弱，不太合适（比如许多专家都是教授）
    * expert，专家，用在这里应该是最合适的
    """
    class Meta:
        db_table = 'y_expert'

    name = models.CharField(
            max_length=191,
            verbose_name='姓名',
            )
    picture = models.ForeignKey(
            'Image',
            models.PROTECT,
            verbose_name='头像',
            null=True,
            )
    introduction = models.TextField(
            verbose_name='简介',
            blank=True,
            )
    organization = models.CharField(
            max_length=191,
            verbose_name='单位',
            )

class COPDLive(models.Model):
    """
    直播
    """
    class Meta:
        db_table = 'y_copdlive'

    title = models.CharField(
            max_length=191,
            verbose_name='直播标题',
            )
    plan_begin = models.DateTimeField(
            verbose_name='直播开始时间（计划）',
            )
    plan_end = models.DateTimeField(
            verbose_name='直播结束时间（计划）',
            )
    thumbnail = models.ForeignKey(
            'models.Image',
            models.PROTECT,
            verbose_name='缩略图',
            )
    # 富文本
    introduction = models.TextField(
            verbose_name='直播简介',
            )
    host = models.CharField(
            max_length=191,
            verbose_name='主办方',
            )
    talkers = models.ManyToManyField(
            'Expert',
            through='COPDLiveTalker',
            verbose_name='讲师',
            )
    # 为发布状态的直播页面无法打开，已发布的直播页面可以打开（即使不显示在首页，只要用户有链接，就可以打开
    is_active = models.BooleanField(
            default=False,
            verbose_name='是否发布',
            )
    # 是否在列表页显示
    show_in_list = models.BooleanField(
            default=False,
            verbose_name='列表页显示',
            )
    display_order = models.IntegerField(
            default=0,
            verbose_name='排序',
            )
    vhall_roomid = models.CharField(
            max_length=255,
            verbose_name='微吼房间号',
            )

class COPDLiveTalker(models.Model):
    """
    直播-讲师 M2M 关系的中间表。一场直播会有多个讲师。

    显式声明该 Model，将来可能需要添加排序支持
    """
    class Meta:
        db_table = 'y_copdlive_talker'

    live = models.ForeignKey('COPDLive', models.CASCADE)
    talker = models.ForeignKey('Expert', models.CASCADE)
    display_order = models.IntegerField(default=0)
