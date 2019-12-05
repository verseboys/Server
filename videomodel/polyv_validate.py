#coding:utf-8

from frontmodel.models import  FrontUserModel,UserBuyOrderModel
from frontmodel.decorators import front_login_required,front_user_infomation_is_full
from videomodel.models import VideoModel
from frontmodel import configs
import hashlib,json
from django.http import JsonResponse
import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def polyv_response(request, context):
	vid = request.GET.get('vid', '')
	code = request.GET.get('code', '')
	callback = request.GET.get('callback', None)
	t = request.GET.get('t', '')
	secretkey = configs.polyv_secretkey

	str_hash = 'vid={vid}&secretkey={secretkey}&username={username}&code={code}&status={status}&t={t}'.format(
			vid=vid, secretkey=secretkey, username=context.get('username', ''), code=code, status=context['status'], t=t
			)
	sign = hashlib.md5(str_hash).hexdigest().lower()
	context['sign'] = sign

	if callback:
		return HttpResponse("{callback}({json})".format(callback=callback,json=json.dumps(context)), content_type='application/javascript; charset=utf-8')
	return JsonResponse(context)

#保利威视视频授权验证
def polyv_validate(request):
	'''
	授权播放功能接口主要的播放操作是：授权播放，即判断是否允许播放。

	1、用户登录才可以访问
	2、用户资料完整才可以访问
	4、规则
		a、若用户未登录、资料不完善，不可以播放
		b、若视频为收费，需要判断用户是否付费
	'''
	referer = request.META.get('HTTP_REFERER', '')
	if '://www.cardpc.org/' in referer:
		return polyv_validate_for_cardpc(request)

	videoId = request.GET.get('vid',None)
	username = request.GET.get('code', None)
	t = request.GET.get('t', None)
	callback = request.GET.get('callback', None)

	status = 1
	msg = ''
	secretkey = configs.polyv_secretkey
	user = getattr(request, 'front_user', None)

	if user:
		userModel = user
		if userModel.is_active:
			# 判断用户资料是否完整
			if not (userModel.corporation and userModel.profession and userModel.jobtitle):
				context = {
					'status': 2,
					'username': '',
					'msg': u'请先到个人中心补充完善个人资料信息!',
				}
				return polyv_response(request, context)
		else:
			context = {
				'status': 2,
				'username': '',
				'msg': u'此账号已锁定,请联系管理员!',
			}
			return polyv_response(request, context)
	else:
		context = {
			'status': 2,
			'username': '',
			'msg': u'请登录后播放!',
		}
		return polyv_response(request, context)

	#判断视频是否存在，vid的真假只能依靠保利判断
	videoModel = VideoModel.objects.filter(polyv_vid=videoId, status=1).first()

	if videoModel:
		# 判断视频是否收费
		if videoModel.is_pay == 0:
			pass
		elif videoModel.is_pay == 1:
			# 付费课程,判断用户是否已购买该视频
			isOrderModel = UserBuyOrderModel.objects.filter(username=userModel,status=2).all()
			if isOrderModel:
				is_pay =[]
				for i in isOrderModel:
					if i.content_object == videoModel.course.relevance_category:
						is_pay.append(i)

				if not len(is_pay):
					context = {
						'status': 2,
						'username': username,
						'msg': u'请购买后观看!'
					}
					return polyv_response(request, context)
			else:
				context = {
					'status':2,
					'username':username,
					'msg':u'请购买后观看!'
				}
				return polyv_response(request, context)
		else:
			context = {
				'status': 2,
				'username': username,
				'msg': u'此视频正在制作中,暂时不可以播放!',
			}
			return polyv_response(request, context)
	else:
		context = {
			'status': 2,
			'username': username,
			'msg': u'你尝试播放一个不存在的视频!',
		}
		return polyv_response(request, context)

	context = {
		'status':status,
		'username':username,
		'msg':msg,
	}
	return polyv_response(request, context)

def polyv_validate_for_cardpc(request):
	username = request.GET.get('code', '')
	status = 1
	context = {
		'status':status,
		'username':username,
	}
	return polyv_response(request, context)
