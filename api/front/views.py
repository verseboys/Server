# coding:utf-8

import datetime
import json
import logging
import os
import random
import re
import time

from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage, InvalidPage
from django.db.models import Q, Count, Prefetch, Case, When
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.http import require_http_methods
from django.db.models.functions import Greatest, Coalesce

from anniversary.decorators import anniversary_data
from anniversary.models import medalModel, userMedalModel, anniversaryModel, specialTopicCommentModel, \
    specialTopicCommentLikeModel
from api.common.views import comment_time_period, add_answer, question_detail, favorites, user_praise
from api.front.user_views import login_by_specific_backend
from api.webapp_front.views import professional_sections, job_title
from extends import send_email
from extends.alipay.y_alipay import y_alipay, y_alipay_return_url
from extends.buildjson import json_result, json_params_error, json_method_error
from extends.tasks import update_order_status
from extends.views import send_captcha_email
from frontmodel import configs
from frontmodel.decorators import front_login_required, front_user_infomation_is_full, \
    front_user_infomation_is_full_soft
from frontmodel.models import FrontUserModel, ProfessionalSectionsModel, JobTitleModel, UserFavoritesModel, \
    UserPraiseModel, UserBuyOrderModel
from methodmodel.models import MethodArticleInfoModel, MethodArticleContentModel, MethodCategoryModel, BannerModel, \
    MethodArticleRelatedReadingModel, MethodArticleTopicModel, TopicRelatedMethodArticleModel, KeyWordModel, \
    KeyWordRelevanceArticleModel
from models.network import NetworkMemberB4Account
from newsmodel.models import NewsCategoryModel, NewsModel, NewsCommentModel, HoldNewsModel, NewsRelatedReadingModel
from questionsandanswersmodel.models import QuestionsModel, AnswersModel, QuestionCategoryModel, CollectAnswerModel, \
    PraiseAnswerModel, UserCollectCategoryModel, AttentionQuestionModel, MyMessagesModel
from supervisormodel.models import UserFeedBack
from videomodel.models import VideoModel, CourseModel, VideoCommentModel, VideoRelatedDataModel
from videomodel.polyv_validate import polyv_validate
from yizhu import settings

logger = logging.getLogger(__name__)


# 登录页面渲染
def f_login(request):
    return render(request, 'front_login.html')


# 注册页面渲染
def f_register(request):
    return render(request, 'front_register.html')


# 找回密码渲染
@require_http_methods(['GET','POST'])
def recover_password(request, code=None):
    if request.method == 'GET':
        if not cache.get(code):
            context = dict(message='链接已失效')
            return render(request, 'recover_password.html',context=context)
        return render(request, 'recover_password.html')
        # 验证邮箱的url
    password = request.POST.get('password', None)
    repeat_password = request.POST.get('repeat_password', None)

    if code:
        # 根据code 从缓存中读取对应的邮箱
        email = cache.get(code)
        logger.info({'缓存中的邮箱:': email, })
        if email:
            if password:
                if password == repeat_password:
                    if len(password) < 4 or len(password) > 16:
                        return json_params_error(message=u'请输入4-16位长度的密码!')
                    # 查询出这个邮箱对应的用户信息
                    try:
                        user = FrontUserModel.objects.get(email=email)
                    except FrontUserModel.DoesNotExist:
                        return json_params_error(message=u'该邮箱未注册!')
                    user.update_password(password)
                    cache.delete(code)
                    login_by_specific_backend(request,user)
                    return json_result(message=u'密码已经重置!')

                else:
                    return json_params_error(message=u'两次密码不一致!')
            else:
                return json_params_error(message=u'密码不能为空!')
        else:
            return json_params_error(message=u'链接已失效!')
    else:
        return json_params_error(message=u'你尝试访问一个不存在的地址!')


@require_http_methods(['POST'])
def check_captcha(request):
    # 验证码验证：
    captcha = request.POST.get('captcha')
    if captcha:
        cache_captcha = cache.get(request.session.session_key)

        if not cache_captcha:
            return json_params_error(message='验证码获取失败')
        captcha = str(captcha).lower()
        cache_captcha = str(cache_captcha).lower()
        if captcha != cache_captcha:
            return json_params_error(message='注册失败')
    else:
        return json_params_error(message='验证码不能为空')
    return json_result(message=u'注册成功!')


# 注册
@require_http_methods(['GET', 'POST'])
def register(request):
    # TODO 和用户相关的应该要迁移到user_views里面去
    if request.method == 'GET':
        return json_result(message=u'这是注册页面get请求!')
    else:
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repeat_password = request.POST.get('repeat_password', None)
        captcha = request.POST.get('captcha', None)

        logger.info({'email': email, 'password': password, 'repeat_password': repeat_password,
                     'captcha': captcha})

        # 将错误提示汇总一起返回
        tmp_message = {}

        # 邮箱、密码和验证码验证部分
        # TODO 校驗部分需要放入在Form裏面完成
        if email is None:
            return json_params_error(data={'email': u'请输入邮箱'})
        if not re.match(configs.EMAIL_REGX, email):
            return json_params_error(data={'email': u'邮箱格式错误'})
        if not password:
            return json_params_error(data={'password': u'密码不能为空!'})
        if len(password) < 4 or len(password) > 16:
            return json_params_error(data={'password': u'请输入4-16位长度的密码'})
        if not captcha:
            return json_params_error(data={'captcha': u'验证码不能为空'})
        # 验证码验证部分
        cache_captcha = cache.get(request.session.session_key)
        if not cache_captcha:
            return json_params_error(data={'captcha':u'验证码错误'})
        try:
            captcha = str(captcha).lower()
            cache_captcha = str(cache_captcha).lower()
        except:
            pass
        if captcha != cache_captcha:
            return json_params_error(data={'captcha':u'验证码错误'})
        cache.delete(request.session.session_key)
        try:
            user_findby_email = FrontUserModel.objects.get(email=email)
            return json_params_error(data={'email': u'该邮箱已被注册,请返回登录'})
        except FrontUserModel.DoesNotExist:
            pass

        # 用户名现在不由用户注册时输入，默认生成一个。
        user = FrontUserModel(email=email, password=password)
        user.create_user_by_email()
    try:
        if send_email.send_email_active_mail(request, email):
            return json_result(message=u'激活邮件已发送')
        else:
            return json_params_error(data={'email': u'激活邮件发送失败'})
    except Exception:
        return json_params_error(data={'email': u'邮件发送失败，请检查邮箱地址'})


# 给邮箱发送验证码
@require_http_methods(['GET', 'POST'])
def register_send_email(request):
    email = request.POST.get('email', None)

    result = send_captcha_email(request, email)
    if result:
        logger.info({'email': email, 'cache_captcha': cache.get(request.session.session_key), })
        return json_result(message=u'验证码已发送到你的邮箱!')
    else:
        return json_params_error(message=u'邮件发送失败!邮箱不存在!')


# 忘记密码
@require_http_methods(['GET','POST'])
def forget_password(request):
    if request.method == 'GET':
        return render(request, 'forget_password.html')

    email = request.POST.get('email', None)
    captcha = request.POST.get('captcha', None)
    if not email:
        return json_params_error(message=u'邮箱不能为空!')
    if not re.match(configs.EMAIL_REGX, email):
        return json_params_error(message=u'邮箱格式错误')
    if not captcha:
        return json_params_error(message=u'验证码不能为空')
        # 验证码验证部分
    cache_captcha = cache.get(request.session.session_key)
    if not cache_captcha:
        return json_params_error(message= u'验证码错误')
    try:
        captcha = str(captcha).lower()
        cache_captcha = str(cache_captcha).lower()
    except:
        pass
    if captcha != cache_captcha:
        return json_params_error(message=u'验证码错误')
    cache.delete(request.session.session_key)
        # 查询出这个邮箱对应的用户信息
    try:
        userModel = FrontUserModel.objects.get(email=email)
    except FrontUserModel.DoesNotExist:
        # TODO 这里会暴露邮箱是否在医咖会注册，需要从业务上补充。
        return json_params_error(message=u'该邮箱未注册!')

    subject = u'[医咖会]-找回密码'
    time_formated = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime())
    message = {
        'first_content': u'你好!\n你在' + time_formated + '提交了邮箱找回密码请求\n请在30分钟内点击下面的链接找回密码：'
    }
    try:
        result = send_email.send_forget_password_email(request, email=email, check_url='recover_password', subject=subject,
                                               message=message, expire_second=1800)
    except Exception:
        return json_method_error(message= u'邮件发送失败，请检查邮箱地址')

    if result:
        return json_result(message=u'邮件发送成功!')
    else:
        return json_params_error(message=u'邮件发送失败!')


# 忘记密码时检查邮箱 deprecated by recover_password
def check_email(request, code=None):
    pass


# 登录
@require_http_methods(['GET', 'POST'])
def front_login(request):
    if request.method == 'GET':
        return json_result(message=u'这是登录页面!')
    else:
        identity = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(identity=identity, password=password)
        if not user:
            return json_params_error(data=dict(message=u'账号或密码错误'))

        # TODO 检查账号是否是用邮箱注册、且没有点击验证链接，这种情况下，
        #      跳转到页面提示用户完成激活
        # if not user.activated:
        #    return redirect(...)

        if not user.is_active:
            return json_params_error(data=dict(message=u'此用户已被锁定,请联系管理员!'))

        # TODO 以下代码为原来的代码，需要添加逻辑说明
        b4account = NetworkMemberB4Account.objects.filter(member__email=user.email).first()
        if b4account and b4account.password_raw:
            user.set_email_validated()

        login(request, user)
        # 如果邮箱没有验证，那么跳转到邮箱验证页，考虑增加额外需要验证的字段，已有的邮箱先都标记为无需验证，
        # 新注册的邮箱标记为需要验证。
        if user.email_need_validate:
            return json_result(message=u'登陆成功',data=dict(redirect='/email_checking'))

        # 如果有 next，则跳转到 next 页面，否则返回 json 信息
        nexturl = request.GET.get('next')
        if nexturl:
            return redirect(nexturl)
        else:
            context = dict(id=user.id, username=user.username, avatar=user.avatar)
            return json_result(message=u'登录成功!', data=context)

# 修改密码
@require_http_methods(['GET', 'POST'])
@front_login_required
def reset_password(request):
    if request.method == 'GET':
        return json_result(message=u'修改密码页面')
    else:
        old_password = request.POST.get('old_password', None)
        new_password = request.POST.get('new_password', None)
        repeat_password = request.POST.get('repeat_password', None)

        if old_password:
            userModel = FrontUserModel.objects.filter(pk=request.front_user.id).first()
            logger.info({'userModel': userModel.username, 'old_password': 'hidden', 'new_password': 'hidden', })
            if userModel:
                check_password_result = userModel.check_password(old_password)
                if check_password_result:
                    if new_password:
                        if repeat_password:
                            if new_password == repeat_password:
                                if len(new_password) >= 4 and len(new_password) <= 16:
                                     userModel.update_password(new_password)
                                     return json_result(message=u'密码修改成功!')
                                else:
                                    return json_params_error(message=u'请输入4-16位长度的密码!')
                            else:
                                return json_params_error(message=u'两次密码不一致!')
                        else:
                            return json_params_error(message=u'请再次输入密码!')
                    else:
                        return json_params_error(message=u'请输入新密码!')
                else:
                    return json_params_error(message=u'原始密码错误!')
            else:
                return json_params_error(message=u'用户不存在/登录超时!')
        else:
            return json_params_error(message=u'请输入现有密码!')


# 退出账号
def front_logout(request):
    logout(request)
    return redirect(reverse('front_method'))

# 慢阻肺专项退出账号
def front_logout_network (request):
    logout(request)
    return redirect(reverse('front_network'))

# 专业科室
# 这里调用微信端的专业科室
@front_login_required
def front_professional_sections(request, department_id=0):
    departmentId = int(department_id)
    return professional_sections(request, departmentId)


# 专业职称
# 这里调用微信端的专业职称
@front_login_required
def front_job_title(request, job_id=0):
    jobId = int(job_id)
    return job_title(request, jobId)


# 个人信息中心
@require_http_methods(['GET', 'POST'])
@front_login_required
def user_info(request):
    if request.method == 'GET':
        userModel = FrontUserModel.objects.filter(pk=request.front_user.id).first()

        if userModel:
            if userModel.profession:
                profession = userModel.profession
            else:
                profession = None

            if userModel.jobtitle:
                job_title = userModel.jobtitle
            else:
                job_title = None

            # 回答总数
            answerCount = AnswersModel.objects.filter(is_removed=0, author=request.front_user).count()

            context = {
                'id': userModel.id,
                'username': userModel.username,
                'fullname': userModel.full_name,
                'signature': userModel.signature,  # 签名
                'avatar': userModel.avatar,
                'gender': userModel.gender,
                'email': userModel.email,
                'email_validated': userModel.email_validated,
                'phone': userModel.phone,
                'phone_validated': userModel.phone_validated,
                'mobile': userModel.mobile,
                'contact_email': userModel.contact_email,
                'corporation': userModel.corporation,  # 公司
                'profession': profession.serialize() if profession else None,  # 科室
                'jobTitle': job_title.serialize() if job_title else None,
                'answer_count': answerCount,
            }
            return json_result(data=context)
        else:
            return json_params_error(message=u'用户信息不存在!')
    else:
        signature = request.POST.get('signature', None)
        avatar = request.POST.get('avatar', 'yika_admin.png')
        full_name = request.POST.get('fullname','')
        username = request.POST.get('username', request.front_user.username)
        gender = request.POST.get('gender', None)
        corporation = request.POST.get('corporation', None)
        professionId = request.POST.get('profession_id', None)
        jobId = request.POST.get('job_id', None)
        mobile = request.POST.get('mobile', None)
        contact_email = request.POST.get('contact_email', None)

        try:
            gender = int(gender)
        except:
            pass

        logger.info({
            'signature': signature,
            'avatar': avatar,
            'username': username,
            'fullname': full_name,
            'gender': gender,
            'corporation': corporation,
            'professionId': professionId,
            'jobId': jobId,
            'moble': mobile,
            'contact_email': contact_email,
        })

        # 判断提交的科室是否存在且为最后一级
        if professionId:
            professionModel = ProfessionalSectionsModel.objects.filter(
                Q(pk=professionId) & ~Q(professional_section=professionId)).first()
            if not professionModel:
                return json_params_error(message=u'你选择的科室不存在!')
        else:
            return json_params_error(message=u'请选择科室!')

        # 判断提交的职称是否存在且为最后一级
        if jobId:
            jobTitleModel = JobTitleModel.objects.filter(Q(pk=jobId) & ~Q(job_title=jobId)).first()
            if not jobTitleModel:
                return json_params_error(message=u'你选择的职称不存在!')
        else:
            return json_params_error(message=u'请选择职称!')


        # 判断用户名是否重复
        if username:
            username = username.replace(' ', '')  # 去除空格
            if username in configs.ILLEGALITY_NAME:
                return json_params_error(message=u'用户名非法!')
            if re.match('^\d*$',username):
                return json_params_error(message=u'用户名不能是纯数字')
            pattern = re.compile(u"^[\w\u4e00-\u9fa5]+$")
            if not re.match(pattern,username):
                return json_params_error(message=u'用户名只能为数字、大小写字母、下划线和汉字')

            if len(username) < 2 or len(username) > 16:
                return json_params_error(message=u'请输入2-16位的用户名!')
            # TODO  建议修改为通过id和username过滤自身
            userModel = FrontUserModel.objects.filter(username=username).first()
            if userModel:
                # 如果查出来的用户id 和当前提交的用户的id不相同，表示不是同一个人
                if userModel.id != request.front_user.id:
                    return json_params_error(message=u'该用户名已被使用!')
        else:
            return json_params_error(message=u'请输入2-16位的用户名!')

        userInfoModel = FrontUserModel.objects.filter(pk=request.front_user.id).first()

        if userInfoModel:

            if gender in [0, 1, 2]:
                # avatar_path = os.path.join(settings.BASE_DIR,'images/avatar/').replace("\\", "/")
                if gender == 0 and not avatar:
                    avatar_list = ['man1.png', 'man2.png', 'man3.png']
                    userInfoModel.avatar = random.choice(avatar_list)
                elif gender == 1 and not avatar:
                    avatar_list = ['woman1.png', 'woman2.png', 'woman3.png']
                    userInfoModel.avatar = random.choice(avatar_list)
                elif gender == 2 and not avatar:
                    userInfoModel.avatar = 'yika_admin.png'
                else:
                    userInfoModel.avatar = avatar
            else:
                return json_params_error(message=u'请选择真实性别!')

            userInfoModel.signature = signature
            userInfoModel.username = username
            userInfoModel.gender = gender
            userInfoModel.corporation = corporation
            userInfoModel.profession = professionModel
            userInfoModel.jobtitle = jobTitleModel
            userInfoModel.full_name = full_name
            #在这里不允许修改手机和邮箱，这个由单独的接口去实现。
            userInfoModel.mobile = mobile
            userInfoModel.contact_email = contact_email
            userInfoModel.save(
                update_fields=['signature', 'username', 'full_name', 'gender', 'corporation', 'profession', 'jobtitle',
                               'avatar', 'mobile', 'contact_email'])
            return json_result(message=u'个人信息修改成功!')
        else:
            return json_params_error(message=u'你尝试修改一个不存在的用户信息!')


# 文章列表 由于研究方法和研究进展页面渲染方式不同，因此分开渲染
def article_list(request, section_id=1, page=1):
    # 所属版块，0:全部 1:研究方法 2.研究进展
    try:
        sectionId = int(section_id)
        currentPage = int(page)
    except:
        pass

    if not sectionId:
        sectionId = 1
    if not currentPage:
        currentPage = 1

    start = 0
    end = currentPage * int(configs.PC_FRONT_NUM_PAGE)

    # 过滤出 状态为 发布和推荐的文章
    if sectionId:
        sectionIdModel = SectionModel.objects.filter(pk=sectionId).first()

        if sectionIdModel:
            articleModel = ArticleModel.objects.filter(section=sectionIdModel, status__in=[1, 2]).all()
            if articleModel:
                context = {
                    'article_count': articleModel.count()
                }
                tmp_article_list = []
                for article in articleModel:
                    comment_count = article.commentmodel_set.filter(status=1, relevance_comment=None).all().count()
                    tmp_article_list.append({
                        'id': article.id,
                        'title': article.title,
                        'summary': article.summary,
                        'thumbnail': article.thumbnail,
                        'publish_time': comment_time_period(article.publish_time),
                        'section': article.section.id,
                        'comment_count': comment_count,
                    })

                context['articles'] = tmp_article_list[start:end]
                context['current_page'] = currentPage
                return context
            else:
                return {'message': u'这是一片没有知识存在的荒原!'}
        else:
            return {'message': u'你尝试查看一个不存在的分类!'}


