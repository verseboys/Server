#coding:utf-8

from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render,redirect,reverse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponseRedirect
import json
from extends.buildjson import json_result
from frontmodel.decorators import login_required
from frontmodel import configs
from models.network import Network, NetworkApplication, NetworkMember, NetworkCourse, NetworkCourseVideo, NetworkCourseTrainLog,NetworkCourseTrainProgress, \
    NetworkNotice, NetworkNoticeAttachment, NetworkTag
from models.edc import EdcStudy
from network_forms import ApplicationForm, ApplicationMemberForm
from anniversary.models import userMedalModel,medalModel
from videomodel.models import VideoRelatedDataModel,VideoModel

from django.db.models import F
from api.common import service_ss
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.db.models import F
from django.db.models.aggregates import Count
'''
科研网络页面 /networks/1/

由于目前只有一个科研网络（慢阻肺专项），当访问 /networks/ 时，我们自动跳转到 /networks/1/。

科研网络页面有三个标签子页，分别为：
* “简介”标签页，展示科研网络简介（目前内容 hard code 在网页模板中）
* “科研项目”标签页，展示该科研网络关联的科研项目，对于每个科研项目，展示以下信息：
  * 项目名称、项目介绍
  * 跳转到科研项目详情页的链接
* “培训认证”标签页，根据当前登录用户的情况不同，分别展示：
  * 如果当前用户未加入该科研网络（不在任何一个申请表中，或者在申请表中但没有开户），则展示提示信息，提示用户申请加入或联系工作人员开通权限
  * 用户已加入该科研网络（在某个申请表中，并且已经开户），那么：
    * fundamental_course is None or !fundamental_course.published 如果没有基本课程或基本课程未发布，则展示提示信息：“培训视频预计于11月~12月上线，敬请期待！”
    * 如果基本课程已发布，则展示课程列表（含基本课程和后续课程）

科研网络页面上还有一个“申请加入”的按钮，其显示、跳转逻辑如下：
  * 如果当前登录用户已经提交了申请表，那么显示“已提交申请”
  * 如果当前登录用户没有提交过申请，那么点击后跳转到填写申请表单的页面
'''
@require_http_methods(['GET'])
def network(request, network_id):
    return _ok(message='已废弃')


def _has_has_applied_and_member(request):
    has_applied, member = NetworkApplication.has_has_applied_and_member(request)
    return has_applied, member


@require_http_methods(['GET'])
def page_home(request, network_id):
    try:
        network = Network.objects.get(id=network_id)
    except Network.DoesNotExist:
        return HttpResponseNotFound()
    notices = NetworkNotice.objects.filter(network=network, status=1)\
        .only('title', 'published_at', 'tags','top')\
        .order_by('-top','-published_at')[:3]

    # need_login 为True的情况：该notice为非公开权限，且用户未登录
    # has_permission 为True的情况：该notice为公开权限，或非公开权限且用户有权限查看
    # 前端判断need_login==True，直接访问详情页，由后端处理后续跳转逻辑；
    # 前端判断need_login==False，if has_permission==True，访问详情页，else 弹出无权限提示。
    if notices:
        for notice in notices:
            user = None
            if hasattr(request, 'front_user'):
                user = request.front_user
                notice.need_login = False
            else:
                notice.need_login = True
            notice.has_permission = _has_notice_permission(notice, network, user)
            if notice.has_permission and notice.need_login:
                notice.need_login = False

    has_applied, member = _has_has_applied_and_member(request)

    if member:
        context = dict(
            network=network,
            notices=notices,
            has_applied=has_applied
        )
        return render(request, 'network/index.html', context=context)

    context = dict(
        network=network,
        has_applied=has_applied
    )
    return render(request, 'network/home.html', context=context)


@require_http_methods(['GET'])
def page_studies(request, network_id):
    try:
        network = Network.objects.prefetch_related('studies', 'courses').get(id=network_id)
    except Network.DoesNotExist:
        return HttpResponseNotFound()

    has_applied, member = _has_has_applied_and_member(request)

    context = dict(
                network=network,
                studies=network.studies.all().order_by('display_order'),
                has_applied=has_applied,
                # 模板中可以判断 member 是否为空来判定当前用户是否有权限访问（是否已加入网络）
                member=member,
            )
    return render(request, 'network/studies.html', context=context)


