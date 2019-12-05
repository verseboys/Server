#coding:utf-8
"""yizhu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import settings
import os
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'',include('api.front.urls')),
    url(r'^extends/',include('extends.urls')),
    url(r'^supervisor/',include('api.supervisor.urls')),
    url(r'^webapp_front/',include('api.webapp_front.urls')),
]

urlpatterns += static('/supervisor/', document_root=os.path.join(settings.BASE_DIR, 'supervisor'))
urlpatterns += static('/images/', document_root=os.path.join(settings.BASE_DIR, 'images'))
urlpatterns += static('/media/',document_root=os.path.join(settings.BASE_DIR,'media'))
# 映射周年庆典url
# print os.path.join(settings.BASE_DIR,'api/front/anniversary/dist/static/css/')
urlpatterns += static('/anniversary_static/img/',document_root=os.path.join(settings.BASE_DIR,'api/front/anniversary/dist/anniversary_static/img/'))
urlpatterns += static('/anniversary/',document_root=os.path.join(settings.BASE_DIR,'api/front/anniversary/dist/'))
urlpatterns += static('/anniversary_static/css/',document_root=os.path.join(settings.BASE_DIR,'api/front/anniversary/dist/anniversary_static/css/'))
urlpatterns += static('/anniversary_static/js/',document_root=os.path.join(settings.BASE_DIR,'api/front/anniversary/dist/anniversary_static/js/'))

# vue新后台 静态资源路径

urlpatterns += static('/new_manager_static/img/',document_root=os.path.join(settings.BASE_DIR,'supervisor/new_manager/dist/new_manager_static/img/'))
urlpatterns += static('/new_manager_static/css/',document_root=os.path.join(settings.BASE_DIR,'supervisor/new_manager/dist/new_manager_static/css/'))
urlpatterns += static('/new_manager_static/js/',document_root=os.path.join(settings.BASE_DIR,'supervisor/new_manager/dist/new_manager_static/js/'))