# 研究方法页面
def study_method(request, section_id=1, page=1):
    context = article_list(request, section_id=section_id, page=page)
    return render(request, 'front_study_method.html', context=context)


# 研究进展页面
def study_evolve(request, section_id=2, page=1):
    context = article_list(request, section_id=section_id, page=page)
    return render(request, 'front_study_evolve.html', context=context)


# 文章详情
def article_detail(request, article_id=0):
    try:
        articleId = int(article_id)
    except:
        pass

    if articleId:
        articleModel = ArticleModel.objects.filter(pk=articleId, status__in=[1, 2]).first()
        if articleModel:
            # 统计文章阅读量
            readArticleCountModel = ReadArticleCountModel.objects.filter(article=articleModel).first()
            if readArticleCountModel:
                readArticleCountModel.read_count += 1
                readArticleCountModel.save(update_fields=['read_count'])
            else:
                readArticleCountModel = ReadArticleCountModel(article=articleModel, read_count=1)
                readArticleCountModel.save()

            # 获取文章对应的标签
            tags = articleModel.tags.all()
            tmp_tags = []
            if tags:
                for t in tags:
                    tmp_tags.append({
                        'id': t.id,
                        'tag': t.tag,
                    })
            # 获取文章的评论
            commentModel = articleModel.commentmodel_set.filter(status=1, relevance_comment=None).all()
            tmp_comment = []
            if commentModel:
                for c in commentModel:
                    # 查找每个一级评论关联的二级评论
                    secondLevelCommentModel = CommentModel.objects.filter(status=1, relevance_comment=c).all()
                    # 如果secondLevelCommentModel为真，表示有二级评论，反之则没有
                    if secondLevelCommentModel:
                        tmp_second_level_comment = []
                        for s in secondLevelCommentModel:
                            tmp_second_level_comment.append({
                                'id': s.id,
                                'avatar': s.author.avatar,
                                'username': s.author.username,
                                'comment': s.comment,
                                'create_time': comment_time_period(s.create_time),
                            })
                        # 将一级评论和关联的二级评论同时返回
                        tmp_comment.append({
                            'id': c.id,
                            'avatar': c.author.avatar,
                            'username': c.author.username,
                            'comment': c.comment,
                            'create_time': comment_time_period(c.create_time),

                            'second_level_comment': tmp_second_level_comment,
                        })
                    else:
                        # 表示没有二级评论
                        tmp_comment.append({
                            'id': c.id,
                            'avatar': c.author.avatar,
                            'username': c.author.username,
                            'comment': c.comment,
                            'create_time': comment_time_period(c.create_time),
                            'second_level_comment': None,
                        })

            context = {
                'id': articleModel.id,
                'title': articleModel.title,
                'content': articleModel.content,
                'publish_time': comment_time_period(articleModel.publish_time),
                'tags': tmp_tags,
                'comments': tmp_comment,
                'comment_count': commentModel.count(),
            }

            return render(request, 'front_article_detail.html', context=context)
        else:
            return render(request, 'front_article_detail.html', {'message': u'没有发表此文章!'})
    else:
        return render(request, 'front_article_detail.html', {'message': u'这是一片没有知识存在的荒原!'})


# 发表评论
@require_http_methods(['GET', 'POST'])
@front_login_required
@front_user_infomation_is_full
def add_comment(request):
    articleId = request.POST.get('article_id', None)
    comment = request.POST.get('comment', None)
    relevanceCommentId = request.POST.get('relevance_comment_id', None)

    logger.info({'articleId': articleId, 'comment': comment, 'relevanceCommentId': relevanceCommentId})

    if articleId:
        if comment:
            articleModel = ArticleModel.objects.filter(Q(status=1) | Q(status=2), pk=articleId).first()
            if articleModel:
                # 如果关联的评论为真,则表示添加的是二级评论
                if relevanceCommentId:
                    relevanceCommentModel = CommentModel.objects.filter(pk=relevanceCommentId, status=1).first()
                    if relevanceCommentModel:
                        commentModel = CommentModel(author=request.front_user, article=articleModel, comment=comment,
                                                    relevance_comment=relevanceCommentModel)
                        commentModel.save()
                        return json_result(message=u'成功添加二级评论!')
                    else:
                        return json_params_error(message=u'你尝试评论一个不存在的评论!')
                # 表示添加的是一级评论
                else:
                    commentModel = CommentModel(author=request.front_user, article=articleModel, comment=comment)
                    commentModel.save()
                    return json_result(message=u'成功添加一级评论!')
            else:
                return json_params_error(message=u'你尝试评论一篇不存在的文章!')
        else:
            return json_params_error(message=u'评论内容不能为空!')
    else:
        return json_params_error(message=u'这是一片没有知识存在的荒原!')


# 热门文章
def hot_articles(request):
    articleModel = ArticleModel.objects.filter(status=2).all()

    if articleModel:
        articleModel = list(articleModel)[0:4]
        tmp_article = []
        for article in articleModel:
            tmp_article.append({
                'id': article.id,
                'title': article.title,
                'publish_time': comment_time_period(article.publish_time),
            })
        context = {
            'hot_articles': tmp_article,
        }
        return json_result(data=context)


# 搜索研究方法和研究进展文章
@require_http_methods(['POST'])
def search_article(request, section_id=1, time_id=1, page=1):
    '''
		mark:20171220
		1、研究方法和研究进展做了区分，因此搜索的查询方式需要重新修改
	'''

    search_key_words = request.POST.get('search_key_words', '')
    try:
        sectionId = int(section_id)
        timeId = int(time_id)
        currentPage = int(page)
        search_key_words = str(search_key_words).strip()

    except:
        pass

    numPage = int(configs.PC_FRONT_NUM_PAGE)
    end = currentPage * numPage

    logger.info({
        'section_id': sectionId,
        'time_id': timeId,
        'search_key_words': search_key_words,
    })
    if sectionId:
        if timeId:
            # 如果sectionModel.id == 1 表示是研究方法，从新表(MethodArticleInfoModel)中查询
            # time==1:表示一周内,  time==2:表示一个月内, time==3:表示三个月内, time==4:表示一年内
            if sectionId == 1:
                if timeId == 1:
                    tmp_articleModel = MethodArticleInfoModel.objects.filter(
                        Q(methodarticlecontentmodel__content__icontains=search_key_words) |
                        Q(title__icontains=search_key_words) |
                        Q(summary__icontains=search_key_words),
                        status__in=[1, 2],
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=7),
                    )
                elif timeId == 2:
                    tmp_articleModel = MethodArticleInfoModel.objects.filter(
                        Q(methodarticlecontentmodel__content__icontains=search_key_words) |
                        Q(title__icontains=search_key_words) |
                        Q(summary__icontains=search_key_words),
                        status__in=[1, 2],
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=30),
                    )
                elif timeId == 3:
                    tmp_articleModel = MethodArticleInfoModel.objects.filter(
                        Q(methodarticlecontentmodel__content__icontains=search_key_words) |
                        Q(title__icontains=search_key_words) |
                        Q(summary__icontains=search_key_words),
                        status__in=[1, 2],
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=90),
                    )
                elif timeId == 4:
                    tmp_articleModel = MethodArticleInfoModel.objects.filter(
                        Q(methodarticlecontentmodel__content__icontains=search_key_words) |
                        Q(title__icontains=search_key_words) |
                        Q(summary__icontains=search_key_words),
                        status__in=[1, 2],
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=365),
                    )

                else:
                    return json_params_error(message=u'选择的时间段错误!')

                # 由于文章内容分多个版块,因此需要将检索出来的模型去重，并保持排序不变
                articleModel = []
                for t in tmp_articleModel:
                    if t not in articleModel:
                        articleModel.append(t)

            # 表示研究进展的搜索
            elif sectionId == 2:

                if timeId == 1:
                    articleModel = NewsModel.objects.filter(
                        Q(title__icontains=search_key_words) |
                        Q(summary__icontains=search_key_words) |
                        Q(content__icontains=search_key_words),
                        status__in=[1, 2],
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=7)
                    )
                elif timeId == 2:
                    articleModel = NewsModel.objects.filter(
                        Q(title__icontains=search_key_words) |
                        Q(summary__icontains=search_key_words) |
                        Q(content__icontains=search_key_words),
                        status__in=[1, 2],
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=30),
                    )
                elif timeId == 3:
                    articleModel = NewsModel.objects.filter(
                        Q(title__icontains=search_key_words) |
                        Q(summary__icontains=search_key_words) |
                        Q(content__icontains=search_key_words),
                        status__in=[1, 2],
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=90),
                    )
                elif timeId == 4:
                    articleModel = NewsModel.objects.filter(
                        Q(title__icontains=search_key_words) |
                        Q(summary__icontains=search_key_words) |
                        Q(content__icontains=search_key_words),
                        status__in=[1, 2],
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=365),
                    )

                else:
                    return json_params_error(message=u'选择的时间段错误!')
            else:
                return json_params_error(message=u'你查看的分类不存在!')

            if len(articleModel) > 0:
                articleCount = len(articleModel)

                pageCount = articleCount / numPage
                if articleCount % numPage > 0:
                    pageCount += 1

                articleModel = list(articleModel)[0:end]

                tmp_articles = []
                for a in articleModel:
                    # 20171220 由于研究方法改版，研究方法和研究进展数据分开存储，数据库中文章创建时间字段命名不同,因此需要判断读取

                    if hasattr(a, 'create_time'):
                        create_time = a.create_time
                    else:
                        create_time = a.publish_time

                    if a.category:
                        category = a.category.id
                    else:
                        category = None

                    tmp_articles.append({
                        'id': a.id,
                        'title': a.title,
                        'summary': a.summary,
                        'app_thumbnail': a.app_thumbnail,
                        'category_id': category,
                        'create_time': create_time,
                    })

                context = {
                    'articles': tmp_articles,
                    'current_page': currentPage,
                    'article_count': articleCount,
                    'page_count': pageCount,
                }
                return json_result(data=context)
            else:
                return json_params_error(message=u'暂无文章!')
        else:
            return json_params_error(message=u'请选择时间段!')
    else:
        return json_params_error(message=u'请选择分类!')


'''
    功能:搜索研究方法和研究进展文章
    请求方法:POST
    参数:
        query_string:
            page:1 // 页码
        body:
            time_range: 1w, // 可取值：1w, 1m, 3m, 1y, all，分别表示几种不同的时间区间
            article_type: news, // 可取值： news，method，分别表示研究进展和研究方法
            search_in: title, // 可取值：title, content， all ，分别表示在标题、内容、标题和内容中进行搜索
            keyword: xxx, // 搜索的关键字
    return:
        {
            'articles': [{
                id: 188,
                category_id: 13,
                summary: "在病例对照研究中...",
                title: "病例对照研究...",
            }],
            'current_page': 1,
            'article_count': 1,
            'page_count': 1,
        }

'''


def search_articles(request):
    time_range = request.POST.get('time_range', '1w')  # 默认搜索一周的内容
    article_type = request.POST.get('article_type', 'method')  # 默认搜索研究方法
    search_in = request.POST.get('search_in', 'title')  # 默认仅在标题中搜索
    keyword = request.POST.get('keyword', '')

    # 参数检查
    if time_range not in ('1w', '1m', '3m', '1y', 'all'):
        return json_params_error(message=u'选择的时间段错误!')

    if article_type not in ('method', 'news'):
        return json_params_error(message=u'搜索内容类型错误!')

    if search_in not in ('title', 'content', 'all'):
        return json_params_error(message=u'搜索类型错误!')

    if not keyword:
        return json_params_error(message=u'没有提供关键字!')

    # 根据 article_type 确定需要搜索的 model
    Model = MethodArticleInfoModel if article_type == 'method' else NewsModel

    # 拼装筛选请求
    query = Model.objects

    q_title = Q(title__icontains=keyword)
    q_content = Q(methodarticlecontentmodel__content__icontains=keyword) if article_type == 'method' else Q(
        content__icontains=keyword)
    q_summary = Q(summary__icontains=keyword)

    if search_in == 'title':
        query = query.filter(q_title)
    elif search_in == 'content':
        query = query.filter(q_content)
    elif search_in == 'all':
        query = query.filter(q_title | q_content | q_summary)

    time_range_delta_days = {'1w': 7, '1m': 30, '3m': 90, '1y': 365, 'all': None}[time_range]
    if time_range_delta_days:
        query = query.filter(create_time__gte=datetime.date.today() - datetime.timedelta(days=time_range_delta_days))

    # 过滤 status 0：删除  1:发布  2：推荐 3：草稿
    query = query.filter(status__in=[1, 2])

    # 有复杂搜索条件的情况下，加上 distinct() 比较保险
    # 有分页时，必须排序
    query = query.distinct().order_by('-create_time')

    # 接下来使用 Django 的分页
    page = request.GET.get('page', 1)  # 页码一般不放在 URL 中，而是 URL 的 query string 中
    page_size = int(configs.PC_FRONT_NUM_PAGE)  # 这里暂时使用原来代码中的配置
    paginator = Paginator(query, page_size)
    # 在Django 2.0 以上用Paginator.get_page替换下面方法
    try:
        articles = list(paginator.page(page).object_list.values("id", "title", "summary", "category_id"))
    except InvalidPage:
        articles = []

    return json_result(message="请求成功", data={
        'articles': articles,
        'current_page': page,
        'article_count': paginator.count,
        'page_count': paginator.num_pages,
    })


# 按标签检索文章
def search_tag_article(request, tag_id=0, page=1):
    try:
        tagId = int(tag_id)
        currentPage = int(page)
    except:
        pass

    start = (currentPage - 1) * configs.PC_FRONT_NUM_PAGE
    end = start + configs.PC_FRONT_NUM_PAGE

    tagModel = TagsModel.objects.filter(pk=tagId).first()
    if tagModel:
        articleModel = ArticleModel.objects.filter(status__in=[1, 2], tags__in=[tagModel]).values('id', 'title',
                                                                                                  'summary')

        context = {
            'articles': list(articleModel)[start:end],
            'currentPage': currentPage,
            'article_count': articleModel.count()
        }
        return json_result(message=u'查询成功!', data=context)
    else:
        return json_params_error(message=u'标签不存在!')


'''
	date:20170823
	author:zhangx
	mark:
		下面是问答版块的功能
'''


# 研究问答分类列表
def front_question_category_list(request):
    questionCategoryListModel = list(QuestionCategoryModel.objects.values('id', 'category'))

    if questionCategoryListModel:
        context = {
            'question_category_list': questionCategoryListModel,
        }
        return json_result(data=context)


