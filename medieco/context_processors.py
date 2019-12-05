# coding: utf-8

def front_user(request):
    """
    说明：在 Django 模板中，默认是可以访问 request 这个 context 变量的（Django 默认的
    django.template.context_processors.request 中加入了这个变量），因此我们可以直接使用
    request.user 或 request.front_user。但是之前写的所有的模板文件中都直接使用 front_user，
    因此我们需要这个变量。
    """
    return {
            'front_user': getattr(request, 'front_user', None),
        }
