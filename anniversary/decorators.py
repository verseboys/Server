#coding:utf-8
from frontmodel.models import FrontUserModel
from frontmodel import configs
# from extends.buildjson import json_result,json_unauth_error,json_params_error,json_method_error,json_block_error,json_redirect_error
from models import anniversaryModel
import json

#周年庆典数据装饰器
def anniversary_data(func):
	def wrapper(request,*args,**kwargs):

		user = request.front_user
		# 目前只有两周年的数据
		anniversary2 = anniversaryModel.objects.filter(user = user,anniversary_times = 2).first()
		if anniversary2:
			request.anniversary2 = anniversary2
		else:
			request.anniversary2 = None
		return func(request,*args,**kwargs)

	return wrapper