# 研究问答：最新问答
def recently_questions(request, category_id=0, page=1):
    try:
        categoryId = int(category_id)
        currentPage = int(page)
    except:
        pass

    # 定义每页显示条数
    numPage = int(configs.PC_FRONT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    context = {}

    # 将问题分类列表和摘要返回
    questionCategoryListModel = list(QuestionCategoryModel.objects.values('id', 'category', 'summary'))
    if questionCategoryListModel:
        context['question_category_list'] = questionCategoryListModel
    else:
        context['question_category_list'] = None

    # 如果问答分类为真,则过滤出和当前分类相关的问题。否则，展示全部问题
    if categoryId:
        questionCategoryModel = QuestionCategoryModel.objects.filter(pk=categoryId).first()

        if questionCategoryModel:
            recentlyQuestionsModel = QuestionsModel.objects.filter(is_removed=0,category=questionCategoryModel).all() \
                                                   .annotate(last_activity=Coalesce(Greatest('create_time', 'last_answer_time'),'create_time')) \
                                                   .order_by('-last_activity')
            context['question_category'] = questionCategoryModel.summary
            context['category_id'] = questionCategoryModel.id
            context['title'] = questionCategoryModel.category

        else:
            return render(request, 'front_question_category_list.html', {'message': u'你尝试查看一个不存在的分类信息!'})
    else:
        recentlyQuestionsModel = QuestionsModel.objects.filter(is_removed=0).all() \
                                               .annotate(last_activity=Coalesce(Greatest('create_time', 'last_answer_time'),'create_time')) \
                                               .order_by('-last_activity')                                                          
        # 返回全部问答的分类摘要!
        context[
            'question_category'] = u'这里是交流临床研究设计和医学统计问题的平台！你可以：和其他伙伴交流你遇到的统计难题；提出你对某个问题的建议；分享你解决问题的思路和经验。交流、分享、互助——共同提高临床研究水平！'
        context['category_id'] = 0
        context['title'] = u'研究问答'

    if recentlyQuestionsModel:

        questionCount = recentlyQuestionsModel.count()

        pageCount = questionCount / numPage
        if questionCount % numPage > 0:
            pageCount += 1

        pages = []

        # 如果当前页码小于5,那么 pages将[1,2,3,4]填充进去
        # 如果当前页码大于5,那么 需要显示当前页码的左边2个，右边2个页码
        # 当页码为倒数第2页的时候,需要往前查找3页，往后查找1页
        # 如果当前页码是尾页，那么需要往前显示4个页码

        if currentPage < 5:
            tmpPage = currentPage - 1
            while tmpPage >= 1:
                if tmpPage % 5 == 0:
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage -= 1

            tmpPage = currentPage
            while tmpPage <= pageCount:
                if tmpPage % 5 == 0:
                    pages.append(tmpPage)
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage += 1

        elif currentPage + 1 < pageCount:
            # 往前查找2次
            tmpPage = currentPage - 1
            t = 1
            while t < 3:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找3次
            tmpPage = currentPage
            t = 1
            while t < 4:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break

        elif currentPage + 1 == pageCount:
            # 这个判断用来解决当前页码为倒数第2页的时候,只显示4页的bug
            # 往前查找3次
            tmpPage = currentPage - 1
            t = 1
            while t < 4:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找2次
            tmpPage = currentPage
            t = 1
            while t < 3:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break
        else:
            tmpPage = currentPage
            t = 1
            # 往前查找5次
            while t < 6:
                pages.append(tmpPage)
                tmpPage -= 1
                t += 1

        pages.sort()

        recentlyQuestionsModel = recentlyQuestionsModel[start:end]

        tmp_questions = []
        # 遍历过滤后的问题列表,如果当前问题有回复，则取出最后的回复信息，如果没有回复则取出问题信息

        for r in recentlyQuestionsModel:

            # 获取当前问题的分类
            if r.category:
                category = r.category.category
                categoryId = r.category.id
            else:
                category = None

            # 获取当前问题的最新一条回复信息
            lastAnswerModel = AnswersModel.objects.filter(is_removed=0, questions=r).last()
            if lastAnswerModel:
                # 获取当前问题回答总数
                answersCount = AnswersModel.objects.filter(is_removed=0, questions=r).count()

                tmp_questions.append({
                    'question_id': r.id,
                    'content': r.content,
                    'category': category,
                    'question_category_id': categoryId,
                    'top': r.top,
                    'recently_answer_user_id': lastAnswerModel.author.id,
                    'recently_answer_username': lastAnswerModel.author.username,
                    'recently_answer_time': comment_time_period(lastAnswerModel.create_time),
                    'answers_count': answersCount,
                })
            else:
                # 当前问题没有没有回复
                tmp_questions.append({
                    'question_id': r.id,
                    'content': r.content,
                    'category': category,
                    'question_category_id': categoryId,
                    'top': r.top,
                    'username': r.author.username,
                    'create_time': comment_time_period(r.create_time),
                    'answers_count': None,
                })

        context['questions_list'] = tmp_questions
        context['current_page'] = currentPage
        context['page_count'] = pageCount
        context['pages'] = pages
        context['index'] = 'front_recently_questions'  # 把当前的url返回供加载更多翻页使用
        # webapp需要调用此接口
        if request.is_ajax():
            return json_result(data=context)
        else:
            return render(request, 'front_question_category_list.html', context=context)
    else:
        # webapp需要调用此接口
        if request.is_ajax():
            return json_result(data=context)
        else:
            return render(request, 'front_question_category_list.html', context=context)


# 研究问答：热门问答
def hold_questions(request, category_id=0, page=1):
    try:
        categoryId = int(category_id)
        currentPage = int(page)
    except:
        pass

    # 定义每页显示条数
    numPage = int(configs.PC_FRONT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    context = {}

    # 将问题分类列表和摘要返回
    questionCategoryListModel = list(QuestionCategoryModel.objects.values('id', 'category', 'summary'))
    if questionCategoryListModel:
        context['question_category_list'] = questionCategoryListModel
    else:
        context['question_category_list'] = None

    # 如果问答分类为真,则过滤出和当前分类相关的问题。否则，展示全部问题
    if categoryId:
        questionCategoryModel = QuestionCategoryModel.objects.filter(pk=categoryId).first()

        if questionCategoryModel:
            # 给问题模型增加answer_count评论总数属性，并且过滤掉已删除的评论。再按照评论总数排序
            holdQuestionModel = QuestionsModel.objects.filter(
                create_time__gte=datetime.date.today() - datetime.timedelta(days=30), is_removed=0,
                category=questionCategoryModel, answersmodel__is_removed=0).annotate(
                answer_count=Count('answersmodel')).order_by('-top', '-answer_count').all()

            context['question_category'] = questionCategoryModel.summary
            context['category_id'] = questionCategoryModel.id
            context['title'] = questionCategoryModel.category

        else:
            return render(request, 'front_question_category_list.html', {'message': u'你尝试查看一个不存在的分类信息!'})
    else:
        holdQuestionModel = QuestionsModel.objects.filter(
            create_time__gte=datetime.date.today() - datetime.timedelta(days=30), is_removed=0,
            answersmodel__is_removed=0).annotate(answer_count=Count('answersmodel')).order_by('-top',
                                                                                              '-answer_count').all()

        # 返回全部问答的分类摘要!
        context['question_category'] = u'临床研究的过程中，经常遇到研究设计和统计难题？赶快在这里提问吧！我们的伙伴中有医生、统计专业人士、临床研究领域资深专家…听听他们的答案，一定能让你茅塞顿开!'
        context['category_id'] = 0
        context['title'] = u'研究问答'

    if holdQuestionModel:

        questionCount = holdQuestionModel.count()

        pageCount = questionCount / numPage
        if questionCount % numPage > 0:
            pageCount += 1

        pages = []

        # 如果当前页码小于5,那么 pages将[1,2,3,4]填充进去
        # 如果当前页码大于5,那么 需要显示当前页码的左边2个，右边2个页码
        # 当页码为倒数第2页的时候,需要往前查找3页，往后查找1页
        # 如果当前页码是尾页，那么需要往前显示4个页码

        if currentPage < 5:
            tmpPage = currentPage - 1
            while tmpPage >= 1:
                if tmpPage % 5 == 0:
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage -= 1

            tmpPage = currentPage
            while tmpPage <= pageCount:
                if tmpPage % 5 == 0:
                    pages.append(tmpPage)
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage += 1

        elif currentPage + 1 < pageCount:
            # 往前查找2次
            tmpPage = currentPage - 1
            t = 1
            while t < 3:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找3次
            tmpPage = currentPage
            t = 1
            while t < 4:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break

        elif currentPage + 1 == pageCount:
            # 这个判断用来解决当前页码为倒数第2页的时候,只显示4页的bug
            # 往前查找3次
            tmpPage = currentPage - 1
            t = 1
            while t < 4:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找2次
            tmpPage = currentPage
            t = 1
            while t < 3:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break
        else:
            tmpPage = currentPage
            t = 1
            # 往前查找5次
            while t < 6:
                pages.append(tmpPage)
                tmpPage -= 1
                t += 1

        pages.sort()

        holdQuestionModel = holdQuestionModel[start:end]

        # 根据问题，查询最后回复当前问题的用户
        tmp_questions = []
        for r in holdQuestionModel:
            # 获取当前问题的最新一条回复信息
            lastAnswerModel = AnswersModel.objects.filter(is_removed=0, questions=r).last()
            # 获取当前问题的分类
            if r.category:
                category = r.category.category
                categoryId = r.category.id
            else:
                category = None

            # 获取当前问题回答总数
            answersCount = AnswersModel.objects.filter(is_removed=0, questions=r).count()

            tmp_questions.append({
                'question_id': r.id,
                'content': r.content,
                'category': category,
                'question_category_id': categoryId,
                'top': r.top,
                'recently_answer_user_id': lastAnswerModel.author.id,
                'recently_answer_username': lastAnswerModel.author.username,
                'recently_answer_time': comment_time_period(lastAnswerModel.create_time),
                'answers_count': answersCount,
            })

        context['questions_list'] = tmp_questions
        context['current_page'] = currentPage
        context['page_count'] = pageCount
        context['pages'] = pages
        context['index'] = 'front_hold_questions'

        if request.is_ajax():
            return json_result(data=context)
        else:
            return render(request, 'front_question_category_list.html', context=context)
    else:
        if request.is_ajax():
            return json_result(data=context)
        else:
            return render(request, 'front_question_category_list.html', context=context)


# 研究问答：等待问答
def wait_relay_questions(request, category_id=0, page=1):
    try:
        categoryId = int(category_id)
        currentPage = int(page)
    except:
        pass

    # 定义每页显示条数
    numPage = int(configs.PC_FRONT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    context = {}

    # 将问题分类列表和摘要返回
    questionCategoryListModel = list(QuestionCategoryModel.objects.values('id', 'category', 'summary'))
    if questionCategoryListModel:
        context['question_category_list'] = questionCategoryListModel
    else:
        context['question_category_list'] = None

    if categoryId:
        questionCategoryModel = QuestionCategoryModel.objects.filter(pk=categoryId).first()
        if questionCategoryModel:
            AllQuestionsModel = QuestionsModel.objects.filter(is_removed=0, category=questionCategoryModel).order_by(
                '-top', '-last_answer_time', '-create_time')

            context['question_category'] = questionCategoryModel.summary
            context['category_id'] = questionCategoryModel.id
            context['title'] = questionCategoryModel.category

        else:
            return render(request, 'front_question_category_list.html', {'message': u'你尝试查看一个不存在的分类信息!'})
    else:
        AllQuestionsModel = QuestionsModel.objects.filter(is_removed=0).order_by('-top', '-last_answer_time',
                                                                                 '-create_time')

        # 返回全部问答的分类摘要!
        context['question_category'] = u'临床研究的过程中，经常遇到研究设计和统计难题？赶快在这里提问吧！我们的伙伴中有医生、统计专业人士、临床研究领域资深专家…听听他们的答案，一定能让你茅塞顿开!'
        context['category_id'] = 0
        context['title'] = u'研究问答'
    '''
		1、先查找出当前分类或者所有分类下的问题
		2、然后遍历问题,检索出回答表中没有的问题
		3、将回答表中没有的问题存入临时列表
	'''

    if AllQuestionsModel:
        questionsList = []
        for question in AllQuestionsModel:
            waitRelayQuestionsModel = AnswersModel.objects.filter(is_removed=0, questions=question).first()

            # 如果当前问题在回答列表中不存在，则表示当前问题是没有回答的问题
            if not waitRelayQuestionsModel:
                if question.category:
                    category = question.category.category
                    categoryId = question.category.id
                else:
                    category = None

                questionsList.append({
                    'question_id': question.id,
                    'content': question.content,
                    'category': category,
                    'question_category_id': categoryId,
                    'top': question.top,
                    'username': question.author.username,
                    'create_time': comment_time_period(question.create_time),
                    'answers_count': None,
                })

        questionCount = len(questionsList)
        pageCount = questionCount / numPage
        if questionCount % numPage > 0:
            pageCount += 1

        pages = []

        # 如果当前页码小于5,那么 pages将[1,2,3,4]填充进去
        # 如果当前页码大于5,那么 需要显示当前页码的左边2个，右边2个页码
        # 当页码为倒数第2页的时候,需要往前查找3页，往后查找1页
        # 如果当前页码是尾页，那么需要往前显示4个页码

        if currentPage < 5:
            tmpPage = currentPage - 1
            while tmpPage >= 1:
                if tmpPage % 5 == 0:
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage -= 1

            tmpPage = currentPage
            while tmpPage <= pageCount:
                if tmpPage % 5 == 0:
                    pages.append(tmpPage)
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage += 1

        elif currentPage + 1 < pageCount:
            # 往前查找2次
            tmpPage = currentPage - 1
            t = 1
            while t < 3:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找3次
            tmpPage = currentPage
            t = 1
            while t < 4:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break

        elif currentPage + 1 == pageCount:
            # 这个判断用来解决当前页码为倒数第2页的时候,只显示4页的bug
            # 往前查找3次
            tmpPage = currentPage - 1
            t = 1
            while t < 4:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找2次
            tmpPage = currentPage
            t = 1
            while t < 3:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break
        else:
            tmpPage = currentPage
            t = 1
            # 往前查找5次
            while t < 6:
                pages.append(tmpPage)
                tmpPage -= 1
                t += 1

        pages.sort()

        context['page_count'] = pageCount
        context['pages'] = pages
        context['questions_list'] = questionsList[start:end]
        context['current_page'] = currentPage
        context['index'] = 'front_wait_relay_questions'

        return render(request, 'front_question_category_list.html', context=context)
    else:
        return render(request, 'front_question_category_list.html', context=context)


# 研究问答：发表评论
@require_http_methods(['GET', 'POST'])
@front_login_required
@front_user_infomation_is_full
def front_add_answer(request):
    # 调用common接口中的add_answer方法
    return add_answer(request)


# 研究问答：活跃用户排行榜
def active_users_ranking(request, category_id=0, time_id=0):
    try:
        categoryId = int(category_id)
        timeId = int(time_id)
    except:
        pass

    if categoryId:
        questionCategoryModel = QuestionCategoryModel.objects.filter(pk=categoryId).first()
        if questionCategoryModel:
            questionsModel = QuestionsModel.objects.filter(category=questionCategoryModel, is_removed=0).all()

            '''
				用户活跃排行榜解决方案:
				1、先根据分类查出当前分类下的所有问题
				2、然后将当前分类下的所有问题模型存入临时列表中
				3、然后从问答列表中过滤出相关的回答
				4、然后将回答列表去重，统计回答的用户数量
				5、取回答数最高的10个
			'''
            if questionsModel:
                tmp_questions_list = []
                for q in questionsModel:
                    tmp_questions_list.append(q)

                if timeId == 1:
                    activeUsersRankingModel = AnswersModel.objects.filter(is_removed=0,
                                                                          questions__in=tmp_questions_list,
                                                                          create_time__gte=datetime.date.today() - datetime.timedelta(
                                                                              days=7)).all()
                elif timeId == 2:
                    activeUsersRankingModel = AnswersModel.objects.filter(is_removed=0,
                                                                          questions__in=tmp_questions_list,
                                                                          create_time__gte=datetime.date.today() - datetime.timedelta(
                                                                              days=30)).all()
                else:
                    activeUsersRankingModel = AnswersModel.objects.filter(is_removed=0,
                                                                          questions__in=tmp_questions_list).all()
            else:
                return json_params_error(message=u'暂无活跃用户排行榜!')
        else:
            return json_params_error(message=u'你尝试查看一个不存在的问答分类!')

    else:
        # 返回所有分类下活跃用户排行榜
        if timeId == 1:
            activeUsersRankingModel = AnswersModel.objects.filter(is_removed=0,
                                                                  create_time__gte=datetime.date.today() - datetime.timedelta(
                                                                      days=7)).all()
        elif timeId == 2:
            activeUsersRankingModel = AnswersModel.objects.filter(is_removed=0,
                                                                  create_time__gte=datetime.date.today() - datetime.timedelta(
                                                                      days=30)).all()
        else:
            activeUsersRankingModel = AnswersModel.objects.filter(is_removed=0, ).all()

    if activeUsersRankingModel:
        users_ranking = []
        for a in activeUsersRankingModel:
            users_ranking.append(a.author.id)  # 将用户id存储在列表中

        # 将回答列表去重
        set_users_ranking = list(set(users_ranking))
        rank = []
        for s in set_users_ranking:
            userModel = FrontUserModel.objects.filter(pk=s).first()
            rank.append({
                'user_id': userModel.id,
                'username': userModel.username,
                'avatar': userModel.avatar,
                'active_count': users_ranking.count(s),
            })

        rank.sort(reverse=True)
        rank = rank[:10]

        return json_result(data=rank)
    else:
        return json_params_error(message=u'此分类下暂无问答!')


# 研究问答：问题详情
def front_question_detail(request, question_id=0, answer_id=0, parent_page=1, child_page=1):
    context = question_detail(request, question_id=question_id, answer_id=answer_id, parent_page=parent_page,
                              child_page=child_page)
    # 将问题分类列表和摘要返回
    questionCategoryListModel = list(QuestionCategoryModel.objects.values('id', 'category', 'summary'))
    if questionCategoryListModel:
        context['question_category_list'] = questionCategoryListModel
    else:
        context['question_category_list'] = None

    if request.is_ajax():
        return json_result(data=context)
    else:
        return render(request, 'front_question_detail.html', context=context)


# 研究问答：发表问题
@require_http_methods(['GET', 'POST'])
@front_login_required
@front_user_infomation_is_full  # 个人资料是否完善
def front_release_question(request):
    if request.method == 'GET':
        return json_result(message=u'这里是发布问题页面!')
    else:
        content = request.POST.get('content', None)
        questionCategoryId = request.POST.get('question_category_id', 0)
        relevanceMethodArticleId = request.POST.get('relevance_method_article_id', None)

        logger.info({'question_category_id': questionCategoryId, 'content': content})

        if content:
            if questionCategoryId:
                questionCategoryModel = QuestionCategoryModel.objects.filter(pk=questionCategoryId).first()
                if questionCategoryModel:

                    logger.info(
                        {'user': request.front_user.username, 'user_id': request.front_user.id, 'content': content})

                    # 20171212 如果关联的研究方法文章为真,则关联
                    if relevanceMethodArticleId:
                        methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=relevanceMethodArticleId,
                                                                                       status__in=[1, 2]).first()
                        if methodArticleInfoModel:
                            # 若关联的文章为更多教程文章，那么需要把修改文章跳转的详情页面
                            questionModel = QuestionsModel(author=request.front_user, content=content,
                                                           category=questionCategoryModel,
                                                           last_answer_time=datetime.datetime.now(),
                                                           relevance_method_article=methodArticleInfoModel)
                            questionModel.save()

                            return json_result(message=u'发布问题成功!')
                        else:
                            return json_params_error(message=u'你尝试对一篇不存在的文章进行提问!')
                    else:
                        questionModel = QuestionsModel(author=request.front_user, content=content,
                                                       category=questionCategoryModel,
                                                       last_answer_time=datetime.datetime.now())
                        questionModel.save()
                        return json_result(message=u'发布问题成功!')
                else:
                    return json_params_error(message=u'你尝试在一个不存在的分类下发表问题!')
            else:
                return json_params_error(message=u'请选择分类!')
        else:
            return json_params_error(message=u'内容不能为空!')


# 研究问答：搜索功能
@require_http_methods(['GET', 'POST'])
def search_questions_and_answers(request, section_id=3, time=1, page=1):
    search_key_words = request.POST.get('search_key_words', '')
    try:
        sectionId = int(section_id)
        time = int(time)
        currentPage = int(page)
        search_key_words = str(search_key_words).strip()
    except:
        pass

    numPage = int(configs.PC_FRONT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = currentPage * numPage

    context = {}

    if sectionId:
        if search_key_words:
            # 表示类型是研究问答
            if sectionId == 3:
                # time==1:表示一周内,  time==2:表示一个月内, time==3:表示三个月内, time==4:表示一年内
                # datetime.timedelta() 此函数可以操作天,小时,分钟,秒,毫秒
                if time == 1:
                    recentlyQuestionsModel = QuestionsModel.objects.filter(
                        is_removed=0,
                        content__icontains=search_key_words,
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=7),
                    ).order_by('-last_answer_time', '-create_time').all()[start:end]
                elif time == 2:
                    recentlyQuestionsModel = QuestionsModel.objects.filter(
                        is_removed=0,
                        content__icontains=search_key_words,
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=30),
                    ).order_by('-last_answer_time', '-create_time').all()[start:end]
                elif time == 3:
                    recentlyQuestionsModel = QuestionsModel.objects.filter(
                        is_removed=0,
                        content__icontains=search_key_words,
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=90),
                    ).order_by('-last_answer_time', '-create_time').all()[start:end]
                elif time == 4:
                    recentlyQuestionsModel = QuestionsModel.objects.filter(
                        is_removed=0,
                        content__icontains=search_key_words,
                        create_time__gte=datetime.date.today() - datetime.timedelta(days=365),
                    ).order_by('-last_answer_time', '-create_time').all()[start:end]
                else:
                    recentlyQuestionsModel = QuestionsModel.objects.filter(
                        is_removed=0,
                        content__icontains=search_key_words,
                    ).order_by('-last_answer_time', '-create_time').all()[start:end]

                if recentlyQuestionsModel:

                    questionCount = recentlyQuestionsModel.count()

                    pageCount = questionCount / numPage
                    if questionCount % numPage > 0:
                        pageCount += 1

                    # recentlyQuestionsModel = list(recentlyQuestionsModel)[0:end]

                    tmp_questions = []
                    # 遍历过滤后的问题列表,如果当前问题有回复，则取出最后的回复信息，如果没有回复则取出问题信息

                    for r in recentlyQuestionsModel:

                        # 获取当前问题的分类
                        if r.category:
                            category = r.category.category
                        else:
                            category = None

                        # 获取当前问题的最新一条回复信息
                        lastAnswerModel = AnswersModel.objects.filter(is_removed=0, questions=r).last()

                        if lastAnswerModel:
                            # 获取当前问题回答总数
                            answersCount = AnswersModel.objects.filter(is_removed=0, questions=r).count()

                            tmp_questions.append({
                                'question_id': r.id,
                                'content': r.content,
                                'category': category,
                                'create_time': comment_time_period(r.create_time),  # 问题创建时间,用于搜索页面的混合排序
                                'recently_answer_user_id': lastAnswerModel.author.id,
                                'recently_answer_username': lastAnswerModel.author.username,
                                'recently_answer_time': comment_time_period(lastAnswerModel.create_time),
                                'answers_count': answersCount,
                            })
                        else:
                            # 当前问题没有没有回复
                            tmp_questions.append({
                                'question_id': r.id,
                                'content': r.content,
                                'category': category,
                                'username': r.author.username,
                                'create_time': comment_time_period(r.create_time),
                                'answers_count': None,
                            })

                    context = {
                        'page_count': pageCount,
                        'current_page': currentPage,
                        'questions_list': tmp_questions,
                        'question_count': questionCount,
                    }

                    return json_result(message=u'查询成功!', data=context)
                else:
                    return json_params_error(message=u'暂无问答!')
            else:
                return json_params_error(message=u'你查看的分类不存在!')
        else:
            return json_params_error(message=u'请输入搜索关键词!')
    else:
        return json_params_error(message=u'请选择分类!')