@require_http_methods(['GET'])
def page_courses(request, network_id):
    try:
        network = Network.objects.prefetch_related('studies', 'courses').get(id=network_id)
    except Network.DoesNotExist:
        return HttpResponseNotFound()

    # “项目培训”下展示后台“序号”前两个课程的“课程名称”、“课程简介”和“课程图片”，按照课程的“序号”顺序排序展示
    courses = list(network.courses.filter(status='publish').order_by('order'))[:2]
    # NOTE 为了减少一次数据库请求，这里不使用 network.courses.filter(type=0)，而是在代码中筛选
    _fundamental_courses = [course for course in courses if course.type == 0]
    fundamental_course = _fundamental_courses[0] if _fundamental_courses else None
    # TODO “补充课程”的英文应该是什么？
    supplement_courses = [course for course in courses if course.type == 1]
    supplement_course = supplement_courses[-1] if supplement_courses else None

    has_applied, member = _has_has_applied_and_member(request)

    context = dict(
        network=network,
        has_applied=has_applied,
        # 模板中可以判断 member 是否为空来判定当前用户是否有权限访问（是否已加入网络）
        member=member,
        fundamental_course=fundamental_course,
        supplement_course=supplement_course,
        courses=courses,
    )
    return render(request, 'network/courses.html', context=context)


@require_http_methods(['GET'])
def page_notices(request, network_id):
    try:
        network = Network.objects.prefetch_related('studies', 'courses').get(id=network_id)
        tag_id = request.GET.get('tag_id')
        if tag_id:
            notices = NetworkTag.objects.get(id=tag_id).notices.prefetch_related('tags').filter(status=1).order_by(
                '-top', '-published_at')
        else:
            notices = NetworkNotice.objects.filter(network=network, status=1).only('title', 'published_at', 'tags',
                                                                                   'top').order_by('-top',
                                                                                                   '-published_at')
    except Network.DoesNotExist:
        return HttpResponseNotFound()
    tags = NetworkTag.objects.all().only('id', 'name')
    # todo 待优化
    # need_login 为True的情况：该notice为非公开权限，且用户未登录
    # has_permission 为True的情况：该notice为公开权限，或非公开权限且用户有权限查看
    # 前端判断need_login==True，直接访问详情页，由后端处理后续跳转逻辑；
    # 前端判断need_login==False，if has_permission==True，访问详情页，else 弹出无权限提示。
    if notices:
        for notice in notices:
            user = None
            if hasattr(request, 'front_user'):
                user = request.front_user
                notice.need_login = False
            else:
                notice.need_login = True
            notice.has_permission = _has_notice_permission(notice, network, user)
            if notice.has_permission and notice.need_login:
                notice.need_login = False

    has_applied, member = _has_has_applied_and_member(request)

    context = dict(
        network=network,
        has_applied=has_applied,
        # 模板中可以判断 member 是否为空来判定当前用户是否有权限访问（是否已加入网络）
        member=member,
        notices=notices,
        tags=tags,
    )
    return render(request, 'network/notices.html', context=context)


@require_http_methods(['GET'])
def page_about(request, network_id):
    try:
        network = Network.objects.prefetch_related('studies', 'courses').get(id=network_id)
    except Network.DoesNotExist:
        return HttpResponseNotFound()

    has_applied, member = _has_has_applied_and_member(request)

    context = dict(
        network=network,
        has_applied=has_applied,
        # 模板中可以判断 member 是否为空来判定当前用户是否有权限访问（是否已加入网络）
        member=member,
    )
    return render(request, 'network/about.html', context=context)


