#coding:utf-8

from __future__ import unicode_literals

import hashlib
import json
import random
import re
import time

from django.contrib.auth import login, authenticate
from django.core import mail
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from extends import alisms, send_email
from extends.buildjson import json_params_error, json_result, json_method_error
from frontmodel import configs
from frontmodel.decorators import front_login_required
from frontmodel.models import FrontUserModel
from models.network import NetworkMemberB4Account
from yizhu import settings

FRONT_USER_AUTH_BACKEND = 'medieco.backends.FrontUserPasswordAuthenticationBackend'
SMS_TYPE_REGISTER = 'register'
SMS_TYPE_FORGET_PWD = 'forget_pwd'
SMS_TYPE_LOGIN = 'login'
SMS_TYPE_BIND_PHONE = 'bind_phone'

CODE_TYPE_BIND_EMAIL = 'bind_email'

# 正则：手机号（精确） * 移动：134(0-8)、135、136、137、138、139、147、150、151、152、157、158、159、178、182、183、184、187、188、198 *
# 联通：130、131、132、145、155、156、175、176、185、186、166*
# 电信：133、153、173、177、180、181、189、199 *
# 全球星：1349 *
# 虚拟运营商：170
# ---------------------

# TODO 这段代码应该放到一个公共的地方，现在临时拷贝过来使用
# TODO 建议实现默认的sucessResponse errorResponse
class Response(JsonResponse):
    def __init__(self, status=200, code=200, message='', data=None, pagination=None, form_errors=None, event_id=None):
        content = dict(apiVersion='v2', code=code, message=message, data=data)
        if pagination:
            content['pagination'] = pagination
        if event_id:
            content['eventId']= event_id
        if form_errors:
            content['formErrors'] = form_errors
        super(Response, self).__init__(data=content, status=status)

@require_http_methods(['POST'])
def create_user(request):
    """
    POST /users

    文档：https://confluence.natureself.site/pages/viewpage.action?pageId=25624953

    创建用户，支持多种途径创建账号:
        * 激活科研网络开户的账号
        * 用户网站自助注册（暂未实现）

    请求 body：

    {
        'action': 'activate-network-user', // 如果是网站自助注册，为 register

        // 如果 action == activate-network-user
        'code': '...', // 激活开户账号的 code

        // 如果 action == 'register'
        'username': '...',
        'password': '...',
        '...',
    }

    对于激活开户账号的情况：
    响应：200，400，500，其他
    1、如果存在数据结构错误，比如发送的 body 不是有效的 json，或者字段类型有错误，会返回400，message 为错误说明。
       这类问题前端无需展示给客户，这些错误应该只在本地测试的时候发生，正式上线后不允许发生，如果发生，那是前端有bug。
    2、如果用户激活成功，会返回200，message 为成功描述，data 为 user 数据结构
    3、如果激活码此前已经成功激活过，会返回200，内容与2相同（API的调用结果相同，区别是后端不会对数据库写任何东西）
    4、服务器内部发生错误，会返回500
    除 500 外，其他情况下返回的 message 可以直接用于给用户展示。
    """
    try:
        body = json.loads(request.body)
    except:
        return Response(400, code=400, message='无效的请求内容')

    action = body.get('action', None)
    if action == 'activate-network-user':
        return activate_network_user(request, body)
    elif action == 'activate-email':
        return activate_email(request,body)
    else:
        return Response(400, code=400, message='无效的请求')


def activate_email(request,body):
    '''
    用户的邮箱激活
    * 从cache里面验证激活码，失效则return 400
    * 激活码验证成功后，将本地账户邮箱验证状态设置为true （ums考虑在认证时刷新邮箱状态信息）
    TODO 针对用户操作cache最好都放在user_view里面比较合适
    :param request:
    :param body:  code: 存储在cache里面的激活验证码
    :return:
    '''
    code = body.get('code')
    if not code:
        return Response(400, code=400, message='链接已失效')  # body 没有带 code

    email = cache.get(code)
    if not email:
        return Response(400, code=400, message='链接已失效')  # body 没有带 code

    try:
        user = FrontUserModel.objects.get(email=email)
    except FrontUserModel.DoesNotExist:
        return Response(400, code=400, message='用户不存在')
    user.set_email_validated()
    login_by_specific_backend(request, user)
    cache.delete(code)

    return Response(200, code=200, data=user.serialize(), message='邮件激活成功')