'''
    功能：搜索研究问答
    方法： POST
    参数：
        query_string:
            page:1 //页码
        body:
            time_range: 1w,         //可取值：1w,1m,3m,1y,all,分别表示几种不同的时间区间
            question_category: all, // 可取值: all, 目前只有all表示问题类别
            keyword:xxx,            //搜索的关键字
    return:
        {
            questions:[
                //无回复
                {
                    answers_count: null,
                    category: "其他",
                    content: "<p>123</p>",
                    create_time: "17天前",
                    question_id: 1763,
                    username: "马萌",
                },
                //有回复
                {
                    answers_count: 1,
                    category: "统计方法",
                    content: "在stata 14中保存log file",
                    create_time: "2018-07-18",
                    question_id: 1589,
                    recently_answer_time: "2018-07-19",
                    recently_answer_user_id: 167,
                    recently_answer_username: "Brian",
                }
            ],
            current_page:1,
            page_count:1,
            question_count:1,
        }
'''


@require_http_methods(['POST'])
def search_questions(request):
    keyword = request.POST.get("keyword", "")
    time_range = request.POST.get("time_range", "1w")
    question_category = request.POST.get("question_category", "all")

    if time_range not in ["1w", "1m", "3m", "1y", "all"]:
        return json_params_error(message="时间范围错误")
    if question_category not in ["all"]:
        return json_params_error(message="问题类别错误")
    if not keyword:
        return json_params_error(message="搜索关键字缺失")

    # is_remmoved 0：未删除 1：已删除
    query = QuestionsModel.objects.filter(is_removed=0)
    # 过滤关键字
    query = query.filter(content__icontains=keyword)
    # 过滤时间
    time_range_delta_days = {'1w': 7, '1m': 30, '3m': 90, '1y': 365, 'all': None}[time_range]
    if time_range_delta_days:
        query = query.filter(create_time__gte=datetime.date.today() - datetime.timedelta(days=time_range_delta_days))

    # 查询问题相关的类型，作者
    query = query.select_related("category", "author")

    # 高版本Django考虑使用OuterRef,Subquery减少prefetch_related数量
    query = query.prefetch_related(
        Prefetch("answersmodel_set", queryset=AnswersModel.objects.filter(is_removed=0).select_related('author'))
    )

    # 排序
    query = query.order_by('-last_answer_time', '-create_time')
    # 查询未删除的回答总数
    query = query.annotate(num_answers=Count(
        Case(
            When(answersmodel__is_removed=0, then="answersmodel")
        )
    ))

    page = request.GET.get('page', 1)
    page_size = int(configs.PC_FRONT_NUM_PAGE)
    paginator = Paginator(query, page_size)

    # 在Django 2.0 以上用Paginator.get_page替换下面方法
    try:
        questions = [
            {
                "answers_count": question.num_answers,
                "category": question.category.category,
                "content": question.content,
                "create_time": comment_time_period(question.create_time),
                "question_id": question.id,
                "recently_answer_user_id": question.latest_answer.author.id,
                "recently_answer_time": comment_time_period(question.latest_answer.create_time),
                "recently_answer_username": question.latest_answer.author.username,
            }
            if question.num_answers else
            {
                "answers_count": None,
                'category': question.category.category,
                "content": question.content,
                "create_time": comment_time_period(question.create_time),
                "question_id": question.id,
                "username": question.author.username,
            }
            for question in paginator.page(page).object_list
        ]
    except InvalidPage:
        questions = []
    return json_result(message="请求成功", data={
        "questions": questions,
        "current_page": page,
        "page_count": paginator.num_pages,
        "question_count": paginator.count,
    })


# 关于我们
def about_us(request):
    return render(request, 'about_us.html')


# 学术服务
def science(request):
    return render(request, 'science.html')


def search(request):
    return render(request, 'search.html')


'''
	date:20170907
	author:zhangx
	mark:
		下面是个人中心模块功能，包含收藏回答和点赞回答功能
'''


def user(request):
    # return render(request, 'user.html')
    return render(request, 'user_center/index.html')


# 研究问答：收藏回答和取消收藏回答
@front_login_required
def collect_answer(request, answer_id=0, collect_category_id=0):
    try:
        answerId = int(answer_id)
        collectCategoryId = int(collect_category_id)
    except:
        pass

    logger.info({'answer_id': answerId})

    if answerId:
        answerModel = AnswersModel.objects.filter(pk=answerId).first()
        if answerModel:
            # 判断收藏分类是否存在
            if collectCategoryId:
                userCollectCategoryModel = UserCollectCategoryModel.objects.filter(author=request.front_user,
                                                                                   pk=collectCategoryId).first()
                if userCollectCategoryModel:
                    # 判断收藏模型中是否存在对应的收藏，如果有则删除，否则添加
                    collectAnswerModel = CollectAnswerModel.objects.filter(username=request.front_user,
                                                                           collect_answer=answerModel,
                                                                           collect_category=userCollectCategoryModel).first()
                    if collectAnswerModel:
                        collectAnswerModel.delete()
                        context = {
                            'is_collect': 0,
                        }
                        return json_result(message=u'已取消收藏!', data=context)
                    else:
                        collectAnswerModel = CollectAnswerModel(username=request.front_user, collect_answer=answerModel,
                                                                collect_category=userCollectCategoryModel)
                        collectAnswerModel.save()
                        context = {
                            'is_collect': 1,
                        }
                        return json_result(message=u'收藏成功!', data=context)
                else:
                    return json_params_error(message=u'你尝试查看一个不存在的分类!')
            else:
                # 判断收藏模型中是否存在对应的收藏，如果有则删除，否则添加
                collectAnswerModel = CollectAnswerModel.objects.filter(username=request.front_user,
                                                                       collect_answer=answerModel)
                if collectAnswerModel:
                    collectAnswerModel.delete()
                    context = {
                        'is_collect': 0,
                    }
                    return json_result(message=u'已取消收藏!', data=context)
                else:
                    collectAnswerModel = CollectAnswerModel(username=request.front_user, collect_answer=answerModel)
                    collectAnswerModel.save()
                    context = {
                        'is_collect': 1,
                    }
                    return json_result(message=u'收藏成功!', data=context)
        else:
            return json_params_error(message=u'你尝试收藏一个不存在的回答!')
    else:
        return json_params_error(message=u'你尝试查看一个不存在的回答!')


# 研究问答：点赞回答和取消点赞回答
@front_login_required
def praise_answer(request, answer_id=0):
    try:
        answerId = int(answer_id)
    except:
        pass

    logger.info({'answer_id': answerId})

    if answerId:
        answerModel = AnswersModel.objects.filter(pk=answerId).first()
        if answerModel:
            # 如果可以查到已点赞的记录,就删除。否则添加
            praiseAnswerModel = PraiseAnswerModel.objects.filter(username=request.front_user, praise_answer=answerModel)
            if praiseAnswerModel:
                praiseAnswerModel.delete()
                context = {
                    'is_praise': 0,
                }
                return json_result(message=u'已取消点赞!', data=context)
            else:
                praiseAnswerModel = PraiseAnswerModel(username=request.front_user, praise_answer=answerModel)
                praiseAnswerModel.save()
                context = {
                    'is_praise': 1,
                }
                return json_result(message=u'已点赞!', data=context)
        else:
            return json_params_error(message=u'你尝试点赞一个不存在的回答!')
    else:
        return json_params_error(message=u'你尝试查看一个不存在的回答!')


# 研究问答：用户创建收藏分类
@front_login_required
@require_http_methods(['GET', 'POST'])
def create_user_collect_category(request):
    if request.method == 'GET':
        return json_result(message=u'这里是创建用户自定义收藏夹页面!')
    else:
        collectCategory = request.POST.get('collect_category', None)
        summary = request.POST.get('summary', None)
        try:
            collectCategory = str(collectCategory).strip()
        except:
            pass

        if collectCategory:
            # 判断当前用户创建的收藏分类是否重复
            userCollectCategoryModel = UserCollectCategoryModel.objects.filter(author=request.front_user,
                                                                               collect_category=collectCategory).first()
            if userCollectCategoryModel:
                return json_params_error(message=u'此收藏分类已存在!')
            createUserCollectCategoryModel = UserCollectCategoryModel(author=request.front_user,
                                                                      collect_category=collectCategory, summary=summary)
            createUserCollectCategoryModel.save()
            return json_result(message=u'成功创建收藏分类!')

        else:
            return json_params_error(message=u'收藏夹名称不能为空!')


# 研究问答：用户收藏夹分类列表
@front_login_required
def user_collect_category_list(request):
    userCollectCategoryListModel = UserCollectCategoryModel.objects.filter(author=request.front_user).values('id',
                                                                                                             'collect_category')
    if userCollectCategoryListModel:
        context = {
            'user_collect_category_list': list(userCollectCategoryListModel),
        }
        return json_result(data=context)
    else:
        return json_params_error(message=u'暂未创建收藏夹!')


# 个人中心：修改个人收藏夹
@front_login_required
@require_http_methods(['GET', 'POST'])
def alter_collect_category(request, collect_category_id=0):
    try:
        collectCategoryId = int(collect_category_id)
    except:
        pass

    if collectCategoryId:
        userCollectCategoryModel = UserCollectCategoryModel.objects.filter(pk=collectCategoryId,
                                                                           author=request.front_user).first()
        if userCollectCategoryModel:
            if request.method == 'GET':
                context = {
                    'id': userCollectCategoryModel.id,
                    'collect_category': userCollectCategoryModel.collect_category,
                    'summary': userCollectCategoryModel.summary,
                }
                return json_result(data=context)
            else:
                collectCategory = request.POST.get('collect_category', userCollectCategoryModel.collect_category)
                summary = request.POST.get('summary', userCollectCategoryModel.summary)

                try:
                    collectCategory = str(collectCategory).strip()
                except:
                    pass

                if collectCategory:
                    # 判断收藏夹分类是是否重复
                    repetitionCollectCategoryModel = UserCollectCategoryModel.objects.filter(author=request.front_user,
                                                                                             collect_category=collectCategory).first()
                    if repetitionCollectCategoryModel:
                        if repetitionCollectCategoryModel.id != collectCategoryId:
                            return json_params_error(message=u'此收藏夹已存在!')

                    userCollectCategoryModel.collect_category = collectCategory
                    userCollectCategoryModel.summary = summary
                    userCollectCategoryModel.save()
                    return json_result(message=u'成功修改收藏夹!')

                else:
                    return json_params_error(message=u'收藏夹名称不能为空!')
        else:
            return json_params_error(message=u'你尝试修改一个不存在的收藏夹!')
    else:
        return json_params_error(message=u'你尝试查看一个不存在的收藏夹!')


# 个人中心：删除个人收藏夹
@front_login_required
def delete_collect_category(request, collect_category_id=0):
    try:
        collectCategoryId = int(collect_category_id)
    except:
        pass

    if collectCategoryId:
        userCollectCategoryModel = UserCollectCategoryModel.objects.filter(author=request.front_user,
                                                                           pk=collectCategoryId).first()
        if userCollectCategoryModel:
            # 删除收藏夹的前提是先删除此收藏夹下存在的回答
            collectAnswerModel = CollectAnswerModel.objects.filter(username=request.front_user,
                                                                   collect_category=userCollectCategoryModel).all()
            if collectAnswerModel:
                collectAnswerModel.delete()
            userCollectCategoryModel.delete()
            return json_result(message=u'成功删除收藏夹!')
        else:
            return json_params_error(message=u'你尝试删除一个不存在的收藏夹!')
    else:
        return json_params_error(message=u'你尝试查看一个不存在的收藏夹!')


