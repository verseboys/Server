#coding:utf-8
from django.http import HttpResponse,JsonResponse
from captcha.buildcaptcha import Captcha
from django.core.cache import cache
try:
	from cStringIO import StringIO
except:
	from io import BytesIO as StringIO
from django.conf import settings
from django.core import mail
import logging
import hashlib
import time,os
from django.views.decorators.http import require_http_methods
from extends.buildjson import json_result, json_params_error
from frontmodel import configs

logger = logging.getLogger(__name__)

#将验证码图片当成流发送给客户端
def captcha(request):
	text,image = Captcha.gene_code()
	#需要通过StringIO这个类来把图片当成流的形式返回给客户端
	out = StringIO()#获取管道
	image.save(out,'png')#把图片保存到管道中
	out.seek(0)#移动文件指针到第0个位置
	cache.set(request.session.session_key,text,60*10)
	response = HttpResponse(content_type = 'image/png')
	response.write(out.read())

	logger.info(u'生成的验证码是：%s'%cache.get(request.session.session_key))
	
	return response

# 发送验证码邮件
def send_captcha_email(request,email,subject=None,message=None):
	captcha(request)
	cache_captcha = cache.get(request.session.session_key)
	
	#将验证码和邮箱绑定，存入缓存
	cache_data ={
		'email':email,
		'cache_captcha':cache_captcha,
	}
	cache.set(request.session.session_key,cache_data,60*10)
	
	if subject:
		subject=subject
	else:
		subject = u'[医咖会]-注册验证码'
		
	if message:
		message = message['first_content'] + cache_captcha + u',请在10分钟内完成验证。工作人员不会向您索取验证码'
	else:
		message = u'这是来自[医咖会]的注册邮件,您的验证码是：' + cache_captcha + u',请在10分钟内完成验证。工作人员不会向您索取验证码'
	from_email = settings.EMAIL_HOST_USER
	recipinet_list = [email]
	
	if mail.send_mail(subject, message, from_email, recipinet_list):
		#request.session['email'] = email  # 将邮箱存入缓存
		return True
	else:
		return False


#上传图片重命名
@require_http_methods(['GET','POST'])
def image_storage(request,img_path):
	if request.method == 'POST':
		imgFile = request.FILES.get('imgFile')

		logger.info({'imgFile':imgFile})

		if imgFile:
			file_name = hashlib.md5(str(time.time()) + imgFile.name).hexdigest()
			file_path = os.path.join(settings.BASE_DIR, 'images/%s/%s', ).replace("\\", "/")%(img_path, file_name)
			with open(file_path, 'wb') as f:
				for chunk in imgFile.chunks():
					f.write(chunk)
			return json_result(data=file_name)
		else:
			return json_params_error(message=u'图片不能为空!')

#上传附件
@require_http_methods(['GET','POST'])
def upload_file(request,file_path):
	if request.method == 'POST':
		fileInfo = request.FILES.get('file_info')
		if fileInfo:
			filePath = os.path.join(settings.BASE_DIR,'media/%s/%s').replace("\\","/")%(file_path,fileInfo.name)
			with open(filePath,'wb') as f:
				for chunk in fileInfo.chunks():
					f.write(chunk)
			return json_result(data=fileInfo.name)
		else:
			return json_params_error(message=u'请添加需要上传的文件!')




























