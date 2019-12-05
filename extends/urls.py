#coding:utf-8
from django.conf.urls import url
import views

urlpatterns = [
	#图形验证码
	url(r'^captcha/$',views.captcha,name = 'captcha'),
	url(r'^image_storage/(?P<img_path>\w+)/$',views.image_storage,name='image_storage'),
	url(r'^upload_file/(?P<file_path>\w+)/$',views.upload_file), #上传附件
]