# 个人中心：我关注的问题
@front_login_required
def my_attention_questions(request, page=1):
    try:
        currentPage = int(page)
    except:
        pass

    numPage = int(configs.PC_FRONT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    attentionQuestionModel = AttentionQuestionModel.objects.filter(username=request.front_user).all().order_by('-pk')
    if attentionQuestionModel:

        questionCount = attentionQuestionModel.count()

        pageCount = questionCount / numPage

        if questionCount % numPage > 0:
            pageCount += 1

        attentionQuestionModel = list(attentionQuestionModel)[start:end]

        attention_questions = []
        for a in attentionQuestionModel:
            answerCount = AnswersModel.objects.filter(is_removed=0, questions=a.attention_question).count()
            attentionCount = AttentionQuestionModel.objects.filter(attention_question=a.attention_question).count()

            # 兼容微信上原有数据没有分类的问题
            if a.attention_question.category:
                questionCategory = a.attention_question.category.category
            else:
                questionCategory = None

            attention_questions.append({
                'id': a.attention_question.id,
                'question': a.attention_question.content,
                'question_category': questionCategory,
                'create_time': comment_time_period(a.attention_question.create_time),
                'answer_count': answerCount,
                'attention_count': attentionCount,
            })

        context = {
            'attention_questions': attention_questions,
            'current_page': currentPage,
            'page_count': pageCount
        }
        return json_result(data=context)
    else:
        return json_params_error(message=u'暂无关注的问题!')


# 个人中心: 关注问题和取消关注问题
@front_login_required
def attention_question(request, question_id=0):
    try:
        questionId = int(question_id)
    except:
        pass

    if questionId:
        questionModel = QuestionsModel.objects.filter(pk=questionId).first()
        if questionModel:
            attentionQuestionModel = AttentionQuestionModel.objects.filter(username=request.front_user,
                                                                           attention_question=questionModel).first()
            if attentionQuestionModel:
                attentionQuestionModel.delete()
                attentionCount = AttentionQuestionModel.objects.filter(attention_question=questionModel).count()
                context = {
                    'is_attention': 0,
                    'attention_count': attentionCount,
                }
                return json_result(message=u'取消关注成功!', data=context)
            else:
                attentionQuestionModel = AttentionQuestionModel(attention_question=questionModel,
                                                                username=request.front_user)
                attentionQuestionModel.save()
                attentionCount = AttentionQuestionModel.objects.filter(attention_question=questionModel).count()
                context = {
                    'is_attention': 1,
                    'attention_count': attentionCount,
                }
                return json_result(message=u'关注问题成功!', data=context)
        else:
            return json_params_error(message=u'你尝试查看一个不存在的问题!')
    else:
        return json_params_error(message=u'你尝试查看一个不存在的问题!')


# 个人中心：我的回答
@front_login_required
def my_answers(request, page=1):
    try:
        currentPage = int(page)
    except:
        pass

    myAnswersModel = AnswersModel.objects.filter(is_removed=0, author=request.front_user).all().order_by('-create_time')
    if myAnswersModel:
        tmp_answer = []
        for answer in myAnswersModel:

            # 如果当前回答所对应的问题没有删除，则展示，否则不显示
            if not answer.questions.is_removed:

                # 获取当前1级回答的点赞数
                praiseAnswerCount = PraiseAnswerModel.objects.filter(praise_answer=answer).count()

                # 如果当前用户已点赞，需要显示黄色小手
                isPraiseModel = PraiseAnswerModel.objects.filter(username=request.front_user,
                                                                 praise_answer=answer).first()
                if isPraiseModel:
                    is_praise = 1
                else:
                    is_praise = 0

                # 获取当前1级回答的收藏数
                collectAnswerCount = CollectAnswerModel.objects.filter(collect_answer=answer).count()
                # 如果当前用户收藏此回答,需要显示已收藏
                isCollectModel = CollectAnswerModel.objects.filter(username=request.front_user,
                                                                   collect_answer=answer).first()
                if isCollectModel:
                    is_collect = 1
                else:
                    is_collect = 0

                # 统计当前1级评论的2级评论总数
                childAnswersCount = AnswersModel.objects.filter(is_removed=0, relevance_answer=answer).count()

                tmp_answer.append({
                    'question_id': answer.questions.id,
                    'question_content': answer.questions.content,
                    'answer_user_id': answer.author.id,
                    'answer_user_username': answer.author.username,
                    'answer_user_avatar': answer.author.avatar,
                    'answer_comment': answer.comment,
                    'answer_create_time': comment_time_period(answer.create_time),
                    'child_answer_count': childAnswersCount,
                    'is_praise': is_praise,
                    'is_collect': is_collect,
                    'praise_count': praiseAnswerCount,
                    'collect_count': collectAnswerCount,
                    'answer_id': answer.id,
                })

        numPage = int(configs.PC_FRONT_COMMENT_NUM_PAGE)
        start = (currentPage - 1) * numPage
        end = start + numPage

        answerCount = myAnswersModel.count()

        pageCount = answerCount / numPage

        if answerCount % numPage > 0:
            pageCount += 1

        context = {
            'my_answers': tmp_answer[start:end],
            'current_page': currentPage,
            'page_count': pageCount,
        }
        return json_result(data=context)

    else:
        return json_params_error(message=u'你还没有回答过任何问题!')


# 个人中心: 我的收藏
@front_login_required
def my_collect(request, user_collect_category_id=0, page=1):
    try:
        userCollectCategoryId = int(user_collect_category_id)
        currentPage = int(page)
    except:
        pass

    model_type = configs.model_type

    numPage = int(configs.PC_FRONT_COMMENT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    userCollectCategoryModel = None
    if userCollectCategoryId:
        userCollectCategoryModel = UserCollectCategoryModel.objects.filter(pk=userCollectCategoryId,
                                                                           author=request.front_user).first()
        if not userCollectCategoryModel:
            return json_params_error(message=u'你尝试查看一个不存在的收藏分类!')

        collectAnswerModel = CollectAnswerModel.objects.filter(collect_category=userCollectCategoryModel,
                                                               username=request.front_user).all().order_by('-pk')
        # 新增的用户收藏夹。
        userFavoritesModel = UserFavoritesModel.objects.filter(username=request.front_user,
                                                               favorite_category=userCollectCategoryModel).order_by(
            '-create_time')
    else:
        collectAnswerModel = CollectAnswerModel.objects.filter(username=request.front_user).all().order_by('-pk')
        # 新增的用户收藏夹。
        userFavoritesModel = UserFavoritesModel.objects.filter(username=request.front_user).order_by('-create_time')

    # 收藏的回答
    tmp_answers = []
    if collectAnswerModel:
        for answer in collectAnswerModel:
            answerModel = AnswersModel.objects.filter(pk=answer.collect_answer.id).first()
            if answerModel:
                # 评论总数：计算的是当前评论的2级评论总数
                levelAnswerCount = AnswersModel.objects.filter(relevance_answer=answerModel).count()
                if levelAnswerCount:
                    answerCount = levelAnswerCount
                else:
                    answerCount = 0
                # 该回答被点赞总数
                praiseAnswerCount = PraiseAnswerModel.objects.filter(praise_answer=answerModel).count()
                if praiseAnswerCount:
                    praiseCount = praiseAnswerCount
                else:
                    praiseCount = 0

                isPraiseModel = PraiseAnswerModel.objects.filter(username=request.front_user,
                                                                 praise_answer=answerModel).first()
                if isPraiseModel:
                    is_praise = 1
                else:
                    is_praise = 0

                tmp_answers.append({
                    'question_id': answerModel.questions.id,
                    'question_content': answerModel.questions.content,
                    'answer_id': answerModel.id,
                    'answer_username': answerModel.author.username,
                    'answer_username_avatar': answerModel.author.avatar,
                    'answer_content': answerModel.comment,
                    'answer_create_time': comment_time_period(answerModel.create_time),
                    'answer_count': answerCount,
                    'praise_count': praiseCount,
                    'type': model_type['4'],
                    'create_time': answerModel.create_time,
                    'is_praise': is_praise,
                })

    # 收藏的视频、问答、文章等
    tmp_favorites = []
    if userFavoritesModel:
        for u in userFavoritesModel:
            tmp_favorites.append({
                'video_id': u.content_object.id,
                'title': u.content_object.title,
                'thumbnail': u.content_object.thumbnail,
                'is_collect': 1,
                'collect_category': u.favorite_category.id,
                'type': model_type['3'],
                'create_time': u.create_time,
            })

    tmp_favorites = tmp_answers + tmp_favorites

    tmp_favorites = sorted(tmp_favorites, key=lambda x: x['create_time'], reverse=True)

    favoritesCount = len(tmp_favorites)

    pageCount = favoritesCount / numPage
    if favoritesCount % numPage:
        pageCount += 1

    context = {
        'favorites': tmp_favorites[start:end],
        'page_count': pageCount,
        'current_page': currentPage
    }
    return json_result(data=context)


# 个人中心：我的提问
@front_login_required
def my_questions(request, page=1):
    try:
        currentPage = int(page)
    except:
        pass

    numPage = int(configs.PC_FRONT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    myQuestionsModel = QuestionsModel.objects.filter(is_removed=0, author=request.front_user).annotate(
        answer_count=Count('answersmodel'), attention_question_count=Count('attentionquestionmodel')).all().order_by(
        '-create_time')
    if myQuestionsModel:
        questionCount = myQuestionsModel.count()

        pageCount = questionCount / numPage
        if questionCount % numPage:
            pageCount += 1

        tmp_questions = []
        for question in myQuestionsModel:
            tmp_questions.append({
                'id': question.id,
                'content': question.content,
                'create_time': comment_time_period(question.create_time),
                'answer_count': question.answer_count,
                'attention_question_count': question.attention_question_count,
            })
        context = {
            'my_questions': tmp_questions[start:end],
            'current_page': currentPage,
            'page_count': pageCount,
        }
        return json_result(data=context)
    else:
        return json_params_error(message=u'你还没有发表过问题!')


# 个人中心：我的消息
@front_login_required
def my_messages(request, page=1):
    try:
        currentPage = int(page)
    except:
        pass

    numPage = int(configs.PC_FRONT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    myMessagesModel = MyMessagesModel.objects.filter(question__author=request.front_user).all()
    if myMessagesModel:
        messageCount = myMessagesModel.count()
        pageCount = messageCount / numPage
        if messageCount % numPage > 0:
            pageCount += 1

        pages = []

        # 先往前面找
        tmpPage = currentPage - 1
        while tmpPage >= 1:
            if tmpPage % 5 == 0:
                break
            else:
                pages.append(tmpPage)
                tmpPage -= 1
        # 再往后找
        tmpPage = currentPage
        while tmpPage <= pageCount:
            if tmpPage % 5 == 0:
                pages.append(tmpPage)
                break
            else:
                pages.append(tmpPage)
                tmpPage += 1
        pages.sort()

        message_list = []
        for m in myMessagesModel:
            message_list.append({
                'replay_name': m.replay_name.username,
                'replay_user_avatar': m.replay_name.avatar,
                'question': m.question.content,
                'question_id': m.question.id,
                'replay_answer': m.replay_answer.comment,
                'create_time': comment_time_period(m.create_time),
            })

        context = {
            'messages': message_list[start:end],
            'page_count': pageCount,
            'pages': pages,
            'current_page': currentPage,
        }
        return json_result(data=context)
    else:
        return json_params_error(message=u'暂无消息!')


# 我的消息通知列表
@front_login_required
def my_messages_info(request):
    myMessagesModel = MyMessagesModel.objects.filter(question__author=request.front_user, is_read=0).all()

    logger.info({'messages': myMessagesModel.values('question')})

    if myMessagesModel:
        messageCount = myMessagesModel.count()

        message_list = []
        for m in myMessagesModel:
            message_list.append({
                'replay_name': m.replay_name.username,
                'question': m.question.content,
                'question_id': m.question.id,
            })

        context = {
            'messages': message_list,
            'message_count': messageCount,
        }
        return json_result(data=context)
    else:
        context = {
            'messages': None,
            'message_count': 0,
        }
        return json_result(data=context)


# 一键清空我的消息列表
@front_login_required
def delete_my_messages_info(request):
    myMessagesModel = MyMessagesModel.objects.filter(question__author=request.front_user, is_read=0).all()

    logger.info({'messages': myMessagesModel.values('question')})

    if myMessagesModel:
        myMessagesModel.update(is_read=1)  # 将全部通知置为已读
        return json_result(message=u'成功清空消息!')
    else:
        return json_params_error(message=u'暂无消息!')


'''
	author: zhangx
	date: 20171208
	mark:
		1、研究方法3.0版本
'''


# 下载文章
@front_login_required
@front_user_infomation_is_full
def download_article(request, article_id=0, type_id=0, file_id=0):
    try:
        articleId = int(article_id)
        fileId = int(file_id)
    except:
        pass

    def file_iterator(file_name, chunk_size=2612000):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    typeId = type_id
    model_type = configs.model_type
    downLoadModel = None
    filePath = None

    if articleId:
        if model_type[typeId]:
            typeId = int(typeId)
            if typeId == 1:
                downLoadModel = MethodArticleInfoModel.objects.filter(pk=articleId, status__in=[1, 2]).first()
                filePath = u'article'
                if not downLoadModel:
                    return json_params_error(message=u'你尝试下载一篇不存在的资料!')
            if typeId == 3:
                videoModel = VideoModel.objects.filter(pk=article_id, status=1).first()
                if videoModel:
                    downLoadModel = VideoRelatedDataModel.objects.filter(pk=fileId, video=videoModel).first()
                    filePath = u'video'
                    if not downLoadModel:
                        return json_params_error(message=u'你尝试下载一节不存在的资料!')
        else:
            return json_params_error(message=u'你尝试下载一个绝密的资料!')

        if downLoadModel:
            if downLoadModel.file_name:
                fileName = downLoadModel.file_name
                filePath = os.path.join(settings.BASE_DIR, 'media/%s/%s').replace("\\", "/") % (filePath, fileName)
                response = StreamingHttpResponse(file_iterator(filePath))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fileName)
                return response
            else:
                return json_params_error(message=u'此文章没有附件!')
        else:
            return json_params_error(message=u'你尝试查看一篇不存在的文章!')
    else:
        return json_params_error(message=u'你尝试访问一个不存在的文章!')


# 研究方法分类列表、文章标题、视频标题
def method_category_and_article_title(request):
    # 先过滤出一级分类,去掉更多教程分类
    methodCategoryModel = MethodCategoryModel.objects.exclude(pk=13).filter(relevance_category__isnull=True,
                                                                            is_active=1).all()

    if methodCategoryModel:
        category_list = []
        for m_category in methodCategoryModel:

            # 查找一级分类下关联的2级分类
            relevanceMethodCategoryModel = MethodCategoryModel.objects.filter(relevance_category=m_category,
                                                                              is_active=1).all().order_by('rank',
                                                                                                          '-create_time')

            # 如果2级分类为真,则继续查找这个分类关联的所有文章
            # 返回2级分类列表
            relevance_category_list = []
            if relevanceMethodCategoryModel:
                for r_category in relevanceMethodCategoryModel:
                    # 若分类的type=1，则是文章。type=2，则是视频
                    article_and_video_list = []
                    if r_category.type == 1:
                        methodArticleInfoModel = MethodArticleInfoModel.objects.filter(category=r_category,
                                                                                       status__in=[1,
                                                                                                   2]).all().order_by(
                            'create_time')
                        if methodArticleInfoModel:
                            for m in methodArticleInfoModel:
                                article_and_video_list.append({
                                    'article_id': m.id,
                                    'article_category': m.category.category,
                                    'title': m.title,
                                    'rank': m.rank,
                                    'type': m.category.type,
                                })
                    else:
                        videoModel = VideoModel.objects.filter(course=r_category, status=1).all()
                        if videoModel:
                            for v in videoModel:
                                article_and_video_list.append({
                                    'video_id': v.id,
                                    'title': v.title,
                                    'type': v.course.type,
                                })
                    relevance_category_list.append({
                        'relevance_id': r_category.id,
                        'relevance_category': r_category.category,
                        'article_list': article_and_video_list,
                        'column': r_category.column,
                    })
            category_list.append({
                'category_id': m_category.id,
                'category': m_category.category,
                'relevance_category': relevance_category_list,
                'type': m_category.type,
            })

        # return json_result(data=category_list)
        return category_list
    else:
        return {}


# 研究方法文章详情
def method_article_detail(request, article_id=0):
    try:
        articleId = int(article_id)
    except:
        pass

    context = {}

    if articleId:
        methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=articleId, status__in=[1, 2]).first()

        if methodArticleInfoModel:

            # 阅读文章计数
            methodArticleInfoModel.read_count()

            currentCategory = methodArticleInfoModel.category.category

            if methodArticleInfoModel.category.relevance_category:
                parentCategory = methodArticleInfoModel.category.relevance_category.category
                category = u'<span>%s</span><span>%s</span>' % (parentCategory, currentCategory)
            else:
                if methodArticleInfoModel.category.id == 13:
                    category = u'<span>专题合集</span><span>更多教程</span>'
                else:
                    category = currentCategory

            # 查询当前文章的所有内容
            methodArticleContentModel = MethodArticleContentModel.objects.filter(
                article=methodArticleInfoModel).all().order_by('rank')
            content_list = []
            if methodArticleContentModel:
                for c in methodArticleContentModel:
                    content_list.append({
                        'section': c.section.section,
                        'content': c.content,
                        'is_login': c.is_login,
                    })

            context = {
                'id': methodArticleInfoModel.id,
                'title': methodArticleInfoModel.title,
                'category': category,
                'rank': methodArticleInfoModel.rank,
                'file_name': methodArticleInfoModel.file_name,
                'contents': content_list,
                'content_count': methodArticleContentModel.count()  # 这个版块总数用来在前台标记更多阅读版块的id
            }

            # #调用和当前文章关联的问答列表
            # ask_list = method_article_detail_ask_list(request,article_id=methodArticleInfoModel.id,ask_page=1)
            #
            # #由于此方法使用jsonResponse返回的格式，因此需要转换
            # str_json = json.loads(ask_list.content)
            #
            # if str_json['data']:
            # 	context['ask_list']= str_json['data']

            # 调用当前文章关联的更多阅读
            related_reading_articles = related_reading_method_article_list(request, methodArticleInfoModel.id)
            context['related_reading_articles'] = related_reading_articles

    # 调用研究方法公用的文章分类和标题
    category_list = method_category_and_article_title(request)
    context['category_list'] = category_list

    return context


# 研究方法文章详情
def front_method_article_detail(request, article_id=0):
    context = method_article_detail(request, article_id=article_id)
    return render(request, 'front_method_detail.html', context=context)


# 研究方法文章详情的问答列表
def method_article_detail_ask_list(request, article_id=0, ask_page=1):
    try:
        articleId = int(article_id)
        askCurrentPage = int(ask_page)
    except:
        pass

    if articleId:
        methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=articleId, status__in=[1, 2]).first()
        if methodArticleInfoModel:
            questionsModel = QuestionsModel.objects.filter(is_removed=0,
                                                           relevance_method_article=methodArticleInfoModel).all().order_by(
                '-create_time')
            if questionsModel:

                numPage = int(configs.PC_FRONT_COMMENT_NUM_PAGE)
                start = (askCurrentPage - 1) * numPage
                end = start + numPage

                questionCount = questionsModel.count()

                pageCount = questionCount / numPage
                if questionCount % numPage > 0:
                    pageCount += 1

                # 计算翻页
                pages = []

                # 先往前面找
                tmpPage = askCurrentPage - 1
                while tmpPage >= 1:
                    if tmpPage % 5 == 0:
                        break
                    else:
                        pages.append(tmpPage)
                        tmpPage -= 1
                # 再往后面找
                tmpPage = askCurrentPage
                while tmpPage <= pageCount:
                    if tmpPage % 5 == 0:
                        pages.append(tmpPage)
                        break
                    else:
                        pages.append(tmpPage)
                        tmpPage += 1
                pages.sort()

                questionsModel = list(questionsModel)[start:end]

                tmp_questions = []
                # 遍历过滤后的问题列表,如果当前问题有回复，则取出最后的回复信息，如果没有回复则取出问题信息
                for r in questionsModel:
                    # 获取当前问题的分类
                    if r.category:
                        category = r.category.category
                        categoryId = r.category.id
                    else:
                        category = None

                    # 获取当前问题的最新一条回复信息
                    lastAnswerModel = AnswersModel.objects.filter(is_removed=0, questions=r).last()
                    if lastAnswerModel:
                        # 获取当前问题回答总数
                        answersCount = AnswersModel.objects.filter(is_removed=0, questions=r).count()

                        tmp_questions.append({
                            'question_id': r.id,
                            'content': r.content,
                            'category': category,
                            'question_category_id': categoryId,
                            'recently_answer_user_id': lastAnswerModel.author.id,
                            'recently_answer_username': lastAnswerModel.author.username,
                            'recently_answer_time': comment_time_period(lastAnswerModel.create_time),
                            'answers_count': answersCount,
                        })
                    else:
                        # 当前问题没有没有回复
                        tmp_questions.append({
                            'question_id': r.id,
                            'content': r.content,
                            'category': category,
                            'question_category_id': categoryId,
                            'username': r.author.username,
                            'create_time': comment_time_period(r.create_time),
                            'answers_count': 0,
                        })

                context = {
                    'questions_list': tmp_questions,
                    'current_page': askCurrentPage,
                    'page_count': pageCount,
                    'pages': pages,
                    'index': 'method_article_detail_ask_list',  # 把当前的url返回供加载更多翻页使用
                }
                return json_result(data=context)
            else:
                return json_params_error(message=u'暂无问答信息!')
        else:
            return json_params_error(message=u'你尝试查看一篇没有问答的文章列表！')
    else:
        return json_params_error(message=u'你尝试访问一篇没有问答的文章列表!')


# 研究方法首页文章列表/分类文章列表
def method_articles(request, page=1, category_id=0):
    try:
        currentPage = int(page)
        categoryId = int(category_id)
    except:
        pass

    numPage = int(configs.PC_FRONT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    if categoryId:
        methodCategoryModel = MethodCategoryModel.objects.filter(pk=categoryId, is_active=1).first()
        if not methodCategoryModel:
            return json_params_error(message=u'你尝试查看一个不存在的分类下的文章!')

        '''
			由于要将N个模型数据汇总,因此不能使用order_by()方法对模型进行排序,
			所以，采用sorted()方法排序。
			需要在返回的字典中增加排序字段:
			1、sort_1: 第1个排序字段
			2、sort_2: 第2个排序字段

		'''
        methodArticleInfoModel = MethodArticleInfoModel.objects.filter(category=methodCategoryModel, status__in=[1, 2])
        videoModel = VideoModel.objects.filter(course=methodCategoryModel, status=1)

    else:
        methodArticleInfoModel = MethodArticleInfoModel.objects.filter(status__in=[1, 2])
        videoModel = VideoModel.objects.filter(status=1)

    # 研究方法文章和标题、摘要
    article_list = []
    if methodArticleInfoModel:
        for m in methodArticleInfoModel:
            # 这里返回文章的一级分类
            if m.category:
                if m.category.relevance_category:
                    category = m.category.relevance_category.category
                else:
                    category = m.category.category
            else:
                category = None

            article_list.append({
                'id': m.id,
                'title': m.title,
                'summary': m.summary,
                'thumbnail': m.thumbnail,
                'app_thumbnail': m.app_thumbnail,
                'create_time': comment_time_period(m.create_time),
                'sort_1': m.arrange,
                'sort_2': m.create_time,
                'category': category,
                'category_id': m.category.id,
                'type': configs.model_type['1'],
            })

    # 视频课程的标题和摘要
    video_list = []
    if videoModel:
        for v in videoModel:
            if v.course:
                if v.course.relevance_category:
                    category = v.course.relevance_category.category
                else:
                    category = v.course.category
            else:
                category = None

            video_list.append({
                'id': v.id,
                'title': v.title,
                'summary': v.summary,
                'thumbnail': v.thumbnail,
                'create_time': comment_time_period(v.create_time),
                'sort_1': None,
                'sort_2': v.create_time,
                'category': category,
                'category_id': v.course.id,
                'type': configs.model_type['3']
            })

    # 数据汇总
    tmp_info = article_list + video_list

    tmp_info = sorted(tmp_info, key=lambda x: (x['sort_1'], x['sort_2']), reverse=True)

    articleCount = len(tmp_info)

    pageCount = articleCount / numPage
    if articleCount % numPage > 0:
        pageCount += 1

    pages = []

    # 如果当前页码小于5,那么 pages将[1,2,3,4]填充进去
    # 如果当前页码大于5,那么 需要显示当前页码的左边2个，右边2个页码
    # 当页码为倒数第2页的时候,需要往前查找3页，往后查找1页
    # 如果当前页码是尾页，那么需要往前显示4个页码

    if currentPage < 5:
        tmpPage = currentPage - 1
        while tmpPage >= 1:
            if tmpPage % 5 == 0:
                break
            else:
                pages.append(tmpPage)
                tmpPage -= 1

        tmpPage = currentPage
        while tmpPage <= pageCount:
            if tmpPage % 5 == 0:
                pages.append(tmpPage)
                break
            else:
                pages.append(tmpPage)
                tmpPage += 1

    elif currentPage + 1 < pageCount:
        # 往前查找2次
        tmpPage = currentPage - 1
        t = 1
        while t < 3:
            if tmpPage > 1:
                pages.append(tmpPage)
                tmpPage -= 1
                t += 1
            else:
                break

        # 往后查找3次
        tmpPage = currentPage
        t = 1
        while t < 4:
            if tmpPage < pageCount:
                pages.append(tmpPage)
                tmpPage += 1
                t += 1
            else:
                pages.append(tmpPage)
                break

    elif currentPage + 1 == pageCount:
        # 这个判断用来解决当前页码为倒数第2页的时候,只显示4页的bug
        # 往前查找3次
        tmpPage = currentPage - 1
        t = 1
        while t < 4:
            if tmpPage > 1:
                pages.append(tmpPage)
                tmpPage -= 1
                t += 1
            else:
                break

        # 往后查找2次
        tmpPage = currentPage
        t = 1
        while t < 3:
            if tmpPage < pageCount:
                pages.append(tmpPage)
                tmpPage += 1
                t += 1
            else:
                pages.append(tmpPage)
                break
    else:
        tmpPage = currentPage
        t = 1
        # 往前查找5次
        while t < 6:
            pages.append(tmpPage)
            tmpPage -= 1
            t += 1

    pages.sort()

    context = {
        'articles': tmp_info[start:end],
        'pages': pages,
        'current_page': currentPage,
        'page_count': pageCount,
    }

    # 用于webapp调用
    if request.is_ajax():
        return json_result(data=context)

    # 调用研究方法分类和标题方法
    category_list = method_category_and_article_title(request)
    context['category_list'] = category_list

    # 调用banner列表方法
    banner = method_banner_list(request)
    context['banner'] = banner

    # banner个数是否多于一个
    is_banner_more_than_one = len(banner) > 1
    context['is_banner_more_than_one'] = is_banner_more_than_one

    # 调用专题列表
    topic_list = method_topic_list(request)
    context['topic_list'] = topic_list

    return render(request, 'front_methods.html', context=context)


# banner图列表
def method_banner_list(request):
    bannerModel = BannerModel.objects.filter(is_active=1, type=1).order_by('rank').values('id', 'name',
                                                                                          'link').order_by('rank')

    return list(bannerModel)


# 相关阅读文章列表
def related_reading_method_article_list(request, article_id=0):
    try:
        articleId = int(article_id)
    except:
        pass

    tmp_related_articles_list = []

    if articleId:
        # 这里展示已发布、已推荐的文章关联的相关阅读文章
        methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=articleId, status__in=[1, 2]).first()
        if methodArticleInfoModel:
            # 判断当前文章是否有关联的相关阅读文章
            methodArticleRelatedReadingModel = MethodArticleRelatedReadingModel.objects.filter(
                relevance_article=methodArticleInfoModel).all().order_by('arrange')
            if methodArticleRelatedReadingModel:

                for m in methodArticleRelatedReadingModel:
                    # 获取文章分类的父级分类,用于拼接标题。如果分类id==13，则不显示
                    parent_category = None
                    if m.related_reading_article.category:
                        if m.related_reading_article.category.relevance_category:
                            if m.related_reading_article.category.relevance_category.id != 13:
                                parent_category = m.related_reading_article.category.relevance_category.category
                        else:
                            if m.related_reading_article.category.id != 13:
                                parent_category = m.related_reading_article.category.category

                    tmp_related_articles_list.append({
                        'id': m.related_reading_article.id,
                        'title': m.related_reading_article.title,
                        'thumbnail': m.related_reading_article.thumbnail,
                        'summary': m.related_reading_article.summary,
                        'category_id': m.related_reading_article.category.id,
                        'parent_category': parent_category,
                        'create_time': comment_time_period(m.related_reading_article.create_time)
                    })
    if request.is_ajax():
        return json_result(data=tmp_related_articles_list)
    return tmp_related_articles_list


'''
	author:zhangx
	date:20180124
	mark:
		1、新增研究方法专题

'''


# 研究方法专题列表
def method_topic_list(request):
    methodArticleTopicModel = MethodArticleTopicModel.objects.filter(status=2).values('id', 'title', 'summary',
                                                                                      'thumbnail').order_by('arrange')

    if request.is_ajax():
        return json_result(data={'topic_list': list(methodArticleTopicModel)})
    return list(methodArticleTopicModel)


# 所有专题文章列表
def method_topic(request, page=1):
    '''
		所有专题文章列表读取的是分类id=13的文章
	'''
    try:
        currentPage = int(page)
    except:
        pass

    numPage = int(configs.PC_FRONT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    context = {}

    topicRelatedMethodArticleModel = MethodArticleInfoModel.objects.filter(category__id=13, status__in=[1, 2]).all()

    if topicRelatedMethodArticleModel:
        articleCount = topicRelatedMethodArticleModel.count()

        pageCount = articleCount / numPage
        if articleCount % numPage > 0:
            pageCount += 1

        pages = []

        if currentPage < 5:
            tmpPage = currentPage - 1
            while tmpPage >= 1:
                if tmpPage % 5 == 0:
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage -= 1

            tmpPage = currentPage
            while tmpPage <= pageCount:
                if tmpPage % 5 == 0:
                    pages.append(tmpPage)
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage += 1

        elif currentPage + 1 < pageCount:
            # 往前查找2次
            tmpPage = currentPage - 1
            t = 1
            while t < 3:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找3次
            tmpPage = currentPage
            t = 1
            while t < 4:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break

        elif currentPage + 1 == pageCount:
            # 这个判断用来解决当前页码为倒数第2页的时候,只显示4页的bug
            # 往前查找3次
            tmpPage = currentPage - 1
            t = 1
            while t < 4:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找2次
            tmpPage = currentPage
            t = 1
            while t < 3:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break
        else:
            tmpPage = currentPage
            t = 1
            # 往前查找5次
            while t < 6:
                pages.append(tmpPage)
                tmpPage -= 1
                t += 1

        pages.sort()

        topicRelatedMethodArticleModel = topicRelatedMethodArticleModel[start:end]

        topic_article_list = []
        for t in topicRelatedMethodArticleModel:
            topic_article_list.append({
                'id': t.id,
                'title': t.title,
                'category': t.category.category,
                'arrange': t.arrange,
                'summary': t.summary,
                'create_time': comment_time_period(t.create_time),
                'thumbnail': t.thumbnail,
            })

        context['topic_article_list'] = topic_article_list
        context['pages'] = pages
    context['current_page'] = currentPage

    if request.is_ajax():
        return json_result(data=context)

    return render(request, 'front_method_topic.html', context=context)


# 专题详情
def method_topic_detail(request, topic_id=0, page=1):
    try:
        topicId = int(topic_id)
        currentPage = int(page)
    except:
        pass

    numPage = int(configs.PC_FRONT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    context = {}

    if topicId:
        methodArticleTopicModel = MethodArticleTopicModel.objects.filter(pk=topicId, status=2).first()
        if methodArticleTopicModel:

            # 统计专题访问数
            methodArticleTopicModel.read_count()

            topicRelatedMethodArticleModel = TopicRelatedMethodArticleModel.objects.filter(
                topic=methodArticleTopicModel).order_by('arrange')

            context = {
                'id': methodArticleTopicModel.id,
                'title': methodArticleTopicModel.title,
                'summary': methodArticleTopicModel.summary,
                'thumbnail': methodArticleTopicModel.thumbnail,
                'app_thumbnail': methodArticleTopicModel.app_thumbnail,
            }
        else:
            return json_params_error(message=u'你尝试查看一个不存在的专题文章列表!')
    else:
        return json_params_error(message=u'你尝试访问一个不存在的专题文章列表!')

    if topicRelatedMethodArticleModel:
        articleCount = topicRelatedMethodArticleModel.count()

        pageCount = articleCount / numPage
        if articleCount % numPage > 0:
            pageCount += 1

        pages = []

        if currentPage < 5:
            tmpPage = currentPage - 1
            while tmpPage >= 1:
                if tmpPage % 5 == 0:
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage -= 1

            tmpPage = currentPage
            while tmpPage <= pageCount:
                if tmpPage % 5 == 0:
                    pages.append(tmpPage)
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage += 1

        elif currentPage + 1 < pageCount:
            # 往前查找2次
            tmpPage = currentPage - 1
            t = 1
            while t < 3:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找3次
            tmpPage = currentPage
            t = 1
            while t < 4:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break

        elif currentPage + 1 == pageCount:
            # 这个判断用来解决当前页码为倒数第2页的时候,只显示4页的bug
            # 往前查找3次
            tmpPage = currentPage - 1
            t = 1
            while t < 4:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找2次
            tmpPage = currentPage
            t = 1
            while t < 3:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break
        else:
            tmpPage = currentPage
            t = 1
            # 往前查找5次
            while t < 6:
                pages.append(tmpPage)
                tmpPage -= 1
                t += 1

        pages.sort()

        topicRelatedMethodArticleModel = topicRelatedMethodArticleModel[start:end]

        topic_article_list = []
        for t in topicRelatedMethodArticleModel:
            topic_article_list.append({
                'id': t.article.id,
                'title': t.article.title,
                'category': t.article.category.category,
                'category_id': t.article.category.id,
                'arrange': t.arrange,
                'summary': t.article.summary,
                'create_time': comment_time_period(t.article.create_time),
                'thumbnail': t.article.thumbnail,
                'app_thumbnail': t.article.app_thumbnail,
            })

        context['topic_article_list'] = topic_article_list
        context['pages'] = pages
    context['current_page'] = currentPage

    if request.is_ajax():
        return json_result(data=context)

    return render(request, 'front_method_topic_detail.html', context=context)


# 专题文章详情
def method_topic_article_detail(request, article_id=0):
    context = method_article_detail(request, article_id=article_id)

    return render(request, 'front_method_topic_article_detail.html', context=context)


'''
	author: zhangx
	date: 20180314
	mark:
		新增提问关键词检索功能(主要检索研究方法文章)

'''


@require_http_methods(['GET', 'POST'])
def search_key_word(request):
    if request.method == 'GET':
        return json_result(message=u'关键词搜索页面!')
    else:
        searchKeyWord = request.POST.get('search_key_word', None)

        if searchKeyWord:

            # 遍历数据库所有关键词,返回匹配的关键词分组
            keyWordModel = KeyWordModel.objects.all()

            tmpKeyWordGroups = []
            for k in keyWordModel:
                if re.search(k.key_word, searchKeyWord, flags=re.I):
                    # 判断符合的分组模型在临时列表中是否存在,若不存在则保存
                    if k.group_name not in tmpKeyWordGroups:
                        tmpKeyWordGroups.append(k.group_name)

            articleList = []
            for k in tmpKeyWordGroups:
                keyWordRelevanceArticleModel = KeyWordRelevanceArticleModel.objects.filter(group_name=k).all()
                for a in keyWordRelevanceArticleModel:
                    if a.type == 1:
                        methodArticleInfoModel = MethodArticleInfoModel.objects.filter(status__in=[1, 2],
                                                                                       pk=a.article).first()
                        if methodArticleInfoModel:
                            # 这里需要区分下文章所属的分类，如果category=13，则属于更多教程，跳转的详情页面不一样
                            if methodArticleInfoModel.category:
                                category = methodArticleInfoModel.category.category
                                categoryId = methodArticleInfoModel.category.id
                            else:
                                category = None
                                categoryId = None

                            articleList.append({
                                'id': methodArticleInfoModel.id,
                                'title': methodArticleInfoModel.title,
                                'rank': methodArticleInfoModel.rank,
                                'category': category,
                                'category_id': categoryId,
                                'type': a.type,
                                'create_time': methodArticleInfoModel.create_time,
                            })
                    else:
                        methodArticleTopicModel = MethodArticleTopicModel.objects.filter(status__in=[2],
                                                                                         pk=a.article).first()
                        articleList.append({
                            'id': methodArticleTopicModel.id,
                            'title': methodArticleTopicModel.title,
                            'rank': 0,
                            'type': a.type,
                            'create_time': methodArticleTopicModel.create_time,
                        })

            articles = sorted(articleList, key=lambda x: x['create_time'], reverse=True)
            context = {
                'articles': articles,
            }
            return json_result(data=context)
        else:
            return json_params_error(message=u'关键词不能为空!')


# 提问页面渲染
@front_login_required
def ask_question(request):
    return render(request, 'front_ask_question.html')


'''
	author: zhangx
	date: 20180224
	mark:
		研究进展接口

'''


# 研究进展-热门推荐列表
def hold_news(request, type_id=0):
    try:
        typeId = int(type_id)
    except:
        pass

    if typeId in [1, 2]:
        holdNewsModel = HoldNewsModel.objects.filter(type=typeId).all()[0:6]
    else:
        holdNewsModel = HoldNewsModel.objects.all()[0:6]

    if holdNewsModel:
        hold_news_list = []
        for h in holdNewsModel:
            hold_news_list.append({
                'id': h.news.id,
                'title': h.news.title,
                'thumbnail': h.news.thumbnail,
                'summary': h.news.summary,
                'create_time': comment_time_period(h.news.create_time),
                'type': h.type,
            })

        context = {
            'hold_news': hold_news_list,
        }

        return json_result(data=context)


# 研究进展-新闻分类列表
def news_category_list(request):
    newsCategoryListModel = NewsCategoryModel.objects.all().values('id', 'category', 'create_time')

    context = {
        'news_category_list': list(newsCategoryListModel)
    }
    return context


# 研究进展-新闻列表
def news(request, page=1, category_id=0):
    try:
        currentPage = int(page)
        categoryId = int(category_id)
    except:
        pass

    numPage = int(configs.PC_FRONT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    if categoryId:
        newsCategoryModel = NewsCategoryModel.objects.filter(pk=categoryId).first()
        if newsCategoryModel:
            newsModel = NewsModel.objects.filter(status__in=[1, 2], category=newsCategoryModel).all()
        else:
            newsModel = NewsModel.objects.filter(status__in=[1, 2]).all()
    else:
        newsModel = NewsModel.objects.filter(status__in=[1, 2]).all()

    news_list = []
    if newsModel:

        newsCount = newsModel.count()

        pageCount = newsCount / numPage
        if newsCount % numPage > 0:
            pageCount += 1

        pages = []

        if currentPage < 5:
            tmpPage = currentPage - 1
            while tmpPage >= 1:
                if tmpPage % 5 == 0:
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage -= 1

            tmpPage = currentPage
            while tmpPage <= pageCount:
                if tmpPage % 5 == 0:
                    pages.append(tmpPage)
                    break
                else:
                    pages.append(tmpPage)
                    tmpPage += 1

        elif currentPage + 1 < pageCount:
            # 往前查找2次
            tmpPage = currentPage - 1
            t = 1
            while t < 3:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找3次
            tmpPage = currentPage
            t = 1
            while t < 4:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break

        elif currentPage + 1 == pageCount:
            # 这个判断用来解决当前页码为倒数第2页的时候,只显示4页的bug
            # 往前查找3次
            tmpPage = currentPage - 1
            t = 1
            while t < 4:
                if tmpPage > 1:
                    pages.append(tmpPage)
                    tmpPage -= 1
                    t += 1
                else:
                    break

            # 往后查找2次
            tmpPage = currentPage
            t = 1
            while t < 3:
                if tmpPage < pageCount:
                    pages.append(tmpPage)
                    tmpPage += 1
                    t += 1
                else:
                    pages.append(tmpPage)
                    break
        else:
            tmpPage = currentPage
            t = 1
            # 往前查找5次
            while t < 6:
                pages.append(tmpPage)
                tmpPage -= 1
                t += 1

        pages.sort()

        newsModel = list(newsModel)[start:end]
        for n in newsModel:
            if n.category:
                category = n.category.category
            else:
                category = None
            news_list.append({
                'id': n.id,
                'title': n.title,
                'summary': n.summary,
                'thumbnail': n.thumbnail,
                'app_thumbnail': n.app_thumbnail,
                'category': category,
                'create_time': comment_time_period(n.create_time),
            })

        context = {
            'current_page': currentPage,
            'page_count': pageCount,
            'news': news_list,
            'pages': pages,
            'category_id': categoryId,
        }

        # 合并热门推荐,新闻分类列表的数据
        dictMerged1 = context.copy()
        dictMerged1.update(news_category_list(request))

        if request.is_ajax():
            return json_result(data=dictMerged1)
        return render(request, 'front_news.html', context=dictMerged1)
    else:
        context = news_category_list(request)

        if request.is_ajax():
            return json_result(data=context)

        return render(request, 'front_news.html', context=context)


# 研究进展-新闻详情
def news_detail(request, news_id=0, page=1):
    try:
        newsId = int(news_id)
        currentPage = int(page)
    except:
        pass

    numPage = int(configs.PC_FRONT_COMMENT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    if newsId:
        newsModel = NewsModel.objects.filter(pk=newsId, status__in=[1, 2]).first()

        if newsModel:
            newsCommentModel = NewsCommentModel.objects.filter(news=newsModel, status=1).all()
            comments = []
            if newsCommentModel:

                commentCount = newsCommentModel.count()
                pageCount = commentCount / numPage
                if commentCount % numPage > 0:
                    pageCount += 1

                pages = []

                if currentPage < 5:
                    tmpPage = currentPage - 1
                    while tmpPage >= 1:
                        if tmpPage % 5 == 0:
                            break
                        else:
                            pages.append(tmpPage)
                            tmpPage -= 1

                    tmpPage = currentPage
                    while tmpPage <= pageCount:
                        if tmpPage % 5 == 0:
                            pages.append(tmpPage)
                            break
                        else:
                            pages.append(tmpPage)
                            tmpPage += 1

                elif currentPage + 1 < pageCount:
                    # 往前查找2次
                    tmpPage = currentPage - 1
                    t = 1
                    while t < 3:
                        if tmpPage > 1:
                            pages.append(tmpPage)
                            tmpPage -= 1
                            t += 1
                        else:
                            break

                    # 往后查找3次
                    tmpPage = currentPage
                    t = 1
                    while t < 4:
                        if tmpPage < pageCount:
                            pages.append(tmpPage)
                            tmpPage += 1
                            t += 1
                        else:
                            pages.append(tmpPage)
                            break

                elif currentPage + 1 == pageCount:
                    # 这个判断用来解决当前页码为倒数第2页的时候,只显示4页的bug
                    # 往前查找3次
                    tmpPage = currentPage - 1
                    t = 1
                    while t < 4:
                        if tmpPage > 1:
                            pages.append(tmpPage)
                            tmpPage -= 1
                            t += 1
                        else:
                            break

                    # 往后查找2次
                    tmpPage = currentPage
                    t = 1
                    while t < 3:
                        if tmpPage < pageCount:
                            pages.append(tmpPage)
                            tmpPage += 1
                            t += 1
                        else:
                            pages.append(tmpPage)
                            break
                else:
                    tmpPage = currentPage
                    t = 1
                    # 往前查找5次
                    while t < 6:
                        pages.append(tmpPage)
                        tmpPage -= 1
                        t += 1

                pages.sort()

                newsCommentModel = list(newsCommentModel)[start:end]

                for c in newsCommentModel:
                    comments.append({
                        'id': c.id,
                        'author': c.author.username,
                        'avatar': c.author.avatar,
                        'comment': c.comment,
                        'create_time': comment_time_period(c.create_time),
                    })

                context = {
                    'id': newsModel.id,
                    'title': newsModel.title,
                    'create_time': comment_time_period(newsModel.create_time),
                    'content': newsModel.content,
                    'file_name': newsModel.file_name,
                    'current_page': currentPage,
                    'comments': comments,
                    'comment_count': commentCount,
                    'pages': pages,
                }

                if request.is_ajax():
                    return json_result(data=context)

                return render(request, 'front_news_detail.html', context=context)
            else:
                context = {
                    'id': newsModel.id,
                    'title': newsModel.title,
                    'create_time': comment_time_period(newsModel.create_time),
                    'content': newsModel.content,
                    'file_name': newsModel.file_name,
                    'current_page': currentPage,
                    'pages': 0,
                    'comments': None,
                    'comment_count': 0,
                }

                if request.is_ajax():
                    return json_result(data=context)

                return render(request, 'front_news_detail.html', context=context)
        else:
            return json_params_error(message=u'你尝试访问一篇不存在的新闻!')
    else:
        return json_params_error(message=u'你尝试查看一篇不存在的新闻!')


# 研究进展-相关阅读新闻列表
def news_related_reading_list(request, news_id=0):
    try:
        newsId = int(news_id)
    except:
        pass

    if newsId:
        newsModel = NewsModel.objects.filter(pk=newsId, status__in=[1, 2]).first()
        if newsModel:
            newsRelatedReadingModel = NewsRelatedReadingModel.objects.filter(related_news=newsModel).all()
            # 根据type值来区分是研究方法文章还是研究进展文章
            if newsRelatedReadingModel:
                related_reading_list = []
                for r in newsRelatedReadingModel:
                    if r.type == 1:
                        methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=r.related_reading_article,
                                                                                       status__in=[1, 2]).first()
                        if methodArticleInfoModel:
                            related_reading_list.append({
                                'id': methodArticleInfoModel.id,
                                'title': methodArticleInfoModel.title,
                                'create_time': comment_time_period(methodArticleInfoModel.create_time),
                                'type': 1,
                            })
                    else:
                        newsModel = NewsModel.objects.filter(pk=r.related_reading_article, status__in=[1, 2]).first()
                        if newsModel:
                            related_reading_list.append({
                                'id': newsModel.id,
                                'title': newsModel.title,
                                'create_time': comment_time_period(newsModel.create_time),
                                'type': 2,
                            })
                # 给相关阅读文章列表按照文章时间排序
                articles = sorted(related_reading_list, key=lambda x: (x['create_time']), reverse=True)

                return json_result(data=articles)
            else:
                return json_params_error(message=u'暂无相关新闻!')
        else:
            return json_params_error(message=u'你尝试查看一篇不存在的新闻!')
    else:
        return json_params_error(message=u'你尝试访问一篇不存在的新闻!')


# 研究进展-添加评论
@front_login_required
@require_http_methods(['GET', 'POST'])
def add_news_comment(request, news_id=0):
    if request.method == 'POST':
        comment = request.POST.get('comment', None)

        try:
            newsId = int(news_id)
            comment = str(comment).strip()
        except:
            pass

        if newsId:
            newsModel = NewsModel.objects.filter(pk=newsId, status__in=[1, 2]).first()
            if newsModel:
                if comment:
                    newsCommentModel = NewsCommentModel(news=newsModel, author=request.front_user, comment=comment)
                    newsCommentModel.save()
                    return json_result(message=u'添加评论成功!')
                else:
                    return json_params_error(message=u'评论内容不能为空!')
            else:
                return json_params_error(message=u'你尝试查看一篇不存在的新闻!')
        else:
            return json_params_error(message=u'你尝试访问一篇不存在的新闻!')


# 下载文章
@front_login_required
@front_user_infomation_is_full
def download_news(request, news_id=0):
    try:
        newsId = int(news_id)
    except:
        pass

    def file_iterator(file_name, chunk_size=2612000):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    if newsId:
        newsModel = NewsModel.objects.filter(pk=newsId).first()
        if newsModel:

            if newsModel.file_name:
                fileName = newsModel.file_name
                filePath = os.path.join(settings.BASE_DIR, 'media/article/%s').replace("\\", "/") % fileName
                response = StreamingHttpResponse(file_iterator(filePath))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fileName)
                return response
            else:
                return json_params_error(message=u'此新闻没有附件!')
        else:
            return json_params_error(message=u'你尝试查看一篇不存在的新闻!')
    else:
        return json_params_error(message=u'你尝试访问一个不存在的新闻!')


'''
	author:zhangx
	date:20180425
	mark:
		1、视频需求

'''


def video_validate(request):
    return polyv_validate(request)


# 视频课程详情
def video_detail(request, video_id=0):
    try:
        videoId = int(video_id)
    except:
        pass

    if videoId:
        videoModel = VideoModel.objects.filter(pk=videoId, status=1).first()
        if videoModel:
            # 关联的课程目录
            courseSection = course_section(request, video_id=videoId)

            # 关联的讲者简介
            courseModel = CourseModel.objects.filter(course=videoModel.course.relevance_category).first()
            if courseModel:
                teachIntro = courseModel.teach_intro
                courseThumbnail = courseModel.thumbnail

            # 关联的附件
            videoRelatedDataModel = VideoRelatedDataModel.objects.filter(video=videoModel).all()
            videoDataList = []
            if videoRelatedDataModel:
                for v in videoRelatedDataModel:
                    videoDataList.append({
                        'file_id': v.id,
                        'file_name': v.file_name,
                    })

            # 一组视频的价格
            price = None
            priceModel = CourseModel.objects.filter(course=videoModel.course.relevance_category).first()
            if priceModel:
                price = priceModel.price

            # 是否收藏
            isCollect = 0
            collectCategoryId = 0
            if hasattr(request, 'front_user'):
                userFavoritesModel = UserFavoritesModel.objects.filter(username=request.front_user).all()
                if userFavoritesModel:
                    for u in userFavoritesModel:
                        if videoModel == u.content_object:
                            isCollect = 1
                            # 判断是否属于某个分类
                            if u.favorite_category:
                                collectCategoryId = u.favorite_category.id

            # 是否已购买
            isBuy = 0
            if hasattr(request, 'front_user'):
                isOrderModel = UserBuyOrderModel.objects.filter(username=request.front_user, status=2).all()
                for i in isOrderModel:
                    if i.content_object == videoModel.course.relevance_category:
                        isBuy = 1

            context = {
                'video_id': videoModel.id,
                'title': videoModel.title,
                'code': videoModel.polyv_vid,
                'course': videoModel.course.category,
                'course_id': videoModel.course.id,
                'course_main': videoModel.course_main,
                'video_time': videoModel.video_time,
                'course_section': courseSection,
                'teach_intro': teachIntro,
                'video_related_data': videoDataList,
                'price': price,
                'is_collect': isCollect,
                'collect_category_id': collectCategoryId,
                'is_pay': videoModel.is_pay,
                'is_buy': isBuy,
                'course_thumbnail': courseThumbnail,
            }

            if request.is_ajax():
                return json_result(data=context)

            return render(request, 'video_detail.html', context=context)
        else:
            return render(request, 'video_detail.html', context={'message': u'你尝试查看一个不存在的视频!'})
    else:
        return render(request, 'video_detail.html', context={'message': u'你尝试访问一个不存在的视频!'})


# 课程目录
def course_section(request, video_id=0):
    try:
        videoId = int(video_id)
    except:
        pass
    # 列出视频详情页中视频关联的课程目录

    if videoId:
        videoModel = VideoModel.objects.filter(pk=videoId, status=1).first()
        if videoModel:
            # 找出此视频章节所属哪个课程
            parentCourseModel = videoModel.course.relevance_category
            if parentCourseModel:
                courseSectionModel = MethodCategoryModel.objects.filter(relevance_category=parentCourseModel,
                                                                        is_active=1).all()
                # 如果课程章节存在,则查找其关联的视频
                if courseSectionModel:
                    course_list = []
                    for c in courseSectionModel:
                        videoModel = VideoModel.objects.filter(course=c, status=1).all()
                        video_list = []
                        for v in videoModel:
                            video_list.append({
                                'video_id': v.id,
                                'video_time': v.video_time,
                                'title': v.title,
                                'is_pay': v.is_pay,
                            })
                        course_list.append({
                            'course': c.category,
                            'course_id': c.id,
                            'video_list': video_list,
                        })
                    return course_list
                else:
                    return {'message': u'此课程还在完善中!'}
            else:
                return {'message': u'此视频还未分类!'}
        else:
            return {'message': u'你尝试查看一个不存在的视频!'}
    else:
        return {'message': u'你尝试访问一个不存在的视频!'}


# 视频评论列表
def video_comment(request, video_id=0, page=1):
    try:
        videoId = int(video_id)
        currentPage = int(page)
    except:
        pass

    numPage = int(configs.PC_FRONT_COMMENT_NUM_PAGE)
    start = (currentPage - 1) * numPage
    end = start + numPage

    if videoId:
        videoModel = VideoModel.objects.filter(pk=videoId, status=1).first()
        if videoModel:
            parentVideoCommentModel = VideoCommentModel.objects.filter(video=videoModel,
                                                                       relevance_comment__isnull=True).all()
            parentVideoCommentCount = parentVideoCommentModel.count()
            pageCount = parentVideoCommentCount / numPage
            if parentVideoCommentCount % numPage > 0:
                pageCount += 1

            if parentVideoCommentModel:
                comment_list = []
                for p in parentVideoCommentModel:

                    # 判断对当前评论是否点赞
                    isPraise = 0
                    if hasattr(request, 'front_user'):
                        userPraiseModel = UserPraiseModel.objects.filter(username=request.front_user)
                        if userPraiseModel:
                            for u in userPraiseModel:
                                if p == u.content_object:
                                    isPraise = 1

                    relevance_comment = []
                    childVideoCommentModel = VideoCommentModel.objects.filter(video=videoModel,
                                                                              relevance_comment=p).all()
                    if childVideoCommentModel:
                        for c in childVideoCommentModel:
                            relevance_comment.append({
                                'id': c.id,
                                'username': c.username.username,
                                'comment': c.comment,
                            })
                    comment_list.append({
                        'id': p.id,
                        'username': p.username.username,
                        'avatar': p.username.avatar,
                        'comment': p.comment,
                        'create_time': comment_time_period(p.create_time),
                        'relevance_comment': relevance_comment,
                        'praise_count': p.user_praise.count(),
                        'is_praise': isPraise,
                    })
                context = {
                    'current_page': currentPage,
                    'page_count': pageCount,
                    'comment_list': comment_list[start:end],
                }

                return json_result(data=context)
            else:
                return json_params_error(message=u'暂无评论!')
        else:
            return json_params_error(message=u'你尝试查看一个不存在的视频评论!')
    else:
        return json_params_error(message=u'你尝试访问一个不存在的视频!')


# 添加视频评论
@front_login_required
@require_http_methods(['GET', 'POST'])
def add_video_comment(request):
    if request.method == 'GET':
        return json_result(message=u'添加视频评论页面!')
    else:
        videoId = request.POST.get('video_id', None)
        comment = request.POST.get('comment', None)
        relevanceCommentId = request.POST.get('relevance_comment_id', None)

        try:
            comment = str(comment).strip().replace("<", " ")
        except:
            pass

        if not videoId:
            return json_params_error(message=u'你尝试评论一个不存在的视频!')

        videoModel = VideoModel.objects.filter(pk=videoId, status=1).first()
        if not videoModel:
            return json_params_error(message=u'你尝试评论一个不存在的视频!')

        if comment:
            if relevanceCommentId:
                relevanceCommentModel = VideoCommentModel.objects.filter(pk=relevanceCommentId).first()
                if relevanceCommentModel:
                    # 要判断关联的评论是不是一级评论
                    if relevanceCommentModel.relevance_comment:
                        return json_params_error(message=u'暂时不能回复2级评论!')
                    else:
                        videoCommentModel = VideoCommentModel(username=request.front_user, video=videoModel,
                                                              comment=comment, relevance_comment=relevanceCommentModel)
                else:
                    return json_params_error(message=u'你尝试回复一个不存在的评论!')
            else:
                videoCommentModel = VideoCommentModel(username=request.front_user, video=videoModel, comment=comment)

            videoCommentModel.save()
            return json_result(message=u'发表评论成功!')
        else:
            return json_params_error(message=u'请填写评论内容!')


# 收藏方法/取消收藏(可收藏视频、研究方法，研究进展等一切)
@front_login_required
def front_favorites(request, id=0, collect_category_id=0, type_id=0):
    return favorites(request, id=id, collect_category_id=collect_category_id, type_id=type_id)


# 用户点赞
@front_login_required
def front_user_praise(request, id=0, type_id=0):
    return user_praise(request, id=id, type_id=type_id)


'''
	author:zhangx
	data:20180530
	mark:
		1、视频支付
		2、调用支付宝付款
'''


# 创建订单
@front_login_required
def create_orders(request, order_id=0):
    '''
		这个方法有两个作用：
		1、创建订单
		2、从个人中心进入已创建未付款的订单进行支付
	'''
    # try:
    # 	orderId = int(order_id)
    # except:pass

    # 声明订单id,创建时间
    orderId = 0
    orderTime = 0

    if request.method == 'GET':
        if order_id:
            # 表示从个人中心进入的未支付订单，进行校验
            orderModel = UserBuyOrderModel.objects.filter(username=request.front_user, order_id=order_id,
                                                          status=1).first()
            if not orderModel:
                return json_params_error(message=u'你的订单不存在/已失效!')
            else:
                orderId = orderModel.order_id
                orderTime = orderModel.create_time
        else:
            return json_params_error(message=u'你尝试查看一个不存在的订单!')
    else:
        goodsId = request.POST.get('goods_id', None)

        try:
            goodsId = int(goodsId)
        except:
            pass
        # 获取商品信息
        if not goodsId:
            return json_params_error(message=u'你尝试查看一个不存在的课程!')

        price = 0
        categoryModel = None
        videoModel = VideoModel.objects.filter(status=1, pk=goodsId).first()
        if not videoModel:
            return json_params_error(message=u'你尝试访问一个不存在的视频课程!')

        # 查询全套视频课程的价格
        if videoModel.course:
            categoryModel = videoModel.course.relevance_category
            # 获取全套视频价格
            priceModel = CourseModel.objects.filter(course=categoryModel).first()
            if priceModel:
                price = priceModel.price
            else:
                return json_params_error(message=u'这套视频已跳出三界之外!')
        else:
            return json_params_error(message=u'这视频没有设置价格!')

        # 初始化订单编号

        localTime = time.strftime('%Y%m%d%H%M%S', time.localtime())
        tradeNo = localTime + str(request.front_user.id)

        repeatTradeNo = UserBuyOrderModel.objects.filter(order_id=tradeNo).first()
        if repeatTradeNo:
            return json_params_error(message=u'你在刷单?')

        else:
            # 若用户已经创建此视频的购买订单且未支付，就需要把这个订单号返回
            repeatOrderModel = UserBuyOrderModel.objects.filter(username=request.front_user, status=1).all()

            if repeatOrderModel:
                tmp_model = []

                for r in repeatOrderModel:
                    if r.content_object == categoryModel:
                        tmp_model.append(r)
                if len(tmp_model):
                    orderId = tmp_model[0].order_id
                    orderTime = tmp_model[0].create_time
                else:
                    orderModel = UserBuyOrderModel(username=request.front_user, order_id=tradeNo, price=price,
                                                   content_object=categoryModel)
                    orderModel.save()
                    orderId = orderModel.order_id
                    orderTime = orderModel.create_time
            else:
                orderModel = UserBuyOrderModel(username=request.front_user, order_id=tradeNo, price=price,
                                               content_object=categoryModel)
                orderModel.save()

                orderId = orderModel.order_id
                orderTime = orderModel.create_time
            # 指定定时任务处理失效订单
            update_order_status.apply_async(args=[orderId], countdown=configs.ORDER_BEHIND_TIME)

    context = {
        'order_id': orderId,
        'create_time': orderTime,
    }
    return json_result(data=context)


# 提交预支付订单
@front_login_required
def pay_orders(request):
    '''
		type == 1 #支付宝
		type == 2 #微信
	'''
    if request.method == 'GET':
        return json_result(message=u'提交预支付订单!')

    else:
        orderId = request.POST.get('order_id', '')
        type = request.POST.get('type', 1)

        try:
            orderId = int(orderId)
            type = int(type)
        except:
            pass

        if type in [1, 2]:
            if type == 1:
                # 根据单号查询预支付订单信息
                orderModel = UserBuyOrderModel.objects.filter(username=request.front_user, order_id=orderId,
                                                              status=1).first()
                if not orderModel:
                    return json_params_error(message=u'此订单已支付/已失效!')

                if orderModel.content_object:
                    subject = orderModel.content_object.category
                else:
                    return json_params_error(message=u'此订单信息不完善!')

                result_url = y_alipay_return_url(
                    out_trade_no=orderId,
                    total_amount=float(orderModel.price),
                    subject=subject,
                )

                return json_result(data=result_url)
        # else:
        # 	return wechat_orders()

        else:
            return json_params_error(message=u'请选择支持的支付类型!')


# 支付宝异步回调验证
def alipay_verify_order(request):
    '''
		异步验证分两种方式，get和post
		get验证直接回调，post验证异步回调
	'''

    alipay = y_alipay()

    if request.method == 'GET':
        data = request.GET.dict()
        sign = data.pop('sign')
        success = alipay.verify(data, sign)

        if success:
            return redirect(reverse('front_method'))
    else:

        data = request.POST.dict()
        orderId = data['out_trade_no']  # 本地订单号
        tradeNo = data['trade_no']

        sign = data.pop('sign')

        success = alipay.verify(data, sign)

        if success:

            # 更新订单状态
            orderModel = UserBuyOrderModel.objects.filter(order_id=orderId, status=1).first()
            if not orderModel:
                return json_params_error(message=u'此订单不存在/已失效!')

            orderModel.status = 2
            orderModel.relevance_order = tradeNo
            orderModel.type = 1
            orderModel.save(update_fields=['status', 'relevance_order', 'type'])

            return HttpResponse('success')


# 支付宝订单支付状态手动校验
@front_login_required
def alipay_order_status(request, order_id=0):
    orderModel = UserBuyOrderModel.objects.filter(order_id=order_id).first()
    if orderModel:
        relevanceOrder = orderModel.relevance_order
        alipay = y_alipay()
        result = alipay.api_alipay_trade_query(out_trade_no=order_id, trade_no=relevanceOrder)

        if result.get('trade_status') == 'TRADE_SUCCESS':
            orderModel.status = 2
            orderModel.save()
            return json_result(message=u'交易成功,订单状态已更新!')
        else:
            return json_params_error(message=u'订单已失效/未付款!')

    else:
        return json_params_error(message=u'你尝试查看一个不存在的订单!')


# 个人中心-我的订单
@front_login_required
def my_orders(request, status=3):
    if status not in ['0', '1', '2', '3']:
        return json_params_error(message=u'你尝试查看一个不存在的分类!')

    if status == '3':
        ordersModel = UserBuyOrderModel.objects.filter(username=request.front_user).all()
    else:
        ordersModel = UserBuyOrderModel.objects.filter(username=request.front_user, status=int(status)).all()

    if ordersModel:
        tmp_order_list = []
        for r in ordersModel:
            courseModel = CourseModel.objects.filter(course=r.content_object).first()
            if courseModel:
                thumbnail = courseModel.thumbnail
            else:
                thumbnail = None
            tmp_order_list.append({
                'order_id': r.order_id,
                'create_time': r.create_time,
                'course': r.content_object.category,
                'thumbnail': thumbnail,
                'price': r.price,
                'status': r.status,
            })
        context = {
            'order_list': tmp_order_list,
        }
        return json_result(data=context)
    else:
        return json_params_error(message=u'暂无订单!')


# 用户反馈页面
@front_login_required
@require_http_methods(['GET', 'POST'])
def user_feed_back(request):
    if request.method == 'GET':
        return json_result(message=u'意见反馈页面!')
    else:
        content = request.POST.get('content', None)
        image = request.POST.get('image', None)
        iphone = request.POST.get('iphone', None)

        if content:
            userFeedBack = UserFeedBack(username=request.front_user, content=content, image=image, iphone=iphone)
            userFeedBack.save()
            return json_result(message=u'管理员已收到你的反馈,稍后会处理!')
        else:
            return json_params_error(message=u'请填写反馈内容!')


# 创建订单页面渲染
def front_create_orders(request):
    return render(request, 'create_orders.html')


# 用户意见反馈页面渲染
def front_user_feed_back(request):
    return render(request, 'feed_back.html')


# 校验用户信息是否完整
@front_login_required
@front_user_infomation_is_full
def user_message_complete(request):
    return json_result(message=u'用户信息完整')


# 用户获得勋章
@front_login_required
# @front_user_infomation_is_full
# 注入用户周年庆信息
@anniversary_data
@require_http_methods(['POST'])
def get_achievement(request):
    user = request.front_user
    anniversary2 = request.anniversary2

    uid = request.POST.get('uid', None)
    magazine = request.POST.get('magazine', None)
    mobile = request.POST.get('mobile', None)

    try:
        is_writer = int(request.POST.get('is_writer', 0))
        is_liaison = int(request.POST.get('is_liaison', 0))
        is_learner = int(request.POST.get('is_learner', 0))
    except:
        return json_params_error(message=u'friend类型参数不合法')

    if not uid:
        return json_params_error(message=u'uid缺失')
    # uid在勋章表是否存在
    try:
        medal = medalModel.objects.get(uid=uid)
    except ObjectDoesNotExist, e:
        return json_params_error(message=u'勋章uid不存在')

    user_medal = userMedalModel.objects.filter(user=user, medal=medal)
    # 勋章数量统计
    medal_count = userMedalModel.objects.filter(medal=medal).count()
    context = {'medal_count': medal_count}
    # 允许用户重复提交 更新勋章附属信息
    # 原早鸟勋章，后更名为医咖会见证者勋章
    if uid == 'old_bird':
        context = {'join_time': user.create_time, 'medal_count': medal_count}

        if user_medal:
            return json_params_error(message=u'用户已获取该勋章', data=context)
        userMedalModel(user=user, medal=medal).save()

        return json_result(message=u'成功获取勋章', data=context)
    # sci大神勋章
    elif uid == 'sci_god':

        if not magazine:
            return json_params_error(message=u'magazine缺失')
        # if not mobile:
        # 	return json_params_error(message=u'mobile缺失')
        if magazine.strip() == '':
            return json_params_error(message=u'magazine不能为空')
        # if mobile.strip() == '':
        # 	return json_params_error(message=u'mobile不能为空')

        if not anniversary2:
            anniversary2_data = {}
            anniversary2_data['sci_mobile'] = mobile
            anniversary2_data['magazine'] = magazine

            if user_medal:
                anniversaryModel(user=user, anniversary_times=2, data=json.dumps(anniversary2_data)).save()
                return json_params_error(message=u'用户已获取该勋章', data=context)

            userMedalModel(user=user, medal=medal).save()
            anniversaryModel(user=user, anniversary_times=2, data=json.dumps(anniversary2_data)).save()
            return json_result(message=u'成功获取勋章', data=context)
        else:
            anniversary2_data = json.loads(anniversary2.data)
            anniversary2_data['sci_mobile'] = mobile
            anniversary2_data['magazine'] = magazine

            if user_medal:
                anniversary2.data = json.dumps(anniversary2_data)
                anniversary2.save()
                return json_params_error(message=u'用户已获取该勋章', data=context)

            userMedalModel(user=user, medal=medal).save()
            anniversary2.data = json.dumps(anniversary2_data)
            anniversary2.save()
            return json_result(message=u'成功获取勋章', data=context)
    # 医咖会的朋友勋章
    elif uid == 'yizhu_friend':
        if is_writer == 0 and is_liaison == 0 and is_learner == 0:
            return json_params_error(message=u'yizhu_friend类型缺失')
        # 需要用户联系方式
        if is_writer == 1 or is_liaison == 1:
            if not mobile:
                return json_params_error(message=u'mobile缺失')
            if mobile.strip() == '':
                return json_params_error(message=u'mobile不能为空')

            if not anniversary2:
                anniversary2_data = {}
                anniversary2_data['friend_mobile'] = mobile
                anniversary2_data['is_writer'] = 1 if is_writer == 1 else 0
                anniversary2_data['is_liaison'] = 1 if is_liaison == 1 else 0
                anniversary2_data['is_learner'] = 1 if is_learner == 1 else 0

                if user_medal:
                    anniversaryModel(user=user, anniversary_times=2, data=json.dumps(anniversary2_data)).save()
                    return json_params_error(message=u'用户已获取该勋章', data=context)

                userMedalModel(user=user, medal=medal).save()
                anniversaryModel(user=user, anniversary_times=2, data=json.dumps(anniversary2_data)).save()
                return json_result(message=u'成功获取勋章', data=context)
            else:
                anniversary2_data = json.loads(anniversary2.data)
                anniversary2_data['friend_mobile'] = mobile
                anniversary2_data['is_writer'] = 1 if is_writer == 1 else 0
                anniversary2_data['is_liaison'] = 1 if is_liaison == 1 else 0
                anniversary2_data['is_learner'] = 1 if is_learner == 1 else 0

                if user_medal:
                    anniversary2.data = json.dumps(anniversary2_data)
                    anniversary2.save()
                    return json_params_error(message=u'用户已获取该勋章', data=context)

                anniversary2.data = json.dumps(anniversary2_data)
                anniversary2.save()
                userMedalModel(user=user, medal=medal).save()
                return json_result(message=u'成功获取勋章', data=context)
        # learner不需要联系方式
        else:
            if not anniversary2:
                anniversary2_data = {}
                anniversary2_data['is_writer'] = 0
                anniversary2_data['is_liaison'] = 0
                anniversary2_data['is_learner'] = 1

                if user_medal:
                    anniversaryModel(user=user, anniversary_times=2, data=json.dumps(anniversary2_data)).save()
                    return json_params_error(message=u'用户已获取该勋章', data=context)

                anniversaryModel(user=user, anniversary_times=2, data=json.dumps(anniversary2_data)).save()
                userMedalModel(user=user, medal=medal).save()
                return json_result(message=u'成功获取勋章', data=context)
            else:
                anniversary2_data = json.loads(anniversary2.data)
                anniversary2_data['is_writer'] = 0
                anniversary2_data['is_liaison'] = 0
                anniversary2_data['is_learner'] = 1
                # 对于已经留下联系方式的用户不予以删除
                # del anniversary2_data['friend_mobile']

                if user_medal:
                    anniversary2.data = json.dumps(anniversary2_data)
                    anniversary2.save()
                    return json_params_error(message=u'用户已获取该勋章', data=context)

                anniversary2.data = json.dumps(anniversary2_data)
                anniversary2.save()
                userMedalModel(user=user, medal=medal).save()
                return json_result(message=u'成功获取勋章', data=context)
    else:
        return json_params_error(message=u'勋章获取方式错误')


# 用户提交周年(可扩展)活动留言
@front_login_required
@front_user_infomation_is_full_soft
@require_http_methods(['POST'])
def add_activity_comments(request):
    user = request.front_user
    topic_type = request.POST.get('topic_type', 'twoYear')
    comments = request.POST.get('comments', None)

    if topic_type not in ['twoYear']:
        return json_params_error(message=u'topic_type类型错误')
    if not comments:
        return json_params_error(message=u'comments缺失')
    if comments.strip() == '':
        return json_params_error(message=u'comments不能为空')
    # TODO：留言数量限制
    if len(comments) >= 2000:
        return json_params_error(message=u'留言长度超过上限')

    specialTopicCommentModel(user=user, topic_type=topic_type, comments=comments).save()
    if request.is_user_information_full:
        return json_result(message=u'留言提交成功,用户信息完整')
    else:
        return json_result(message=u'留言提交成功,用户信息不完整')


# 周年活动留言点赞
@front_login_required
@require_http_methods(['GET'])
def activity_comment_like(request, comment_id=0):
    user = request.front_user

    if not specialTopicCommentModel.objects.filter(id=comment_id):
        return json_params_error(message=u'留言不存在')

    comment = specialTopicCommentModel(id=comment_id)
    comment_like = specialTopicCommentLikeModel.objects.filter(user=user, comment=comment)
    if not comment_like:
        specialTopicCommentLikeModel(user=user, comment=comment).save()
        context = {
            'is_praise': 1
        }
        return json_result(message=u'点赞成功', data=context)
    else:
        comment_like.delete()
        context = {
            'is_praise': 0,
        }
        return json_result(message=u'取消点赞成功', data=context)


# 获取用户勋章信息及全部勋章信息
@front_login_required
@require_http_methods(['GET'])
def get_achievements(request):
    user = request.front_user
    user_medals = list(
        userMedalModel.objects.filter(user=user, is_disabled=False, medal__is_valid=True).values('medal__id',
                                                                                                 'create_time'))
    medals = list(medalModel.objects.annotate(count=Count('usermedalmodel')).filter(is_valid=True).values())
    context = {
        'user_medals': user_medals,
        'medals': medals
    }
    return json_result(message=u'请求成功', data=context)


# 获取展示的话题留言列表
@require_http_methods(['GET'])
def get_activity_comments(request, topic_type='twoYear', page=1, pagesize=5):
    comments = specialTopicCommentModel.objects.order_by('-create_time').filter(is_publish=True)
    comments_list = list(comments.values())
    try:
        user = request.front_user
    except:
        user = None

    # user信息
    for i, comment in enumerate(comments):
        comments_list[i]['user'] = {}
        comments_list[i]['user']['username'] = comment.user.username
        comments_list[i]['user']['avatar'] = comment.user.avatar
        comments_list[i]['like_num'] = specialTopicCommentLikeModel.objects.filter(comment=comment).count()
        # 当前用户是否已点赞
        if not user:
            comments_list[i]['is_praise'] = 0
        else:
            history = specialTopicCommentLikeModel.objects.filter(user=user, comment=comment)
            if not history:
                comments_list[i]['is_praise'] = 0
            else:
                comments_list[i]['is_praise'] = 1
        try:
            reply = comments[i].specialtopiccommentreplymodel
        except:
            continue
        comments_list[i]['reply'] = {}
        comments_list[i]['reply']['content'] = reply.reply_content
        comments_list[i]['reply']['user_name'] = reply.reply_user
        comments_list[i]['reply']['create_time'] = reply.create_time
    paginator = Paginator(comments_list, pagesize)
    # 点赞数

    try:
        comments_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，则展示第1页
        comments_list = paginator.page(1)
    except EmptyPage:
        # 如果page超过范围，则展示最后一页
        comments_list = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    context = {
        'page': int(page),
        'pagesize': int(pagesize),
        'comments': list(comments_list.object_list),
        'page_count': int(paginator.num_pages)
    }

    return json_result(message=u'请求成功', data=context)


# 判定用户登录状态
def is_user_login(request):
    if not hasattr(request, 'front_user'):
        return json_result(message=u'未登录')
    if not request.front_user.is_active:
        return json_result(message=u'此账号被锁定,请联系管理员!')
    context = dict(avatar=user.avatar)
    return json_result(message=u'已登录', data=context)

# 判定用户是否参与过活动
@front_login_required
@require_http_methods(['GET'])
def already_join_anniversary(request):
    user = request.front_user
    medal = medalModel.objects.get(uid="yizhu_friend")

    user_medal = userMedalModel.objects.filter(medal=medal, user=user)
    context = {'avatar': user.avatar}
    if (len(user_medal) != 0):
        return json_result(message=u'已参与', data=context)

    return json_result(message=u'未参与', data=context)
