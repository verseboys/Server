#coding:utf-8

from django.shortcuts import render,redirect,reverse
from frontmodel import configs
from models.edc import *
from django.db.models import Count
from django.core.paginator import Paginator

from models.network import NetworkApplication

#项目列表
def studies(request):
    respBody = {
        'pages': 1,
        'current_page': 1,
        'page_count': 5,
    }
    studies = EdcStudy.objects.all().annotate(user_count=Count('edcstudyrole__user_id', distinct=True)).order_by('display_order')    
    respBody['edcStudies'] = studies

    return render(request, 'front_studies.html', context=respBody)


#项目详情
#包含详细信息 包含PI信息  包含专家委员会信息 包含 中心信息 包含研究者数量
def study(request,study_id=0):

    respBody = {}
    result=EdcStudy.objects.filter(study_id=study_id).annotate(role_count=Count('edcstudyrole__user_id', distinct=True),
                                                  site_count=Count('edcstudysite__site_id'))
    if (len(result)==1):
        respBody['study'] = result[0]
        with_site=EdcStudy.objects.annotate(site_count=Count('edcstudysite__site_id')).filter(study_id=study_id)
        if(len(with_site)==1):
            respBody['site_count']=with_site[0].site_count

    has_applied, member = _has_has_applied_and_member(request)
    respBody['has_applied'] = has_applied

    # EdcStudySite.objects.count
    return render(request, 'front_study.html', context=respBody)


def _has_has_applied_and_member(request):
    has_applied, member = NetworkApplication.has_has_applied_and_member(request)
    return has_applied, member
