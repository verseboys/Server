#coding:utf-8
from django.shortcuts import reverse, redirect

from models import FrontUserModel
import configs
from extends.buildjson import json_result,json_unauth_error,json_params_error,json_method_error,json_block_error,json_redirect_error

#增加一个登录装饰器
def front_login_required(func):
	def wrapper(request,*args,**kwargs):
		user = getattr(request, 'front_user', None)
		if not user:
			return json_redirect_error(message=u'请先登录!')
		if not user.is_active:
			return json_block_error(message=u'此账号被锁定,请联系管理员!')
		else:
			return func(request, *args, **kwargs)

	return wrapper

def login_required(view_func):
	def wrapper(request, *args, **kwargs):
		user = getattr(request, 'front_user', None)
		if not user or not user.is_active:
			login_url = reverse('front_login') + '?next=' + request.path + '#1'
			return redirect(login_url)
		return view_func(request, *args, **kwargs)

	return wrapper

#判断用户资料是否完整
def front_user_infomation_is_full(func):
	def wrapper(request,*args,**kwargs):
		user = getattr(request, 'front_user', None)
		if user:
			if user.corporation and user.profession and user.jobtitle:
				return func(request,*args,**kwargs)
			# elif not user.corporation:
			# 	return json_unauth_error(message=u'单位不能为空，请先到个人中心补充完善个人资料信息!')
			# elif not user.profession:
			# 	return json_unauth_error(message=u'科室不能为空，请先到个人中心补充完善个人资料信息!')
			# elif not user.jobtitle:
			# 	return json_unauth_error(message=u'职位不能为空，请先到个人中心补充完善个人资料信息!')
			else:
				return json_unauth_error(message=u'请先到个人中心补充完善个人资料信息!')
	return wrapper


# 判断用户资料是否完整（非硬性,只记录状态）
def front_user_infomation_is_full_soft(func):
	def wrapper(request,*args,**kwargs):
		user = getattr(request, 'front_user', None)
		if user:
			#公司是否填写
			if user.corporation and user.profession and user.jobtitle:
				request.is_user_information_full = True
				return func(request,*args,**kwargs)
			else:
				request.is_user_information_full = False
				return func(request,*args,**kwargs)
	return wrapper
