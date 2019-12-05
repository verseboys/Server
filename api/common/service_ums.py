#coding:utf-8
import urllib2
import json
import requests
from api.common.medieco_user import MediecoUser
from django.conf import settings

'''
This file is deprecated.will be removed from project.
'''
# @deprecated
def email_check(email):
    req_body={
        "email":email
    }
    response=_ums_upgrade(json.dumps(req_body))
    content = json.loads(response.content)
    if response.status_code == 200:
        user = content['data']['medieco_user']
        user_wapper=MediecoUser(user)
        user_wapper.upgrade_mode=content['data']['upgrade_mode']
        return user_wapper
    elif response.status_code == 400:
        print content
        return None
    else:
        return None

#通过uid检查用户账号是否存在，还有用户是否锁定状态
def is_user_login():
    pass

def login(username_or_email,password):
    req_body = {
        "app":"medieco",
        "type":"password",
        "identity":username_or_email,
        "password":password,
    }
    response = _ums_authenticate(json.dumps(req_body))
    content = json.loads(response.content)
    if response.status_code == 200:
        user = content['data']['medieco_user']
        return MediecoUser(user)
    elif response.status_code == 400:
        return None
    else:
        return None

def change_password(email,password):
    response = _ums_upgrade(json.dumps({'email':email}))
    content = json.loads(response.content)
    if response.status_code <> 200:
        return None
    req_body = {
        'password':password,
    }
    response = _ums_patch_account(content['data']['id'],json.dumps(req_body))
    content = json.loads(response.content)
    if response.status_code <> 200:
        return None
    return content

def change_account(email,req_body):
    response = _ums_upgrade(json.dumps({'email': email}))
    content = json.loads(response.content)
    if response.status_code != 200:
        return None
    response = _ums_patch_account(content['data']['id'], json.dumps(req_body))
    content = json.loads(response.content)
    if response.status_code != 200:
        return None
    return content

def _ums_upgrade(req_body):
    url = settings.SERVICE_UMS + "/v1/upgrade"
    headers = {'content-type':'application/json'}
    response = requests.post(url,data=req_body,headers=headers)
    return response

def _ums_authenticate(req_body):
    url = settings.SERVICE_UMS + "/v1/authenticate"
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=req_body, headers=headers)
    return response

def _ums_patch_account(account_id,req_body):
    url = settings.SERVICE_UMS + "/v1/accounts/"+str(account_id)
    headers = {'content-type': 'application/json'}
    response = requests.patch(url, data=req_body, headers=headers)
    return response
