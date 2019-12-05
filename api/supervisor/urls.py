#coding:utf-8
from django.conf.urls import url
import views

urlpatterns = [

	url(r'^login/$',views.sup_login,name='sup_login'), #登录，get/post
	url(r'^logout/$',views.sup_logout,name='sup_logout'), #退出 get
	url(r'^user_management/(?P<page>\d+)/$',views.user_management,name='user_management'), #用户管理 get
	url(r'^user_detail/(?P<user_id>\d+)/$',views.user_detail,name='user_detail'),#用户详情 get
	url(r'^lock_user/$',views.lock_user,name='lock_user'),#锁定用户 post
	url(r'^search_user/(?P<page>\d+)/$',views.search_user),#搜索用户(昵称搜索)) post
	url(r'^filter_user_date/$',views.filter_user_date),#根据日期区间过滤用户 get
	###########    下面是微信端的接口url   #####################

	url(r'^question_list/(?P<page>\d+)/$',views.question_list,name='question_list'),#问题列表 get
	url(r'^question_detail/(?P<question_id>\d+)/(?P<answer_id>\d+)/(?P<parent_page>\d+)/(?P<child_page>\d+)/$',views.supervisor_question_detail,name='supervisor_question_detail'),#问题详情 get

	url(r'^delete_question/$',views.delete_question,name='delete_question'),#删除问题 post
	url(r'^delete_answer/$',views.delete_answer,name='delete_answer'),#删除回答 post
	url(r'^search_question/$',views.search_question,name='search_question'), #问题搜索 post

	###############  下面是PC端的接口url  ##############
	#url(r'^article_list/(?P<section_id>\d+)/(?P<page>\d+)/$',views.articles_list,name='article_list'), #研究方法管理、研究进展管理列表 支持GET
	#url(r'^search_article/(?P<section_id>\d+)/(?P<page>\d+)/$',views.search_article,name='search_article'), #搜索文章  支持POST
	#url(r'^publish_article/$',views.publish_article,name='publish_article'), #发表文章 支持GET/POST
	#url(r'^edit_article/(?P<article_id>\d+)/$',views.edit_article,name='edit_article'),#编辑文章 支持GET/POST
	#url(r'^delete_article/$',views.delete_article,name='delete_article'),#删除文章 支持POST
	#url(r'^add_tag',views.add_tag,name='add_tag'),#添加标签 支持GET,POST
	#url(r'^delete_tag/$',views.delete_tag,name='delete_tag'),#删除标签 支持POST
	#url(r'^alter_tag/$',views.alter_tag,name='alter_tag'), #修改标签  支持POST
	#url(r'^tag_list/$',views.tag_list,name='tag_list'), #一级标签 支持GET
	#url(r'^relevance_tag/(?P<tag_id>\d+)/$',views.relevance_tag,name='relevance_tag'), #二级标签 支持GET
	# url(r'^comment_list/(?P<page>\d+)/$',views.comment_list,name='comment_list'),#评论管理 支持GET
	# url(r'^delete_comment/$',views.delete_comment,name='delete_comment'),#删除评论  支持GET
	url(r'^search_comment/(?P<page>\d+)/$',views.search_comment,name='search_comment'),#搜索评论 支持POST


	################     微信自定义菜单接口开始    ###################
	url(r'^add_category/$',views.add_category,name='add_category'), # 添加微信自定义菜单分类  get/post
	url(r'^alter_category/(?P<category_id>\d+)/$',views.alter_category,name='alter_category'), #修改分类和摘要 get/post
	#url(r'^delete_category/(?P<category_id>\d+)/$',views.delete_category,name='delete_category'),#删除菜单分类  get
	url(r'^article_category_list/$',views.article_category_list,name='article_category_list'), #菜单分类列表 get
	url(r'^add_article_index/$',views.add_article_index,name='add_article_index'), #添加文章索引 #get/post
	url(r'^alter_article_index/(?P<article_id>\d+)/$',views.alter_article_index,name='alter_article_index'),#修改文章索引  get/post
	url(r'^delete_article_index/(?P<article_id>\d+)/$',views.delete_article_index,name='delete_article_index'), #删除文章索引 get

	url(r'^article_index_list/(?P<page>\d+)/$',views.article_index_list,name='article_index_list'),# 文章列表 get
	url(r'^search_article_index/(?P<page>\d+)/$',views.search_article_index,name='search_article_index'), #搜索文章索引 get/post

	################     微信自定义菜单接口结束    ###################

	############## 问答版块管理接口  开始  ####################

	url(r'^add_question_category/$',views.add_question_category,name='add_question_category'), #添加问答分类和摘要 get/post
	url(r'^alter_question_and_answer_category/(?P<category_id>\d+)/$',views.alter_question_and_answer_category,name='alter_question_and_answer_category'),  #编辑问答分类和摘要 get/post
	url(r'^delete_question_category/(?P<question_category_id>\d+)/$',views.delete_question_category,name='delete_question_category'), #问答分类删除 get
	url(r'^question_category_list/$',views.question_category_list,name='question_category_list'), #问答分类列表展示 get
	url(r'^alter_question/(?P<question_id>\d+)/$',views.alter_question,name='alter_question'), #修改问题  get post
	url(r'^alter_question_category/(?P<question_id>\d+)/(?P<question_category_id>\d+)/$',views.alter_question_category,name='alter_question_category'), #修改问题分类 get
	url(r'^alter_answer/(?P<answer_id>\d+)/$',views.alter_answer,name='alter_answer'), #修改问题的回答 get/post

	############## 问答版块管理接口  结束  ####################

	##############  获取文章资源 开始  #################
	url(r'^get_resource_user_list/(?P<is_send>\d+)/(?P<page>\d+)/$',views.get_resource_user_list),#申请文章资源的用户列表 #get
	url(r'^send_resource',views.send_resource), #发送资源 #get/post
	url(r'^search_get_resource/(?P<page>\d+)/$',views.search_get_resource), #资源分发页面的搜索 get/post
	url(r'^is_send_resource/$',views.is_send_resource),# 资源申请邮件发送状态设置  get/post
	##############  获取文章资源 结束  #################

    ##############研究方法3.0版本接口 开始 ##################
	url(r'^add_method_category/$',views.add_method_category), #添加研究方法文章分类 get /post
	url(r'^alter_method_category/(?P<category_id>\d+)/$',views.alter_method_category), #修改研究方法分类 get /post
	url(r'^add_method_category_banner/(?P<category_id>\d+)/$',views.add_method_category_banner), #给研究方法分类上传banner和链接  get post
	url(r'^delete_method_category_banner/(?P<category_id>\d+)/$',views.delete_method_category_banner),#删除研究方法分类banner和链接  get
	url(r'^method_category_list/(?P<category_is_active>\d+)/$',views.method_category_list),#研究方法分类列表 get
	url(r'^add_method_article_info/$',views.add_method_article_info), #添加研究方法文章标题和属性 get post
	url(r'^alter_method_article/(?P<article_id>\d+)/$', views.alter_method_article),  # 修改研究方法文章标题和属性 get
	url(r'^delete_method_article/(?P<article_id>\d+)/$', views.delete_method_article),  # 删除研究方法文章 get
	url(r'^add_method_article_content/$',views.add_method_article_content), #添加研究方法文章内容 get /post
	url(r'^alter_method_article_content/$',views.alter_method_article_content),#修改研究方法文章内容 get /post
	url(r'^delete_method_article_content/$',views.delete_method_article_content),#删除研究方法文章内容 get /post

	url(r'^method_article_content_sections/$',views.method_article_content_sections),#研究方法文章版块列表 get post
	url(r'^method_articles/(?P<page>\d+)/(?P<category_id>\d+)/$', views.method_articles, name='method_articles'),  # 研究方法首页文章列表/分类文章列表 get
	url(r'^add_method_article_content_section/$',views.add_method_article_content_section),#添加研究方法内容版块 get/post
	url(r'^alter_method_article_content_section/(?P<section_id>\d+)/$',views.alter_method_article_content_section),#修改研究方法内容版块 get post
	url(r'^alter_category_rank/$',views.alter_category_rank), #自定义研究方法分类显示顺序 get post
	#url(r'^alter_category_column/$',views.alter_category_column), #自定义研究方法分类列顺序 get /post
	url(r'^method_article_recommend_list/$',views.method_article_recommend_list), #首页推荐文章列表 get
	url(r'^method_article_recommend_arrange/$',views.method_article_recommend_arrange),#首页推荐文章自定义排序 get /post
	url(r'^cancel_method_article_recommend/(?P<article_id>\d+)/$',views.cancel_method_article_recommend),#添加/取消文章推荐 get
	url(r'^add_related_reading_method_article/(?P<article_id>\d+)/$',views.add_related_reading_method_article),#添加相关阅读文章 post
	url(r'^delete_related_reading_method_article/(?P<article_id>\d+)/$',views.delete_related_reading_method_article),#删除相关阅读文章 get/post
	url(r'^related_reading_method_article_list/(?P<article_id>\d+)/$',views.related_reading_method_article_list),#相关阅读文章列表 post
	url(r'^alter_related_reading_method_article_arrange/(?P<article_id>\d+)/$',views.alter_related_reading_method_article_arrange),#自定义相关阅读文章排序 get /post
	url(r'^upload_method_banner/$',views.upload_method_banner), #上传banner get /post
	url(r'^alter_method_banner_rank/$',views.alter_method_banner_rank),#自定义banner显示顺序 get /post
	url(r'^is_active_method_banner/$',views.is_active_method_banner), #是否显示banner get /post
	url(r'^delete_method_banner/$',views.delete_method_banner),#删除banner get /post
	url(r'^method_banner_list/$', views.method_banner_list),  # banner列表 get
	url(r'^method_banner_type/(?P<id>\d+)/$',views.method_banner_type), #修改banner类型 get  post
	url(r'^search_method_article/(?P<page>\d+)/(?P<category_id>\d+)/$',views.search_method_article),#搜索研究方法文章 get post

	##############研究方法3.0版本接口 结束 ##################

	##############研究方法专题接口 开始 ##################
	url(r'^add_method_article_topic/$',views.add_method_article_topic), #添加专题 get post
	url(r'^alter_method_article_topic/(?P<topic_id>\d+)/$',views.alter_method_article_topic),#修改专题 get post
	url(r'^delete_method_article_topic/$',views.delete_method_article_topic), #删除专题 get post
	url(r'^method_article_topic_list/(?P<page>\d+)/$',views.method_article_topic_list),#专题列表 get
	url(r'^add_topic_related_method_article/$',views.add_topic_related_method_article),#给专题添加相关文章 get
	url(r'^delete_topic_related_method_article/$',views.delete_topic_related_method_article),#删除专题相关文章 get
	url(r'^alter_method_article_arrange/(?P<topic_id>\d+)/$',views.alter_method_article_arrange),#专题相关文章自定义排序 get post
	url(r'^topic_related_method_article_list/(?P<topic_id>\d+)/$',views.topic_related_method_article_list),#专题相关文章列表 get
	url(r'^search_topic_related_method_article/(?P<page>\d+)/$',views.search_topic_related_method_article), #专题搜索

	###############20180314 提问关键词检索接口#########################
	url(r'^add_key_word_group/$',views.add_key_word_group),#创建搜索关键词分组 get post
	url(r'^alter_key_word_group_name/(?P<group_id>\d+)/$',views.alter_key_word_group_name),#修改关键词分组名称 get post
	url(r'^add_key_word/(?P<group_id>\d+)/$',views.add_key_word),#添加关键词 get post
	url(r'^delete_key_word/(?P<key_word_id>\d+)/$',views.delete_key_word),#删除关键词 get post
	url(r'^add_key_word_group_relevance_article/(?P<group_id>\d+)/$',views.add_key_word_group_relevance_article),#给分组添加关联文章 get post
	url(r'^delete_key_word_group_relevance_article/(?P<group_id>\d+)/$',views.delete_key_word_group_relevance_article),#删除分组下的关联文章 get post
	url(r'^delete_key_word_group/(?P<group_id>\d+)/$',views.delete_key_word_group),#删除关键词分组数据 get post
	url(r'^key_word_groups/(?P<page>\d+)/$',views.key_word_groups),#关键词分组数据列表 get
	url(r'^search_key_word_articles/$',views.search_key_word_articles),#搜索关键词文章 get post
	url(r'^search_key_word/(?P<page>\d+)/$',views.search_key_word),#搜索关键词 get post

	##############研究方法专题接口 结束 ##################

	############## 研究进展接口 开始 #####################
	url(r'^add_news_category/$',views.add_news_category),#添加研究进展分类 get post
	url(r'^alter_news_category/(?P<category_id>\d+)/$',views.alter_news_category),#修改研究进展分类 get post
	url(r'^news_category_list',views.news_category_list),#研究进展分类列表 get
	url(r'^add_news/$',views.add_news),#添加研究进展文章 get post
	url(r'^alter_news/(?P<news_id>\d+)/$',views.alter_news),#修改研究进展文章 get post
	url(r'^delete_news/(?P<news_id>\d+)/$',views.delete_news),#删除研究进展文章 get
	url(r'^news/(?P<page>\d+)/(?P<category_id>\d+)/$',views.news),#研究进展文章列表 get
	url(r'^add_hold_news/(?P<news_id>\d+)/(?P<type_id>\d+)/$',views.add_hold_news),#添加研究进展热门文章 get
	url(r'^delete_hold_news/(?P<news_id>\d+)/(?P<type_id>\d+)/$',views.delete_hold_news),#删除研究进展热门文章 get
	url(r'^hold_news/(?P<type_id>\d+)/$',views.hold_news),#研究进展热门文章列表 get
	url(r'^add_news_related_reading_articles/(?P<news_id>\d+)/(?P<article_id>\d+)/(?P<type_id>\d+)/$',views.add_news_related_reading_articles),#添加研究进展相关阅读 get
	url(r'^delete_news_related_reading/(?P<news_related_reading_id>\d+)/$',views.delete_news_related_reading),#删除研究进展相关阅读 get
	url(r'^news_related_reading_article_list/(?P<news_id>\d+)/$',views.news_related_reading_article_list),#研究进展相关阅读文章列表 get
	url(r'^search_news/(?P<page>\d+)/$',views.search_news),#搜索研究进展文章 get post
	url(r'^search_methods_and_news_articles/(?P<page>\d+)/$',views.search_methods_and_news_articles),#搜索研究方法和研究进展文章 get post
	url(r'^search_methods_and_news_articles/(?P<page>\d+)/$',views.search_methods_and_news_articles),#搜索研究方法和研究进展文章 get post

	url(r'^news_comments/(?P<page>\d+)/$',views.news_comments),#研究进展评论列表 get
	url(r'^delete_news_comment/$',views.delete_news_comment), #删除研究进展评论 post
	############## 研究进展接口 结束 #####################

	##############视频模块接口 开始 ##################
	url(r'^add_course/$',views.add_course),#添加视频课程  get post
	url(r'^alter_course/(?P<course_id>\d+)/$',views.alter_course), #修改课程信息 get post
	url(r'^course_list/$',views.course_list), #课程列表 get
	url(r'^course_section/$',views.course_section), #课程章节列表 get
	url(r'^course_video/(?P<course_id>\d+)/$',views.course_video),#章节关联的课时视频列表 get
	url(r'^add_video/$',views.add_video), #添加视频信息 get  post
	url(r'^alter_video/(?P<video_id>\d+)/$',views.alter_video), #修改视频信息  get post
	url(r'^delete_video/(?P<video_id>\d+)/$',views.delete_video),# 删除视频 get
	url(r'^delete_video_related_data/(?P<video_data_id>\d+)/$',views.delete_video_related_data), #删除视频相关资料 get
	url(r'^video_comments/(?P<page>\d+)/$',views.video_comments),#视频评论列表 get
	url(r'^delete_video_comment/(?P<comment_id>\d+)/$',views.delete_video_comment), #删除视频评论 get
	url(r'^search_video_comment/(?P<page>\d+)/$',views.search_video_comment),#搜索视频评论 get post

	##############视频模块接口 结束 ##################


	############## 订单交易列表 get ####################
	url(r'^order_list/(?P<page>\d+)/$',views.order_list), #订单交易列表 get
	url(r'^search_order/(?P<page>\d+)/$',views.search_order), #订单查询 get  post
	url(r'^supervisor_alipay_order_status/(?P<order_id>\d+)/$',views.supervisor_alipay_order_status),# 支付宝订单状态校验 get
	url(r'^user_feed_back/(?P<page>\d+)/$',views.user_feed_back), #用户意见反馈列表 get
	url(r'^user_feed_back_detail/(?P<id>\d+)/$',views.user_feed_back_detail),#意见反馈详情
	############## 订单交易列表 结束 ####################


	################# 周年活动接口 #####################
	url(r'^get_medal/$',views.get_medal),#获取勋章列表
	url(r'^get_user_medal/$',views.get_user_medal),#获取用户勋章信息
	url(r'^add_medal/$',views.add_medal),#添加勋章
	url(r'^delete_medal/$',views.delete_medal),#删除勋章
	url(r'^get_activity_comments/(?P<topic_type>\w+)/(?P<page>\d+)/(?P<pagesize>\d+)/(?P<show_which>\d+)/$',views.get_activity_comments),#获取留言列表
	url(r'^change_activity_comment_state/(?P<comment_id>\d+)/(?P<state>\d+)/$',views.change_activity_comment_state),#修改留言展示状态 并获得活动积极者勋章
	url(r'^get_sci_member/(?P<anniversary_times>\d+)/$',views.get_sci_member),#获取sci成员信息
	url(r'^get_friend_member/(?P<anniversary_times>\d+)/$',views.get_friend_member),#获取医咖会朋友成员信息
	url(r'^disable_user_medal/(?P<medal_type>\w+)/(?P<user_id>\d+)/$',views.disable_user_medal),#剥夺用户勋章
	url(r'^restore_user_medal/(?P<medal_type>\w+)/(?P<user_id>\d+)/$',views.restore_user_medal),#恢复用户勋章
	url(r'^reply_user_comment/$',views.reply_user_comment),#留言回复
	################# 周年活动接口 结束 #################

]

