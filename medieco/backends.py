# coding:utf-8

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from frontmodel.models import FrontUserModel

"""
Django 身份验证后端。

背景说明：

在医咖会项目中，有两个用户表，分别是 FrontUserModel 和 Django 自带的 User，
其中 FrontUserModel 为网站用户，Django User 为管理后台用户。在 session 登录
方面，Django User 直接使用了 Django 默认的 ModelBackend 以及相关的 session 机制，
而 FrontUserModel 的登录全套流程（密码哈希、密码校验、session等）全都是自己
造的轮子，实现质量很差。

我们现在在新项目中重构医咖会，这个新项目中会规范化 FrontUserModel 的全套流程。
为了方便，我们将两套用户系统使用统一的 Authentication Backend 机制以及统一的
session 机制。
"""

class SupervisorUserAuthenticationBackend(ModelBackend):
    """
    管理后台用户登录，直接继承 ModelBackend，不做修改。在配置文件中不直接使用
    ModelBackend，而是使用 SupervisorUserAuthenticationBackend，主要是为了让
    代码意义更加明确。
    """
    pass

class _FrontUserAuthenticationBackendBase(object):
    def get_user(self, user_id):
        try:
            user = FrontUserModel.objects.get(pk=user_id)
        except FrontUserModel.DoesNotExist:
            return None

        return user

class FrontUserPasswordAuthenticationBackend(_FrontUserAuthenticationBackendBase):
    """
    前端用户使用 username/email + password 登录
    """
    def authenticate(self, identity=None, password=None, **kwargs):
        if not identity or not password:
            return None

        try:
            user = FrontUserModel.objects.get(
                    Q(username=identity) | \
                    Q(email__iexact=identity) | \
                    Q(phone=identity)
                    )
        except FrontUserModel.DoesNotExist:
            return None
        except FrontUserModel.MultipleObjectsReturned:
            # 有多个账号匹配到该请求，这应该算是 BUG，我们暂时不做处理
            # TODO
            return None

        if user.check_password(password):
            return user

        return None

class FrontUserCodeAuthenticationBackend(_FrontUserAuthenticationBackendBase):
    """
    前端用户使用 phone + code 登录
    """
    def authenticate(self, phone=None, **kwargs):
        if not phone:
            return None

        try:
            user = FrontUserModel.objects.get(Q(phone=phone))
        except FrontUserModel.DoesNotExist:
            return None

        return user