"""
科研网络申请表页面 /networks/1/apply/

该 view 函数既用于渲染网页，也用于 API 请求，具体如下：
 * GET ->
   * 若用户未提交过申请，渲染申请表页面
   * 若用户已提交过申请，渲染申请表预览页面
   * 若用户已提交过申请，且 querystring 中有 edit=1，则渲染申请表编辑页面
 * POST -> 提交申请表单（API请求，只能用 ajax 请求，不会渲染网页）
"""
@require_http_methods(['GET', 'POST'])
@login_required
def apply(request, network_id):
    if request.method == 'POST':
        return apply_submit(request, network_id)

    try:
        network = Network.objects.prefetch_related('studies').get(id=network_id)
    except Network.DoesNotExist:
        # TODO implement and use a global 404 page
        return HttpResponseNotFound()

    applications = list(request.front_user.network_applications.all())
    if len(applications) == 0:
        application = None
    elif len(applications) == 1:
        application = applications[0]
    else:
        # TODO 处理一个用户有多个申请的情况
        pass

    form = application.to_form_dict() if application else {
            'edc_study_ids': [],
            'site': '',
            'status': 0,
            'address': '',
            'leader': None,
            'researchers': [],
            'datamanager': None,
            }
    studies = [study.to_dict() for study in network.studies.all()]

    has_applied = True if application else False

    context = dict(
            network = network,
            studies = studies,
            studies_json = json.dumps(studies, ensure_ascii=False),
            form = form,
            form_json = json.dumps(form, ensure_ascii=False),
            has_applied = has_applied,
            )
    if not has_applied:
        # 渲染申请表单
        return render(request, 'network/apply.html', context=context)
    else:
        if request.GET.get('edit', '').lower() in ('t', 'true', 'y', 'yes', '1'):
            # 渲染编辑表单页
            return render(request, 'network/apply_edit.html', context=context)
        else:
            # 渲染预览页
            return render(request, 'network/apply_preview.html', context=context)

@require_http_methods(['GET', 'POST'])
@login_required
def apply_success(request, network_id):
    return render(request, 'network/apply_success.html', context={})

"""
提交/修改申请表单
请求 body 数据结构:
    {
       "edc_study_ids": [1, 2, 3],
       "site": "工作单位",
       "address": "工作地址",
       "leader": {
          "name": "张三",
          "email": "zhangsan@126.com",
          "phone": "13312345678",
          "department": "科室",
          "title": "职称",
       },
       "researchers": [
         {
            "name": "李四",
            "email": "lisi@126.com",
            "phone": "13312345678",
            "department": "科室",
            "title": "职称",
         },
         {
         ...
         },
         ...
       ],
       "datamanager": {
          "name": "王五",
          "email": "wangwu@126.com",
          "phone": "13312345678",
          "department": "科室",
          "title": "职称",
       }
    }

返回代码：200, 400, 404
* 如果请求正确，并被服务器正确处理，那么会返回200。response body可以被忽略，前端直接显示申请已提交的页面即可。
* 如果指定的 network 不存在，返回 404（考虑到这属于出bug的情况，暂时不返回json，直接返回django默认的404）
* 如果请求的 body 不是合法的 json，会返回 400
* 如果数据有不正确的情况，会返回400，并在response body里面说明错误出错的信息，格式如下：

    {
      "code": 400,
      "message": "必须提供负责人的手机号", // 后端会返回校验时碰到的第一个错误的描述，前端可以直接展示该信息
      // 提供结构化的错误信息，以便前端可以直接将指定的输入框标红，提示用户哪里除了问题。
      // XXX 请前端同学决定是否需要后端返回该信息
      "form_errors": {},
    }
"""
def apply_submit(request, network_id):
    try:
        network = Network.objects.get(id=network_id)
    except Network.DoesNotExist:
        return HttpResponseNotFound()

    try:
        application = NetworkApplication.objects.get(user=request.front_user)
        # 申请已存在，那么就更新申请
    except NetworkApplication.DoesNotExist:
        # 申请不存在，那么创建新的申请
        application = None

    # -------- 8< --------
    # 处理请求的 body，对数据进行校验

    try:
        data = json.loads(request.body)
    except:
        return _bad_request(message='请求 body 不是合法的 json')

    form = ApplicationForm(data)
    if not form.is_valid():
        return _bad_request(form=form)

    members = []

    if 'leader' not in data:
        return _bad_request(message='请填写项目负责人信息')
    leader = ApplicationMemberForm(data['leader'])
    if not leader.is_valid():
        return _bad_request(message='项目负责人信息有误', form=leader)
    member = leader.cleaned_data
    member['duty'] = '项目负责人'
    members.append(member)

    if 'researchers' not in data:
        return _bad_request(message='请填写研究者信息')
    if len(data['researchers']) == 0:
        return _bad_request(message='请至少填写一个研究者')
    for researcher in [ApplicationMemberForm(item) for item in data['researchers']]:
        if not researcher.is_valid():
            return _bad_request(message='研究者信息有误', form=researcher)
        member = researcher.cleaned_data
        member['duty'] = '研究者'
        members.append(member)

    if 'datamanager' not in data:
        # TODO 我们目前暂时不要求数据管理员
        datamanager = None
    else:
        datamanager = ApplicationMemberForm(data['datamanager'])
        if not datamanager.is_valid():
            return _bad_request(message='数据管理员信息有误', form=researcher)
        member = datamanager.cleaned_data
        member['duty'] = '数据管理员'
        members.append(member)

    phone_email_hash_name = {}
    for member in members:
        if member['phone'] not in phone_email_hash_name:
            phone_email_hash_name[member['phone']] = member['name']
        else:
            if phone_email_hash_name[member['phone']] != member['name']:
                return _bad_request(message='禁止多人填写同一个手机号。',form_errors={ 'phone':member['phone'] })
        if member['email'] not in phone_email_hash_name:
            phone_email_hash_name[member['email']] = member['name']
        else:
            if phone_email_hash_name[member['email']] != member['name']:
                return _bad_request(message='禁止多人填写同一个邮箱。',form_errors={ 'email':member['email'] })

    # -------- 8< --------
    kwargs = form.cleaned_data
    studies = kwargs.pop('edc_study_ids')
    kwargs['network'] = network
    kwargs['user'] = request.front_user

    with transaction.atomic():
        if not application:
            application = NetworkApplication.objects.create(**kwargs)
        else:
            # 申请已经存在，则表示用户需要更新申请
            # 更新申请时，network、user 字段不能修改，只能修改site、address、studies字段
            application.address = kwargs['address']
            application.site = kwargs['site']
            application.save(update_fields=['address', 'site', 'updated_at'])
            # 清空所有关联的 study，后面再重新添加
            application.studies.clear()
            # 先删除原有的所有 member，后面再重新添加 member，避免出现孤儿 member，也免去检查重复，
            # 例如之前有一个研究员姓名为张三，此次将姓名修改为张四，后端层面无法判断是哪一个 member 被修改了
            NetworkMember.objects.filter(network=network, application=application).delete()

        application.studies.add(*studies)
        for kwargs in members:
            kwargs['network'] = network
            kwargs['application'] = application
            member = NetworkMember.objects.create(**kwargs)

    response_data = {'message': '申请已提交成功'}
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), status=200, content_type='application/json')

