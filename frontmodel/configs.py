#coding:utf-8

#非法昵称
ILLEGALITY_NAME = [u'admin',u'supervisor',u'管理员',u'医咖会']

#密码加盐
PASSWORD_SALT = 'sdfdsvcxviewrkfdsfjk;sdfskdf1232344dfjf'

#用户名正则
USERNAME_REGX = r'^[a-zA-Z0-9_-]+$'

#邮箱正则
EMAIL_REGX = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
PHONE_REGX = '^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$'

#微信问题列表翻页
NUM_PAGE = 10

#PC文章列表翻页
PC_FRONT_NUM_PAGE = 20

#科研项目翻页


#PC文章评论列表翻页
PC_FRONT_COMMENT_NUM_PAGE = 5

#管理后台文章翻页
PC_ADMIN_ARTICLE_NUM_PAGE = 20

#问答板块2级评论每页显示条数
ANSWER_NUM_PAGE = 3

#保利威视秘钥
polyv_userid = 'b1e37a1f1a'
polyv_secretkey = 'dZR0fmHHu4'

#模型键值对
model_type = {
	'1': 'methodmodel',
	'2': 'newsmodel',
	'3': 'videomodel',
	'4': 'answersmodel',
	'5': 'questionsmodel',
	'6': 'videocommentmodel',
}


'''
	author:zhangx
	date:20180530

'''


# 支付宝配置
APPID = "2016091100485794"
APP_NOTIFY_URL = "https://zx.evahealth.net/alipay_verify_order/"
REQUEST_TRADE = 'https://openapi.alipay.com/gateway.do'


#定时任务执行时间
ORDER_BEHIND_TIME = 60*60*24
