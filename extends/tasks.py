#coding:utf-8

'''
	author:zhangx
	date:20180531
	mark:
		定时任务
'''
from __future__ import absolute_import,unicode_literals
from celery import task
from frontmodel.models import UserBuyOrderModel
import datetime,redis,time
from yizhu import settings


@task
def update_order_status(order_id):
	orderId = order_id

	orderModel = UserBuyOrderModel.objects.filter(order_id=orderId, status=1).first()
	if orderModel:
		orderModel.status = 0
		orderModel.save()
		print u'{}订单超时未支付...已失效!'.format(orderId)
	else:
		print u'{}订单不存在!'.format(orderId)




