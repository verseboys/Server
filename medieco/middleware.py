# coding: utf-8

from django.utils.deprecation import MiddlewareMixin
from frontmodel.models import FrontUserModel

class FrontUserAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        2019.06.11 更新说明

        我们将用户登录整套流程改为 Django 默认的，因此 Django 的 AuthenticationMiddleware
        会自动注入 request.user，为了代码层面的兼容，我们仍然设置一下 front_user。

        在 settings.py 中，我们需要确认将 AuthenticationMiddleware 放在这个 Middleware 前面。

        注意，request.user 可能是 Django 自带的 user，也可能是 FrontUserModel，我们仅在其为
        FrontUserModel 时设置 request.front_user。

        另一个讨厌的地方，在 Django 中，实际上创建了一个特殊的用户，AnonymouseUser，所有的
        请求都有 request.user 属性，可以通过 request.user.is_authenticated 来判断用户是否登录。
        然而在医咖会原来的代码中，却通过 hasattr(request, 'front_user') 来判断，因此，
        front_user 不能为 None（只要设置了，就一定得是一个 FrontUserModel 实例。
        """
        user = getattr(request, 'user', None)
        if user and isinstance(user, FrontUserModel):
            request.front_user = user