# 由于涉及三个表操作，因此必须在一个 transaction 中进行，要么同时失败，要么同时成功
@transaction.atomic()
def activate_network_user(request, body):
    code = body.get('code')
    if not code:
        return Response(400, code=400, message='无效的激活地址') # body 没有带 code

    try:
        b4account = NetworkMemberB4Account.objects.select_related('member', 'member__application').get(code=code)
    except NetworkMemberB4Account.DoesNotExist:
        return Response(400, code=400, message='无效的激活码') # code 不存在

    try:
        user = FrontUserModel.objects.get(email=b4account.member.email)
    except FrontUserModel.DoesNotExist:
        return Response(400, code=400, message='用户不存在')  # user 不存在

    if b4account.used:
        # NOTE 在没有 BUG 的情况下，以下代码不会出错。这个函数是在一个 transaction 中执行的，
        # 因此 self.used_at 会跟 user 同步创建（修改）
        return Response(200, code=200, data=user.serialize(), message="账号已激活")
    member = b4account.member

    user.set_email_validated()
    # 更新 b4account 中的 used_at 字段，用户如果再次访问，则无需重复创建账号
    b4account.used_at = timezone.now()
    b4account.save(update_fields=['used_at'])

    application = member.application
    # status=2 代表已激活，并且使用户具有观看对应课程视频的权限
    application.members.filter(email=member.email).update(status=2, medieco_user_id=user.id)

    return Response(200, code=200, data=user.serialize(), message='账号已激活')

# @deprecated by FrontUserModel._generate_random_username
def generate_random_username():
    #  用户名生成规则要修改为类似于7位16进制规则
    # 用户名为 medi_$N，其中 $N 是 1000000 ～9999999 之间的数字
    return 'medi_' + str(random.randint(1000000, 9999999))

def activation_page(request):
    # TODO 这里实际上并不需要 render，可以直接输出网页
    # 不过由于该项目代码架构的问题，用 render 来输出网页最方便
    return render(request, 'network/account_activation.html')

def activation_email_page(request):
    return render(request, 'email_activation.html')

@require_http_methods(['POST'])
def send_phone_register_code(request):
    '''
    发送手机注册时的验证码，cache存储的key有特定格式，防止串用验证码
    TODO type定义为reigister/forget_pwd/，这样保证一个验证码只能在一个业务流里使用
    '''
    phone = request.POST.get('phone', None)
    if not phone:
        return json_params_error(data={'phone': u'手机号不能为空'})
    if not re.match(configs.PHONE_REGX, phone):
        return json_params_error(data={'phone': u'手机号格式错误'})
    try:
        user = FrontUserModel.objects.get(phone=phone)
        if user:
            return json_params_error(data={'phone': u'该手机号已注册'})
    except FrontUserModel.DoesNotExist:
        pass

    cache_key = hashlib.md5(SMS_TYPE_REGISTER + phone).hexdigest()
    return _send_sms_code(cache_key, phone)


@require_http_methods(['POST'])
def send_phone_login_code(request):
    '''
    发送手机登陆时的验证码
    '''
    phone = request.POST.get('phone', None)
    if not phone:
        return json_params_error(data={'phone': u'手机号不能为空'})
    if not re.match(configs.PHONE_REGX, phone):
        return json_params_error(data={'phone': u'手机号格式错误'})

    cache_key = hashlib.md5(SMS_TYPE_LOGIN + phone).hexdigest()
    return _send_sms_code(cache_key, phone)