def _bad_request(message=None, form=None, form_errors=None):
    if not form_errors:
        form_errors = form.errors if form else None
    if not message and form_errors:
        # TODO extract message from form error
        message = form_errors.values()[0][0]
    code = 400

    data = dict(message=message, code=code, form_errors=form_errors)
    return HttpResponse(
            json.dumps(data, ensure_ascii=False),
            status = 400,
            content_type = 'application/json',
            )

def _ok(message=None, data=None):
    data = dict(code=200, data=data, message=message)
    return HttpResponse(
            json.dumps(data, ensure_ascii=False),
            status = 200,
            content_type = 'application/json',
            )

def _permission_denied(message='无权访问'):
    data = dict(code=403, data=None, message=message)
    return HttpResponse(
            json.dumps(data, ensure_ascii=False),
            status = 403,
            content_type = 'application/json',
            )

# -------- 8< --------
# 科研培训相关页面
# 原型图：https://us60g5.axshare.com/#g=1&p=%E5%9F%B9%E8%AE%AD%E8%AF%BE%E7%A8%8B
# 文档：https://confluence.natureself.site/pages/viewpage.action?pageId=26772099
# -------- 8< --------

'''
科研网络培训课程详情页：/networks/1/courses/<id>/

需要展示的内容：
* 培训课程的基本信息，  NetworkCourse.name（名称)  description(简介）
* 课程视频列表  video for videos   title(名称) video_time(视频时长)  watched(是否看过） len(videos) 视频总课数量


 member为空需要渲染错误信息 参见network部分
'''
@require_http_methods(['GET'])
@login_required
def course(request, network_id, course_id):
    try:
        network = Network.objects.get(id=network_id)
        course = NetworkCourse.objects.get(network=network, id=course_id)
    except Network.DoesNotExist:
        return HttpResponseNotFound()
    except NetworkCourse.DoesNotExist:
        return HttpResponseNotFound()

    network_course_videos = NetworkCourseVideo.objects.select_related('video').filter(course=course).order_by('order')

    has_applied, member = _has_has_applied_and_member(request)
    # 获取当前用户已经学习过的视频列表，并存在一个集合中
    train_logs = NetworkCourseTrainLog.objects.filter(participant=request.front_user, video__course=course)
    watched_videos = {log.video.id for log in train_logs}
    train_progress = NetworkCourseTrainProgress.objects.filter(participant=request.front_user, course=course).first()

    learned_all=False
    if train_progress is not None and train_progress.end_at is not None:
        learned_all=True
    # videos 给前端用于渲染，这里的 video 是一个 Video 对象，同时
    # * 注入了 'order' 属性，表示其排序顺序
    # * 注入了 'watched' 属性，表示用户是否学习过该视频
    videos = []
    for network_course_video in network_course_videos:
        video = network_course_video
        video.order = network_course_video.order
        video.watched = video.id in watched_videos
        videos.append(video)

    context = dict(
            network = network,
            has_applied=has_applied,
            member = member,
            course = course,
            videos = videos,
            watched_count = len(watched_videos),
            video_count = len(videos),
            learned_all = learned_all,
            )
    return render(request, 'network/course.html', context=context)

