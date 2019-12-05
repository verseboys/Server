#coding:utf-8

from alipay import AliPay
from frontmodel import configs
from django.conf import settings
import os

'''
	author:zhangx
	data:20180530
	mark:
		1、视频支付
		2、调用支付宝付款
'''

def y_alipay():

	with open(os.path.join(settings.BASE_DIR, 'extends/alipay/web_private_key.txt').replace("\\", "/")) as f:
		app_private_key_string = f.read()

	with open(os.path.join(settings.BASE_DIR, 'extends/alipay/alipay_public_key.txt').replace("\\", "/")) as f:
		alipay_public_key_string = f.read()

	alipay = AliPay(
		appid = configs.APPID,
		app_notify_url = configs.APP_NOTIFY_URL,
		app_private_key_string =app_private_key_string,
		alipay_public_key_string =alipay_public_key_string,
		sign_type="RSA2",
		debug=False,
	)
	return alipay

def y_alipay_return_url(out_trade_no,total_amount,subject):
	alipay = y_alipay()
	if subject:
		subject = str(subject).encode('utf-8')

	order_string = alipay.api_alipay_trade_page_pay(
		out_trade_no=out_trade_no,
		total_amount=total_amount,
		subject=subject,
		return_url=configs.APP_NOTIFY_URL,
	)
	re_url = u'{request_trade}?{data}'.format(request_trade=configs.REQUEST_TRADE, data=order_string)

	return re_url