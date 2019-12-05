# coding:utf-8

import json
import logging
import random

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from yizhu import settings

logger = logging.getLogger(__name__)
DRYRUN = getattr(settings, 'ALI_SMS_DRY_RUN', False)
# 以下为必须的配置字段，如果用户没有配置，这里会直接抛出 AttributeError，终止进程启动
ALI_SMS_ACCESS_KEY_ID = settings.ALI_SMS_ACCESS_KEY_ID
ALI_SMS_ACCESS_KEY_SECRET = settings.ALI_SMS_ACCESS_KEY_SECRET


def send_sms(mobile, signature_name, template_code, template_param):
    if DRYRUN:
        logging.info({'mobile': mobile, 'param': template_param})
        return True
    return _alisdk_send_sms(mobile,signature_name,template_code,template_param)

def _alisdk_send_sms(phone_numbers, signature_name, template_code, template_param):
    client = AcsClient(ALI_SMS_ACCESS_KEY_ID, ALI_SMS_ACCESS_KEY_SECRET, 'default')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('PhoneNumbers', phone_numbers)
    request.add_query_param('SignName', signature_name)
    request.add_query_param('TemplateCode', template_code)
    if not isinstance(template_param, str):
        template_param = json.dumps(template_param)
    request.add_query_param('TemplateParam', template_param)
    response = client.do_action_with_exception(request)

    return json.loads(response)


def send_verify_code(mobile):
    str = ''
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        str += ch
    # TODO 定义模板和签名名字
    # TODO 处理response
    send_sms(mobile, '医咖会', 'SMS_164800307', dict(code=str))
    return str