@require_http_methods(['POST'])
def send_phone_forget_pwd_code(request):
    '''
    发送手机登陆时的验证码
    '''
    phone = request.POST.get('phone', None)
    if not phone:
        return json_params_error(data={'phone': u'手机号不能为空'})
    if not re.match(configs.PHONE_REGX, phone):
        return json_params_error(data={'phone': u'手机号格式错误'})
    try:
        user = FrontUserModel.objects.get(phone=phone)
    except FrontUserModel.DoesNotExist:
        return json_params_error(data={'phone': u'该手机号未注册'})

    cache_key = hashlib.md5(SMS_TYPE_FORGET_PWD + phone).hexdigest()
    return _send_sms_code(cache_key, phone)


@require_http_methods(['POST'])
@front_login_required
def send_bind_phone_code(request):
    '''
    发送手机绑定时的验证码
    '''
    phone = request.POST.get('phone', None)
    if not phone:
        return json_params_error(message= u'手机号不能为空')
    if not re.match(configs.PHONE_REGX, phone):
        return json_params_error(message=u'手机号格式错误')
    if phone == request.front_user.phone:
        return json_params_error(message=u'请绑定新手机号')
    try:
        user = FrontUserModel.objects.get(phone=phone)
        if user:
            return json_params_error(message=u'手机号已经被使用')
    except FrontUserModel.DoesNotExist:
        pass

    cache_key = hashlib.md5(SMS_TYPE_BIND_PHONE + phone).hexdigest()
    return _send_sms_code(cache_key, phone)


@require_http_methods(['POST'])
@front_login_required
def send_bind_email_code(request):
    '''
    发送邮箱绑定时的验证码
    '''
    email = request.POST.get('email', None)
    if not email:
        return json_params_error(message=u'邮箱不能为空')
    if not re.match(configs.EMAIL_REGX, email):
        return json_params_error(message=u'邮箱格式错误')
    if email == request.front_user.email:
        return json_params_error(message=u'请绑定新邮箱')

    try:
        user = FrontUserModel.objects.get(email=email)
        if user:
            return json_params_error(message=u'邮箱已经被使用')
    except FrontUserModel.DoesNotExist:
        pass

    cache_key = hashlib.md5(CODE_TYPE_BIND_EMAIL + email).hexdigest()
    return _send_email_code(cache_key, email)


def _send_sms_code(cache_key, phone, exipre_second=600):
    # TODO 需要记录单位时间内同一个手机发送的短信次数,现在先由阿里云直接支持，一个小时一个手机号最多5次
    # TODO 暂时只支持同一种短信类型60秒只能获取一次验证码，是否应该支持全局的同一手机号60秒只能获取一次验证码
    stored_value = cache.get(cache_key)
    if stored_value:
        if (timezone.now() - stored_value['send_time']).seconds < 60:
            return json_params_error(data={'phone': u'60秒内只能获取一次验证码'},message=u'60秒内只能获取一次验证码')

    code = alisms.send_verify_code(phone)
    value = dict(code=code, send_time=timezone.now())
    cache.set(cache_key, value, exipre_second)
    if alisms.DRYRUN:
        return Response(200, code=200, message='短信已发送，测试模式：' + code)
    else:
        return Response(200, code=200, message='短信已发送')


def _send_email_code(cache_key, email, exipre_second=600):
    stored_value = cache.get(cache_key)
    if stored_value:
        if (timezone.now() - stored_value['send_time']).seconds < 60:
            return json_params_error(data={'email': u'60秒内只能获取一次验证码'},message=u'60秒内只能获取一次验证码')

    code = ''
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        code += ch

    value = dict(code=code, send_time=timezone.now())
    cache.set(cache_key, value, exipre_second)

    subject = u'[医咖会]-邮箱验证'

    message = u'您好！ 您在{}申请了邮箱验证\n' \
            u'请填写如下6位验证码：\n' \
            u'{}\n' \
            u'验证码在10分钟内有效，10分钟后需要重新发送\n\n' \
            u'此邮件为系统邮件，请勿回复，如您想了解更多内容，欢迎访问我们的网站获取信息'
    time_formated = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime())
    from_email = settings.EMAIL_HOST_USER
    recipinet_list = [email]

    if mail.send_mail(subject, message.format(time_formated, code), from_email, recipinet_list):
        # request.session['email'] = email  # 将邮箱存入缓存
        return Response(200, code=200, message='验证码已发送到你的邮箱')
    else:
        return Response(400, code=400, message='邮件发送失败，请稍后重试')


