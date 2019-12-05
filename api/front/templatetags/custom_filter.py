#coding:utf-8

from django import template
import re

register = template.Library()

@register.filter
def content_img_filter(value):
	regex = '<img\\s*([\\w]*=(\"|\')([^\"\']*)(\"|\')\\s*)*/>'
	try:
		content_filter = re.sub(pattern=regex,repl=u'[图片]',string=value)
	except:
		pass
	return content_filter

# 数字转中文
@register.filter
def number_convert_chinese(value):
	chinese = ['零','一','二','三','四','五','六','七', '八', '九', '十', '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十']
	try:
		convert_chinese = chinese[value]
	except:pass
	return convert_chinese