'''
科研网络培训课程视频页：/networks/1/courses/<id>/videos/<id>/

需要展示的内容：
    视频title 本期要点 讲者介绍 视频展示窗口
member为空需要渲染错误信息 参见network部分
注意：此video_id 实际是 course_video_id
'''
@require_http_methods(['GET'])
@login_required
def course_video(request, network_id, course_id, video_id):
    try:
        network = Network.objects.get(id=network_id)
        course = NetworkCourse.objects.get(network=network, id=course_id)
        video = NetworkCourseVideo.objects.select_related('video').get(course=course, id=video_id)
    except Network.DoesNotExist:
        return HttpResponseNotFound()
    except NetworkCourse.DoesNotExist:
        return HttpResponseNotFound()
    except NetworkCourseVideo.DoesNotExist:
        return HttpResponseNotFound()

    network_course_videos = NetworkCourseVideo.objects.select_related('video').filter(course=course).order_by('order')

    # TODO 需要校验用户是否有权限访问
    has_applied, member = _has_has_applied_and_member(request)

    train_log = NetworkCourseTrainLog.objects.filter(video=video, participant=request.front_user).first()
    # 注入 'watched' 属性，表示用户是否已经学习过该视频
    video.watched = (train_log != None)

    # 关联的附件 这段代码参考了views.py
    videoModel = VideoModel.objects.get(id=video.video.id)
    video_data_list = VideoRelatedDataModel.objects.filter(video=videoModel).all().values('id','file_name')\
        .annotate(file_id=F('id'))

    context = dict(
            network = network,
            course = course,
            has_applied=has_applied,
            member = member,
            videos = network_course_videos,
            video = video,
            user = request.front_user,
            video_related_data = video_data_list,
            )
    return render(request, 'network/course_video.html', context=context)

