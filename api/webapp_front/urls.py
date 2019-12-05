#coding:utf-8
from django.conf.urls import url
import views

'''
	2017-05-03:zhangx
	1、增加搜索问题url

	20180326：新增研究方法和研究进展接口

'''

urlpatterns = [
	url(r'^register/$',views.webapp_register,name='webapp_register'),#注册。支持get/post
	url(r'^login/$',views.webapp_login,name='webapp_login'),#登录。 支持get/post
	url(r'^logout/$',views.webapp_logout,name='webapp_logout'),#退出。支持get
	url(r'^settings/$',views.author_settings,name='author_settings'),#个人设置。支持get/post

	# wp 使用
	url(r'^send_code/', views.send_code),
	url(r'^forget_password/', views.forget_password),

	url(r'^professional_sections/(?P<department_id>\d+)/$',views.professional_sections,name='professional_sections'),#专业科室。支持get
	url(r'job_title/(?P<job_id>\d+)/$',views.job_title,name='job_title'), #职称。支持get
	url(r'^alter_password/$',views.alter_password,name='alter_password'),#修改/找回密码。支持get/post
	url(r'^send_email/$',views.send_email, name='send_email'),#给邮箱发送文本验证码 。支持POST
	url(r'^question_detail/(?P<question_id>\d+)/(?P<page>\d+)/$',views.question_detail,name='question_detail'),#问题详情。支持GET
	
	url(r'^answer_detail/(?P<question_id>\d+)/(?P<answer_id>\d+)/(?P<page>\d+)/$',views.answer_detail,name='answer_detail'),  #评论详情 支持 get
	
	url(r'^release_question/$',views.release_question,name='release_question'), #发布问题。支持get/post
	url(r'^add_answer/$',views.webapp_add_answer,name='webapp_add_answer'),#添加评论 。支持get/post
	url(r'^my_questions/(?P<page>\d+)/$',views.my_questions,name='my_questions'),#我的问题

	################     微信自定义菜单接口开始    ###################
	url(r'^article_category_info/(?P<category_id>\d+)/$',views.article_category_info,name='article_category_info'), #文章分类的摘要 get
	url(r'^article_category_list/(?P<category_id>\d+)/(?P<page>\d+)/$',views.article_category_list,name='article_category_list'), #分类文章列表 get
	url(r'^search_category_article/(?P<category_id>\d+)/(?P<page>\d+)/$',views.search_category_article,name='search_category_list'), #搜索分类下的文章 get/post

	################     微信自定义菜单接口结束    ###################

	##############    获取文章资源  开始   #################
	url(r'^get_resource_register/(?P<article_id>\d+)/$',views.get_resource_register), #获取文章资源的注册   get/post
	url(r'^get_resource_user_is_active/(?P<article_id>\d+)/$',views.get_resource_user_is_active), #已注册的用户获取资源

	##############    获取文章资源  结束   #################

	##############    问答3.0版本新增接口 开始   #################
	url(r'^recently_ask_list/(?P<category_id>\d+)/(?P<page>\d+)/$',views.recently_ask_list,name='webapp_recently_ask_list'),# 最新问答列表首页 get
	url(r'^hold_ask_list/(?P<category_id>\d+)/(?P<page>\d+)/$',views.hold_ask_list,name='webapp_hold_ask_list'),#热门问答列表 get
	url(r'^search_ask/(?P<page>\d+)/$',views.search_ask,name='webapp_search_ask'),#搜索 get/post
	url(r'^praise_answer/(?P<answer_id>\d+)/$',views.praise_answer,name='webapp_praise_answer'),#点赞和取消点赞回答 get
	url(r'^question_category_list/$',views.question_category_list,name='webapp_question_category_list'), #问题分类列表 get

	##############    问答3.0版本新增接口 结束   #################

	############## 研究方法、研究进展 接口 开始 ############
	url(r'^banner/$',views.banner), #首页banner get
	url(r'^recently_method_article/$',views.recently_method_article),#首页最新的研究方法 get
	url(r'^recently_ask/$',views.recently_ask),#首页最新的研究问答 get
	url(r'^recently_news/$',views.recently_news),#首页最新的研究进展 get
	url(r'^method_articles/(?P<page>\d+)/(?P<category_id>\d+)/$',views.method_articles), #研究方法文章列表 get
	url(r'^method_category_banner/$',views.method_category_banner), #研究方法分类的banner get
	url(r'^method_topic_list/$',views.method_topic_list),#研究方法专题合集 get
	url(r'^method_topic_detail/(?P<topic_id>\d+)/(?P<page>\d+)/$',views.method_topic_detail), #研究方法专题详情 get
	url(r'^method_topic_article_detail/(?P<article_id>\d+)/$',views.method_topic_article_detail), #研究方法专题文章详情 get
	url(r'^method_article_detail/(?P<article_id>\d+)/$',views.method_article_detail), #研究方法文章详情 get
	url(r'^method_release_ask/$',views.method_release_ask),#研究方法发表问题 get post
	url(r'^method_article_detail_ask_list/(?P<article_id>\d+)/(?P<ask_page>\d+)/$',views.method_article_detail_ask_list),#研究方法文章的问答列表 get
	# url(r'^related_reading_method_article_list/(?P<article_id>\d+)/$',views.related_reading_method_article_list),#研究方法文章的相关阅读文章列表 get
	url(r'^news/(?P<category_id>\d+)/(?P<page>\d+)/$',views.news),#研究进展首页新闻列表 get
	url(r'^news_detail/(?P<news_id>\d+)/(?P<page>\d+)/$',views.news_detail),#研究进展新闻详情 gets
	url(r'^search_article/(?P<section_id>\d+)/(?P<page>\d+)/$',views.search_article),#搜索文章
	url(r'^add_news_comment/(?P<news_id>\d+)/$',views.add_news_comment),#添加研究进展评论 get post
	############## 研究方法、研究进展 接口 结束 ############

]