# 手机短信注册部分业务
@require_http_methods(['GET', 'POST'])
def register_email(request):
    if request.method == 'GET':
        return render(request, 'register_email.html')
    # POST
    phone = request.POST.get('phone', None)
    captcha = request.POST.get('captcha', None)
    password = request.POST.get('password', None)

    if phone is None:
        return json_params_error(data={'phone': u'手机号不能为空'})
    if not password:
        return json_params_error(data={'password': u'密码不能为空!'})
    if len(password) < 4 or len(password) > 16:
        return json_params_error(data={'password': u'请输入4-16位长度的密码!'})
    
    cache_key = hashlib.md5(SMS_TYPE_REGISTER + phone).hexdigest()
    if not cache.get(cache_key):
        return json_params_error(data={'captcha': u'验证码错误'})
    if not captcha:
        return json_params_error(data={'captcha': u'验证码不能为空'})
    # 验证码验证部分
    code = cache.get(cache_key)['code']
    # TODO 需要检查一下cache过期是直接删除还是会返回过期的属性，否则无法判断验证码过期还是没有验证码
    if not code:
        return json_params_error(data={'captcha': u'验证码错误'})
    if code != captcha:
        return json_params_error(data={'captcha': u'验证码错误'})
    try:
        emailModel = FrontUserModel.objects.get(phone=phone)
        return json_params_error(data={'phone': u'此手机已被注册!'})
    except FrontUserModel.DoesNotExist:
        pass

    # 用户名现在不由用户注册时输入，默认生成一个。
    user = FrontUserModel(phone=phone, password=password)
    user.create_user_by_phone()
    login_by_specific_backend(request,user)
    return Response(200, code=200, message='注册成功，请登录')


def login_by_specific_backend(request,user):
    login(request,user,FRONT_USER_AUTH_BACKEND)


# 短信登录
@require_http_methods(['GET', 'POST'])
def phone_login(request):
    if request.method == 'GET':
        return render(request, 'phone_login.html')
    # post短信登录
    phone = request.POST.get('phone', None)
    captcha = request.POST.get('captcha', None)

    cache_key = hashlib.md5(SMS_TYPE_LOGIN + phone).hexdigest()
    if not cache.get(cache_key):
        return json_params_error(data={'captcha': u'验证码错误'})
    code = cache.get(cache_key)['code']
    # TODO 需要检查一下cache过期是直接删除还是会返回过期的属性，否则无法判断验证码过期还是没有验证码
    if not code:
        return json_params_error(data={'captcha': u'验证码错误'})
    if code != captcha:
        return json_params_error(data={'captcha': u'验证码错误'})

    user = authenticate(phone=phone)
    if not user:
        return json_params_error(data={'phone': u'账号或密码错误'})

    # TODO 检查账号是否是用邮箱注册、且没有点击验证链接，这种情况下，
    #      跳转到页面提示用户完成激活
    # if not user.activated:
    #    return redirect(...)

    if not user.is_active:
        return json_params_error(message=u'此用户已被锁定,请联系管理员!')

    login(request, user)
    # 如果有 next，则跳转到 next 页面，否则返回 json 信息
    nexturl = request.GET.get('next')
    if nexturl:
        return redirect(nexturl)
    else:
        context = dict(id=user.id, username=user.username, avatar=user.avatar)
        return json_result(message=u'登录成功!', data=context)


