# coding:utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

import network_views
import study_views
import user_views
import views

urlpatterns = [
    # 20180305 登录注册页面模板渲染，解决显示屏太小导致浮层形式的注册登录页面显示不全的问题
    url(r'^login/', views.f_login, name='front_login'),  # 登录页面模板渲染
    url(r'^register/', views.f_register, name='front_register'),  # 注册页面模板渲染
    url(r'^register_email/', user_views.register_email, name='register_email'),  # 邮箱注册页面模板渲染
    url(r'^phone_login/', user_views.phone_login, name='phone_login'), # 短信登录get post
    url(r'^phone_forget_pwd/', user_views.phone_forget_pwd, name='phone_forget_pwd'), # 手机忘记密码get post
    url(r'^recover_password/(?P<code>[\w\d]+)/$', views.recover_password, name='recover_password'), # 找回密码模板渲染
    #########################################
    url(r'^front_register/$', views.register),  # 注册 get/post
    url(r'^front_login/$', views.front_login),  # 登录 get/post
    url(r'^logout/$', views.front_logout, name='front_logout'),  # 退出 get/post
    url(r'^logout_network/$', views.front_logout_network, name='front_logout_network'),  # 慢阻肺专项退出登录 get/post
    url(r'^register_send_email/$', views.register_send_email, name='front_register_send_email'),  # 给邮箱发送验证码 get
    url(r'^resend_active_mail/$', user_views.resend_active_mail, name='resend_active_mail'),  # 重发激活邮件 post
    url(r'^users/email_activation.html$', user_views.activation_email_page, name='email_activation'),
    url(r'^send_phone_register_code/', user_views.send_phone_register_code),
    url(r'^send_phone_login_code/', user_views.send_phone_login_code),
    url(r'^send_phone_forget_pwd_code/', user_views.send_phone_forget_pwd_code),
    url(r'^send_bind_phone_code/', user_views.send_bind_phone_code),
    url(r'^send_bind_email_code/', user_views.send_bind_email_code),


    url(r'^forget_password/$', views.forget_password, name='front_forget_password'),  # 忘记密码 post
    url(r'^check_email/(?P<code>[\w\d]+)/$', views.check_email, name='front_check_email'),  # 忘记密码检查邮箱 get
    url(r'^email_checking/$', user_views.email_checking, name='email_checking'),  # 邮箱激活单独页面 get/post
    url(r'^reset_password/$', views.reset_password, name='front_reset_password'),  # 修改密码  get/post
    url(r'^bind_phone/$', user_views.bing_phone, name='bind_phone'),  # 绑定手机  get/post
    url(r'^bind_email/$', user_views.bind_email, name='bind_email'),  # 绑定邮箱  get/post
    url(r'^front_professional_sections/(?P<department_id>\d+)/$', views.front_professional_sections,
        name='front_professional_sections'),
    # 专业科室 get
    url(r'^front_job_title/(?P<job_id>\d+)/$', views.front_job_title, name='front_job_title'),  # 专业职称 get
    url(r'^user_info/$', views.user_info, name='front_user_info'),  # 个人信息中心  get/post
    # url(r'^news/(?P<section_id>\d+)/(?P<page>\d+)/$',views.study_evolve,name='front_study_evolve'), #研究进展 get
    # url(r'^article_detail/(?P<article_id>\d+)/$',views.article_detail,name='front_article_detail'), #文章详情 get
    # url(r'^add_comment/$',views.add_comment,name='front_add_comment'), #发表评论 get/post
    url(r'^hot_articles/$', views.hot_articles, name='front_hot_article'),  # 热门文章
    url(r'^search_article/(?P<section_id>\d+)/(?P<time_id>\d+)/(?P<page>\d+)/$', views.search_article,
        name='front_search_article'),
    # 搜索文章,研究方法 post
    url(r'^search_articles/', views.search_articles, name='front_search_articles'),  # new 搜索文章,研究方法 post
    # url(r'^search_tag_article/(?P<tag_id>\d+)/(?P<page>\d+)/$',views.search_tag_article,name='front_search_tag_article'), #按标签检索文章 get

    ############## 问答版块管理接口  开始  ####################
    url(r'^my_messages_info/$', views.my_messages_info, name='header_base'),  # 我的消息通知列表 get
    url(r'^delete_my_messages_info/$', views.delete_my_messages_info, name='front_delete_my_messages_info'),
    # 一键清空未读消息列表 get
    url(r'^front_question_category_list/$', views.front_question_category_list, name='front_question_category_list'),
    # 发表问题窗口的分类列表
    url(r'^recently_questions/(?P<category_id>\d+)/(?P<page>\d+)/$', views.recently_questions,
        name='front_recently_questions'),
    # 最新问答 get
    url(r'^hold_questions/(?P<category_id>\d+)/(?P<page>\d+)/$', views.hold_questions, name='front_hold_questions'),
    # 热门问答 get
    url(r'^wait_relay_questions/(?P<category_id>\d+)/(?P<page>\d+)/$', views.wait_relay_questions,
        name='front_wait_relay_questions'),  # 等待回答 get
    url(r'^front_release_question/$', views.front_release_question, name='front_release_question'),  # 发布问题 post
    url(r'^front_add_answer/$', views.front_add_answer, name='front_add_answer'),  # 发表评论 get/post
    url(r'^active_users_ranking/(?P<category_id>\d+)/(?P<time_id>\d+)/$', views.active_users_ranking,
        name='front_active_users_ranking'),  # 活跃用户排行榜 get
    url(r'^question_detail/(?P<question_id>\d+)/(?P<answer_id>\d+)/(?P<parent_page>\d+)/(?P<child_page>\d+)/$',
        views.front_question_detail, name='front_question_detail'),  # 问题详情 get
    url(r'^about_us/$', views.about_us, name='about_us'),  # 关于我们
    url(r'^science/$', views.science, name='science'),  # 学术服务
    url(r'^search_questions_and_answers/(?P<section_id>\d+)/(?P<time>\d+)/(?P<page>\d+)/$',
        views.search_questions_and_answers, name='search_questions_and_answers'),
    # 问答搜索 POST
    url(r'^search_questions/', views.search_questions, name='search_questions'),  # new 问答搜索 POST
    url(r'^search/$', views.search, name='search'),  # 搜索页面

    ############## 问答版块管理接口  结束  ####################

    ############## 个人中心接口  开始  ####################
    url(r'^user/$', views.user, name='front_user'),
    url(r'^collect_answer/(?P<answer_id>\d+)/(?P<collect_category_id>\d+)/$', views.collect_answer,
        name='front_collect_answer$'),
    # 收藏回答和取消收藏回答  get
    url(r'^praise_answer/(?P<answer_id>\d+)/$', views.praise_answer, name='front_praise_answer'),  # 点赞回答和取消点赞回答 get
    url(r'^create_user_collect_category/$', views.create_user_collect_category,
        name='front_cteate_user_collect_category'),
    # 用户创建收藏夹分类  get post
    url(r'^user_collect_category_list/$', views.user_collect_category_list, name='front_user_collect_category_list'),
    # 用户收藏夹分类列表 get post
    url(r'^alter_collect_category/(?P<collect_category_id>\d+)/$', views.alter_collect_category,
        name='front_alter_collect_category'),
    # 修改个人收藏夹 get post
    url(r'^delete_collect_category/(?P<collect_category_id>\d+)/$', views.delete_collect_category),  # 删除个人收藏夹  get
    url(r'^my_attention_questions/(?P<page>\d+)/$', views.my_attention_questions, name='front_my_attention_questions'),
    # 我关注的问题 get
    url(r'^attention_question/(?P<question_id>\d+)/$', views.attention_question, name='front_attention_question'),
    # 关注问题和取消关注问题 get
    url(r'^my_answers/(?P<page>\d+)/$', views.my_answers, name='front_my_answers'),  # 我的回答 get
    url(r'^my_collect/(?P<user_collect_category_id>\d+)/(?P<page>\d+)/$', views.my_collect, name='front_my_collect'),
    # 我的收藏 get
    url(r'^my_questions/(?P<page>\d+)/$', views.my_questions, name='front_my_questions'),  # 我的提问 get
    url(r'^my_messages/(?P<page>\d+)/$', views.my_messages),  # 我的消息 get

    ############## 个人中心接口  结束  ####################

    ############## 研究方法3.0版本接口 开始 #############
    url(r'^method_category_and_article_title/$', views.method_category_and_article_title,
        name='method_category_and_article_title'),
    # 研究方法分类列表和文章标题 get
    url(r'^method_article_detail/(?P<article_id>\d+)/$', views.front_method_article_detail,
        name='front_method_article_detail'),
    # 研究方法文章详情 get
    url(r'^method_article_detail_ask_list/(?P<article_id>\d+)/(?P<ask_page>\d+)/$',
        views.method_article_detail_ask_list, name='front_method_article_detail_ask_list'),
    # 研究方法文章详情的问答列表 get
    url(r'^$', views.method_articles, name='front_method'),  # 研究方法首页文章列表、分类列表，不带参数的，作为首页
    url(r'^method/(?P<page>\d+)/(?P<category_id>\d+)/$', views.method_articles, name='front_method_articles'),
    # 研究方法首页文章列表/分类文章列表 get
    url(r'^method_banner_list/$', views.method_banner_list, name='front_method_banner_list'),  # banner列表 get
    url(r'^related_reading_method_article_list/(?P<article_id>\d+)/$', views.related_reading_method_article_list,
        name='front_related_reading_method_article_list'),  # 相关阅读文章列表 post
    url(r'^download_article/(?P<article_id>\d+)/(?P<type_id>\d+)/(?P<file_id>\d+)/$', views.download_article,
        name='front_download_article'),  # 研究方法下载文章 get

    ############## 研究方法3.0版本接口 结束 #############

    ##############研究方法专题接口 开始 ##################
    url(r'^method_topic_list/$', views.method_topic_list),  # 专题列表 get
    url(r'^method_topic/(?P<page>\d+)/$', views.method_topic, name='front_method_topic'),  # 所有专题相关文章列表  get
    url(r'^method_topic_detail/(?P<topic_id>\d+)/(?P<page>\d+)/$', views.method_topic_detail,
        name='front_method_topic_detail'),
    # 专题详情 get
    url(r'^method_topic_article_detail/(?P<article_id>\d+)/$', views.method_topic_article_detail,
        name='front_method_topic_article_detail'),
    # 专题文章详情 get
    ##############研究方法专题接口 结束 ##################

    ###############20180314 提问关键词检索接口#############
    url(r'^search_key_word/$', views.search_key_word),  # 提问关键词检索 get post
    url(r'^ask_question/$', views.ask_question, name='front_ask_question'),  # 提问页面渲染 get

    ##############研究进展接口 开始 ##################
    url(r'^hold_news/(?P<type_id>\d+)/$', views.hold_news, name='front_hold_news'),  # 研究进展热门推荐列表 get
    url(r'^news_category_list', views.news_category_list, name='front_news_category_list'),  # 研究进展新闻分类列表 get
    url(r'^news/(?P<page>\d+)/(?P<category_id>\d+)/$', views.news, name='front_news'),  # 研究进展 新闻列表 get
    url(r'^news_detail/(?P<news_id>\d+)/(?P<page>\d+)/$', views.news_detail, name='front_news_detail'),  # 研究进展新闻详情 get
    # url(r'^news_comment_list/(?P<news_id>\d+)/(?P<page>\d+)/$',views.news_comment_list,name='front_news_comment_list'),#研究进展新闻评论列表 get
    url(r'^news_related_reading_list/(?P<news_id>\d+)/$', views.news_related_reading_list,
        name='front_news_related_reading_list'),
    # 研究进展相关阅读新闻列表 get
    url(r'^add_news_comment/(?P<news_id>\d+)/$', views.add_news_comment, name='front_add_news_comment'),  # 研究进展添加评论 get
    url(r'^download_news/(?P<news_id>\d+)/$', views.download_news, name='front_download_news'),  # 下载研究进展新闻 get

    ##############研究进展接口 结束 ##################

    ##############视频模块接口 开始 ##################

    url(r'^crossdomain\.xml$', TemplateView.as_view(template_name='crossdomain.xml', content_type='text/xml')),
    url(r'^video_validate/$', views.video_validate),  # 视频授权验证 get

    url(r'^video_detail/(?P<video_id>\d+)/$', views.video_detail, name='video_detail'),  # 视频课程详情 get
    url(r'^course_section/(?P<video_id>\d+)/$', views.course_section),  # 课程目录 get
    url(r'^video_comment/(?P<video_id>\d+)/(?P<page>\d+)/$', views.video_comment),  # 视频评论列表 get
    url(r'^add_video_comment/$', views.add_video_comment),  # 添加视频评论 get
    url(r'^front_favorites/(?P<id>\d+)/(?P<collect_category_id>\d+)/(?P<type_id>\d+)/$', views.front_favorites),
    # 收藏/取消收藏(可收藏视频、文章等) get
    url(r'^praise/(?P<id>\d+)/(?P<type_id>\d+)/', views.front_user_praise),  # 点赞/取消攒点 GET

    ##############视频模块接口 结束 ##################

    #################支付订单接口 开始 ##########################
    url(r'^create_orders/(?P<order_id>\d+)/$', views.create_orders),  # 创建订单 get post
    url(r'^pay_orders/$', views.pay_orders),  # 提交预支付订单 post
    url(r'^alipay_verify_order/$', views.alipay_verify_order),  # 支付宝异步回调 get post
    url(r'^alipay_order_status/(?P<order_id>\d+)/$', views.alipay_order_status),  # 支付宝订单支付状态手动校验
    url(r'^my_orders/(?P<status>\d+)/$', views.my_orders),  # 个人中心-我的订单 get
    url(r'^use_feed_back/$', views.user_feed_back),  # 意见反馈 get post
    url(r'^front_create_orders/$', views.front_create_orders),  # 创建订单页面渲染 get post
    url(r'^feed_back/$', views.front_user_feed_back),  # 用户意见反馈页面渲染 get
    #################支付订单接口 结束 ##########################

    ################# 功能型接口 #####################
    url(r'^user_message_complete/$', views.user_message_complete),
    # 单独校验用户信息是否完整(直接使用下载文件时的检验，会由于ajax不支持流式数据导致一次多余下载) get
    url(r'^is_user_login/$', views.is_user_login),  # 判定用户登录状态
    ################# 功能型接口 结束 #################

    ################# 周年活动页面接口 #####################
    # url(r'^anniversary_comment/$',views.anniversary_comment), #用户获得某一勋章 post
    ################# 周年活动页面接口结束 #####################

    ################# 周年活动ajax接口 #####################
    url(r'^get_achievemnet/$', views.get_achievement),  # 用户获得某一勋章 post
    url(r'^add_activity_comments/$', views.add_activity_comments),  # 用户提交周年活动留言 post
    url(r'^activity_comment_like/(?P<comment_id>\d+)/$', views.activity_comment_like),  # 周年活动留言点赞 get
    url(r'^get_achievements/$', views.get_achievements),  # 获取用户勋章信息 get
    # url(r'^get_achievement_message/(?P<uid>\w+)/$',views.get_achievement_message), TODO:#获取用户某一勋章信息 get
    url(r'^get_activity_comments/(?P<topic_type>\w+)/(?P<page>\d+)/(?P<pagesize>\d+)/$', views.get_activity_comments),
    # 获取展示的话题留言列表 get
    url(r'^already_join_anniversary/$', views.already_join_anniversary),  # 判定用户是否已经参与过活动 get
    ################# 周年活动ajax接口 结束 #################

    ##项目路由
    url(r'^studies/$', study_views.studies, name='edc_studies'),
    url(r'^studies/(?P<study_id>\d+)', study_views.study, name='edc_study'),

    # 科研网络
    url(r'^networks/$', RedirectView.as_view(url='/networks/1/home'), name='front_network'), # 添加 name 是解决慢阻肺专项退出账号 在views.py 
    url(r'^networks/(?P<network_id>\d+)/$', RedirectView.as_view(url='/networks/1/home'), name='network'),
    url(r'^networks/(?P<network_id>\d+)/apply/$', network_views.apply, name='network_apply'),
    url(r'^networks/(?P<network_id>\d+)/apply/success/$', network_views.apply_success, name='network_apply_success'),
    url(r'^networks/(?P<network_id>\d+)/courses/(?P<course_id>\d+)/$', network_views.course, name='network_course'),
    url(r'^networks/(?P<network_id>\d+)/courses/(?P<course_id>\d+)/videos/(?P<video_id>\d+)/$',
        network_views.course_video, name='network_course_video'),
    url(r'^networks/(?P<network_id>\d+)/courses/(?P<course_id>\d+)/videos/(?P<video_id>\d+)/watch$',
        network_views.watch_video, name='network_watch_video'),
    url(r'^networks/(?P<network_id>\d+)/notices/(?P<notice_id>\d+)/$', network_views.notice, name='network_notice'),
    # 公告的统计后续版本实现
    # url(r'^networks/(?P<network_id>\d+)/notices/(?P<notice_id>\d+)/(?P<action>\w+)/$', network_views.stat_notice, name='network_stat_notice'),

    # 科研网络-慢阻肺改版
    url(r'^networks/(?P<network_id>\d+)/home/$', network_views.page_home, name='page_network_home'),
    url(r'^networks/(?P<network_id>\d+)/studies/$', network_views.page_studies, name='page_network_studies'),
    url(r'^networks/(?P<network_id>\d+)/courses/', network_views.page_courses, name='page_network_courses'),
    url(r'^networks/(?P<network_id>\d+)/notices/$', network_views.page_notices, name='page_network_notices'),
    url(r'^networks/(?P<network_id>\d+)/about/$', network_views.page_about, name='page_network_about'),

    url(r'^users$', user_views.create_user, name='create_user'),
    url(r'^users/activation.html$', user_views.activation_page),
]