'''
科研网络培训课程视频播放完后的回调：POST /networks/1/courses/<id>/videos/<id>/watch

在数据库中插入用户的观看记录（即插入一条 NetworkCourseTrainLog）

这是一个纯 API 接口，不会返回网页。

如果成功，返回 200
如果失败，返回 404 或 403，具体如下：
* URL 中的 network id 无效，返回 404
* URL 中的 course id 无效，返回 404
* URL 中的 video id 无效，返回 404
* 当前登录用户无权限，返回 403

注意1：本请求涉及多次数据库写操作，需要用事务保护
注意2: 本API可能会被重复调用（例如用户多次观看同一个视频），所以所有数据库的写操作都要考虑重复的问题
'''
@require_http_methods(['POST'])
@login_required
@transaction.atomic
def watch_video(request, network_id, course_id, video_id):
    try:
        network = Network.objects.get(id=network_id)
        course = NetworkCourse.objects.select_related('medal').get(network=network, id=course_id)
        video = NetworkCourseVideo.objects.select_related('video').get(course=course, id=video_id)
    except Network.DoesNotExist:
        return HttpResponseNotFound()
    except NetworkCourse.DoesNotExist:
        return HttpResponseNotFound()
    except NetworkCourseVideo.DoesNotExist:
        return HttpResponseNotFound()

    member = NetworkMember.objects.filter(email=request.front_user.email, status=2).first()
    if course.public_scope == 1:
        if not member:
            return _permission_denied(message='当前登录账号未加入科研网络')

    log, _ = NetworkCourseTrainLog.objects.get_or_create(participant=request.front_user, video=video)

    # 如果用户第一次观看该课程的视频，则增加 NetworkCourseTrainProgress 记录，设置 begin_at 字段
    # 如果用户已经观看完该课程的所有视频，则标记 TrainProgress 中的 end_at 字段
    course_videos = NetworkCourseVideo.objects.filter(course=course)
    course_video_ids = set([v.id for v in course_videos])
    watched_videos = NetworkCourseTrainLog.objects.filter(video__course=course, participant=request.front_user)
    watched_video_ids = set([v.video_id for v in watched_videos])

    if len(watched_video_ids) == 1:
        # 用户第一次观看该课程的视频
        # NOTE 这里使用 get_or_create 而不是 create，因为用户可能会重复看第一个视频
        progress, _ = NetworkCourseTrainProgress.objects.get_or_create(
                participant=request.front_user, course=course,
                defaults={'begin_at': timezone.now(), 'end_at': None},
                )
    # NOTE 这里不应该用 elif，而必须使用 if。如果某个课程只有一个视频，上下这两段逻辑必须都跑一遍，否则 begin_at 没有值
    if course_video_ids == watched_video_ids:
        # 用户已经观看完该课程的所有视频
        # NOTE 这里使用 update_or_create 而不是 update，因为用户可能会重复看最后一个视频
        progress, _ = NetworkCourseTrainProgress.objects.update_or_create(
                participant=request.front_user, course=course,
                defaults={'end_at': timezone.now()},
                )

        # 如果课程有关联的勋章，还需要给用户添加获得勋章的记录
        # NOTE 这里用 get_or_create 而不是 create，因为用户可能会重复看最后一个视频
        if course.medal is not None:
            medal_count = 0
            front_user_avatar = request.front_user.avatar
            if course.serial_state == "finished":
                medal_count = course.medal.usermedalmodel_set.count()
                userMedalModel.objects.get_or_create(
                    medal=course.medal, user=request.front_user
                    )
            return  _ok("",{
                'earnedMedal':True,
                'dataCollection':course.data_collection,
                "serialState": course.serial_state,
                'medalCount':medal_count,
                "avatar":front_user_avatar
                })
    return _ok("",{'earnedMedal':False})


def _has_notice_permission(notice, network, user):
    # 公开
    if notice.scope == 0:
        return True
    # 需要科研网络权限
    if notice.scope == 1 and user and NetworkMember.objects.filter(medieco_user_id=user.id, status=2, network=network).exists():
        return True
    return False


'''
科研网络通知公告详情页：/networks/1/notices/<notice_id>

需要展示的内容：notice 基础信息 和附件信息
'''
# todo 待优化
@require_http_methods(['GET'])
def notice(request, network_id, notice_id):
    try:
        network = Network.objects.get(id=network_id)
        notice = NetworkNotice.objects.get(network=network, id=notice_id, status=1)
    except Network.DoesNotExist:
        return HttpResponseNotFound()
    except NetworkNotice.DoesNotExist:
        return HttpResponseNotFound()
    user = None
    if hasattr(request, 'front_user'):
        user = request.front_user
    has_permission = _has_notice_permission(notice, network, user)
    # 没有权限分为登录和未登录两种情况
    if not has_permission:
        if user:
            # messages 是 Django 的一种机制，因为 redirect 不便于传递消息，故利用 messages 给网页传递消息
            # 前端根据此来判断是否展示相关提示消息
            messages.warning(request, '抱歉，此通知公告只有科研网络成员有权阅读！')
            return redirect(reverse('network', kwargs={'network_id': 1}) + '#notice')
        login_url = reverse('front_login') + '?next=' + request.path + '#1'
        return redirect(login_url)
    # 有权限，render 详情页

    # 统计该通知公告详情页被访问的次数
    notice.read_count = F('read_count') + 1
    notice.save()

    notice_attachments = NetworkNoticeAttachment.objects.filter(notice=notice)
    attachments = []
    if notice_attachments:
        keys = [o.file_key for o in notice_attachments]
        attachments = service_ss.get_many_files_info(keys)

    has_applied, member = _has_has_applied_and_member(request)

    context = dict(
        network=network,
        notice=notice,
        attachments=attachments,
        has_applied=has_applied,
    )
    return render(request, 'network/notice.html', context=context)