# 手机忘记密码渲染
@require_http_methods(['GET', 'POST'])
def phone_forget_pwd(request):
    if request.method == 'GET':
        return render(request, 'phone_forget_pwd.html')
    # 验证手机号是否和验证码一致，验证码是否有效，密码字符集判断处理，重设密码
    phone = request.POST.get('phone', None)
    captcha = request.POST.get('captcha', None)
    password = request.POST.get('password', None)

    cache_key = hashlib.md5(SMS_TYPE_FORGET_PWD + phone).hexdigest()
    cache_value = cache.get(cache_key)

    if not password:
        return json_params_error(data={'password': u'密码不能为空!'})
    if len(password) < 4 or len(password) > 16:
        return json_params_error(data={'password': u'请输入4-16位长度的密码!'})
    if not cache_value:
        return json_params_error(data={'captcha': u'验证码错误'})
    if not cache_value.has_key('code') or cache_value['code'] != captcha:
        return json_params_error(data={'captcha': u'验证码错误'})
    try:
        user = FrontUserModel.objects.get(phone=phone)
    except FrontUserModel.DoesNotExist:
        return json_params_error(message=u'该账号不存在')

    user.update_password(password)
    login_by_specific_backend(request,user)
    cache.delete(cache_key)
    return json_result(message=u'密码重设成功')


@front_login_required
@require_http_methods(['GET'])
def email_checking(request):
    """
    未验证邮箱的用户登录后跳转该页面。
    """
    if request.method == 'GET':
        return render(request, 'email_checking.html',context=dict(user_email=request.front_user.email))


@require_http_methods(['POST'])
def resend_active_mail(request):
    """
    重新发送激活邮件,支持两种情况：
    登陆的未激活账号重新发送激活邮件：使用request.front_user对象获取邮箱地址
    注册流程中重新发送激活邮件：从post中获取邮箱地址
    """
    if hasattr(request, 'front_user'):
        # 检查cache是否有邮箱激活链接，有则发送cache已有链接，无则发送新的激活链接
        email = request.front_user.email
    else:
        email = request.POST.get('email')
    if not email:
        return json_params_error(message=u'邮箱地址不为空')
        # 查找是否发送过邮箱激活链接，有则重新发送，没有则检查是否有这个账号但是未激活，有则发送激活链接，无则提示未注册。
        # cache里面key是code=md5(time+email)，无法直接通过email查询是否有过邮箱激活链接，所以在
        # cache里面增加一个action+email的缓存，关联到上面code,这样能实现通过email查询当前有无邮件激活链接
    if send_email.send_email_active_mail(request, email):
        return json_result(message=u'激活邮件已发送')
    else:
        return json_method_error(message=u'激活邮件发送失败')


@front_login_required
@require_http_methods(['POST'])
def bing_phone(request):
    """
    绑定新手机,作为登录凭证而存在
    业务流程： 输入新手机号-检查手机是否存在-获取验证码-更换手机号凭证
    此验证码只作为绑定手机业务使用
    手机号要检查是否和当前手机号一致，再检查是否和其他账号的登录凭证冲突
    param phone captcha

    """
    # 验证手机号是否和验证码一致，验证码是否有效，密码字符集判断处理，重设密码
    phone = request.POST.get('phone', None)
    captcha = request.POST.get('captcha', None)

    cache_key = hashlib.md5(SMS_TYPE_BIND_PHONE + phone).hexdigest()
    cache_value = cache.get(cache_key)

    if not cache_value:
        return json_params_error(message=u'验证码错误')
    if not cache_value.has_key('code') or cache_value['code'] != captcha:
        return json_params_error(message=u'验证码错误')

    user = FrontUserModel.objects.filter(pk=request.front_user.id).first()
    user.update_phone(phone)
    cache.delete(cache_key)
    return json_result(message=u'手机绑定成功')


@front_login_required
@require_http_methods(['POST'])
def bind_email(request):
    email = request.POST.get('email', None)
    captcha = request.POST.get('captcha', None)

    cache_key = hashlib.md5(CODE_TYPE_BIND_EMAIL + email).hexdigest()
    cache_value = cache.get(cache_key)

    if not cache_value:
        return json_params_error(message=u'验证码错误')
    if not cache_value.has_key('code') or cache_value['code'] != captcha:
        return json_params_error(message=u'验证码错误')

    user = FrontUserModel.objects.filter(pk=request.front_user.id).first()
    user.update_email(email)
    cache.delete(cache_key)
    return json_result(message=u'邮箱绑定成功')


