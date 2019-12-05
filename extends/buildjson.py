#coding:utf-8

from django.http import JsonResponse
from collections import namedtuple

'''
http状态码:
200: 请求正常(ok)
400: 请求参数错误(paramserror)
401: 没有权限访问(unauth)
403: 被拉黑(block)
405: 请求方法错误(methoderror)
'''

HttpCode = namedtuple('HttpCode',['ok','redirecterror','paramserror','unauth','block','methoderror'])
httpcode = HttpCode(ok=200,redirecterror=302,paramserror=400,unauth=401,block=403,methoderror=405)

#请求成功的Json返回函数
def json_result(code=httpcode.ok,message='',data={},kwargs={}):
	json= {'code':code,'message':message,'data':data}
	if kwargs.keys():
		#把json 和kwargs合并成一个字典
		for k,v in kwargs.items():
			json[k] = v
	return JsonResponse(json)

#参数错误时返回的json
def json_params_error(message='',data={}):
	return json_result(code=httpcode.paramserror,message=message,data=data)

#没有权限访问时返回的json
def json_unauth_error(message=''):
	return json_result(code=httpcode.unauth,message=message)

#被拉黑
def json_block_error(message=''):
	return json_result(code=httpcode.block,message=message)

#请求方法错误时返回
def json_method_error(message=''):
	return json_result(code=httpcode.methoderror,message=message)

#重定向
def json_redirect_error(message=''):
	return json_result(code=httpcode.redirecterror,message=message)

