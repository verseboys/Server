#coding:utf-8
#Author :zhangx

'''
	构建验证码
'''
import random
import string
import sys
import math
#Image：是一个画板(context),ImageDraw：是一个画笔，ImageFont：画笔的字体
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from django.conf import settings
from django.core.cache import cache

#Captcha验证码
class Captcha(object):
	#把一些常量抽取成类属性
	#字体的位置
	font_path = 'extends/captcha/verdana.ttf'
	#生成几位数的验证码
	number = 4
	#生成验证码图片的宽度和高度
	size = (100,30)
	#背景颜色,默认是白色 RGB
	bgcolor = (255,255,255)
	#字体颜色,默认为蓝色
	fontcolor = (random.randint(0,100),random.randint(0,100),random.randint(0,100))
	#验证码字体大小
	fontsize = 25
	#干扰线颜色。默认为红色
	linecolor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
	#是否需要加入干扰线
	draw_line = True
	#是否绘制干扰点
	draw_point = True
	#加入干扰线的条数
	line_number = 2
	
	#用来随机生成一个字符串(包括英文和数字)
	#定义成类方法,然后是私有的,对象在外面不能直接调用
	@classmethod
	def __gene_text(cls):
		source = list(string.letters)
		for index in range(0,10):
			source.append(str(index))
		#random.sample(sequence,k)#从指定序列中随机获取指定长度的片段。sample不会修改原有序列。
		return ''.join(random.sample(source,cls.number))
	
	#用来绘制干扰线
	@classmethod
	def __gene_line(cls,draw,width,height):
		begin = (random.randint(0,width),random.randint(0,height))
		end = (random.randint(0,width),random.randint(0,height))
		draw.line([begin,end],fill=cls.linecolor)
	
	#用来绘制干扰点
	@classmethod
	def __gene_points(cls,draw,point_chance,width,height):
		chance = min(100,max(0,int(point_chance))) #大小限制在[0,100]
		for w in xrange(width):
			for h in xrange(height):
				tmp = random.randint(0,100)
				if tmp > 100 - chance:
					draw.point((w,h),fill=(0,0,0))
					
	#生成验证码
	@classmethod
	def gene_code(cls):
		width,height = cls.size #宽和高
		image = Image.new('RGBA',(width,height),cls.bgcolor)#创建图片
		font = ImageFont.truetype(cls.font_path,cls.fontsize)#验证码字体
		draw = ImageDraw.Draw(image) #创建画笔
		text = cls.__gene_text()#生成字符串
		font_width,font_height = font.getsize(text)
		draw.text(((width - font_width)/2,(height - font_height)/2),text,font=font,fill=cls.fontcolor) #填充字符串
		#如果需要绘制干扰线
		if cls.draw_line:
			#遍历line_number次,就是画line_number根线条
			for x in xrange(0,cls.line_number):
				cls.__gene_line(draw,width,height)
		
		#如果需要绘制噪点
		if cls.draw_point:
			cls.__gene_points(draw,10,width,height)
		#保存到缓存中,过期时间为2分钟
		#cache.set(text.lower(),text.lower(),120)
		return (text,image)
	

		
				
	
	