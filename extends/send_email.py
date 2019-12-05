# coding:utf-8

import hashlib
import time
from django.utils import timezone
from django.conf import settings
from django.core import mail
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.shortcuts import reverse

from extends.buildjson import json_params_error, json_result

EMAIL_TYPE_VALIDATE = 'email_validate'
EMAIL_TYPE_FORGET = 'email_forget'

# 发送普通邮件
def send_forget_password_email(request, email, check_url, subject=None, message=None, expire_second=600):
    key_find_code = hashlib.md5(EMAIL_TYPE_FORGET + email).hexdigest()
    # TODO 可以和send_email_active_mail里面同样的逻辑合并起来
    key_code = cache.get(key_find_code)
    if key_code:
        cache.set(key_find_code, key_code, expire_second)
        cache.set(key_code, email, expire_second)
    else:
        key_code = hashlib.md5(EMAIL_TYPE_FORGET + str(time.time()) + email).hexdigest()
        cache.set(key_find_code, key_code, expire_second)
        cache.set(key_code, email, expire_second)

    url = request.scheme + '://' + request.get_host() + reverse(check_url, kwargs={'code': key_code})

    # 发送邮件到email邮箱
    if not subject:
        subject = u'[医咖会]-邮箱验证'
    else:
        subject = subject

    # message中包含验证的链接
    if not message:
        message = u'这是来自[医咖会]的注册邮件,请点击: ' + url + u' ,请在10分钟内完成验证。'
    else:
        message = message['first_content'] + url
    message += u' \n此邮件为系统邮件请勿回复，如您想了解更多内容，欢迎访问我们的网站获取信息。'
    from_mail = settings.EMAIL_HOST_USER
    recipinet_list = [email]
    try:
        if mail.send_mail(subject, message, from_mail, recipinet_list):
            return True
        else:
            return False
    except Exception:
        raise



def send_email_active_mail(request, email):
    '''
    生成激活码，发送账户激活邮件
    如果存在上一个激活码，那么重新发送，如果不存在，那么发送新激活邮件
    cache_key_validate是为了方便查找到上次的激活码
    TODO 应该限制单位时间内发送的邮件次数
    '''
    key_find_code = hashlib.md5(EMAIL_TYPE_VALIDATE + email).hexdigest()
    key_code = cache.get(key_find_code)
    if key_code:
        # 重置激活有效期
        cache.set(key_code, email, 86400)
        cache.set(key_find_code, key_code, 86400)
    else:
        key_code = hashlib.md5(EMAIL_TYPE_VALIDATE + str(time.time()) + email).hexdigest()
        cache.set(key_code, email, 86400)
        cache.set(key_find_code, key_code, 86400)

    url = request.scheme + '://' + request.get_host() + '/users/email_activation.html?code='+key_code

    # 发送邮件到email邮箱
    subject = u'[医咖会]-注册确认'

    message = u'你好!\n感谢你注册医咖会，请在24h内点击以下链接完成注册： ' + url
    message += u'\n如你未注册该网站，请忽略此邮件。'
    message += u' \n此邮件为系统邮件请勿回复，如您想了解更多内容，欢迎访问我们的网站获取信息。'
    from_mail = settings.EMAIL_HOST_USER
    recipinet_list = [email]
    try:
        if mail.send_mail(subject, message, from_mail, recipinet_list):
            return True
        else:
            return False
    except Exception:
        raise

# 发送带附件的邮件
def send_attach_email(request, email_list, subject=None, body=None, file_path=None):
    if not subject:
        subject = u'【医咖会】-申请的资源文章已审核通过'
    else:
        subject = subject
    if not body:
        body = u'<p>附件是你申请的资源原文，请查收!</p>'
    else:
        body = body
    from_email = settings.EMAIL_HOST_USER
    recipient_list = email_list

    s_email = EmailMessage(subject=subject, body=body, from_email=from_email, to=recipient_list)
    s_email.content_subtype = 'html'
    s_email.encoding = 'utf-8'
    if file_path:
        s_email.attach(filename=file_path.name, content=file_path.read(),
                       mimetype='application/octet-stream;charset=utf-8')
    # s_email.send()

    if s_email.send():
        return True
    else:
        return False


def send_code_email(email, sub_subject=None, message=None, code=None,key_head=EMAIL_TYPE_VALIDATE):
    '''
    生成激活码，发送账户激活邮件
    如果存在上一个激活码，那么重新发送，如果不存在，那么发送新激活邮件
    cache_key_validate是为了方便查找到上次的激活码
    TODO 应该限制单位时间内发送的邮件次数
    '''
    email = None if email == None else email.strip()
    cache_key = hashlib.md5(key_head + email).hexdigest()
    stored_value = cache.get(cache_key)
    if stored_value:
        if (timezone.now() - stored_value['send_time']).seconds < 60:
            return json_params_error(message='60秒内只能获取一次验证码', data={'email': u'60秒内只能获取一次验证码'})

    value = dict(code=code, send_time=timezone.now())
    cache.set(cache_key, value, 600)

    # 发送邮件到email邮箱
    subject = u'[医咖会]-' + sub_subject
    from_mail = settings.EMAIL_HOST_USER

    recipinet_list = [email]
    try:
        if mail.send_mail(subject, message, from_mail, recipinet_list):
            print('saved-key', cache_key, 'value=', value)
            return json_result(message='验证码邮件已发送成功')
        else:
            return json_result(message='验证码邮件已发送失败')
    except Exception:
        raise

