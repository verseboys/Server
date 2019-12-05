#coding:utf-8
#@author ：zhangx
'''
	webapp相关的模块
'''
import hashlib
import random
import time

from django.contrib.auth import authenticate, logout, login
from django.utils import timezone
from api.front.user_views import login_by_specific_backend
from extends import alisms
from extends.send_email import send_code_email
from frontmodel.models import FrontUserModel,ProfessionalSectionsModel,JobTitleModel
from questionsandanswersmodel.models import QuestionsModel,AnswersModel,PraiseAnswerModel,QuestionCategoryModel
from supervisormodel.models import ArticleCategoryMenuModel,ArticleIndexModel,GetResourceModel
from extends.buildjson import json_result,json_params_error,json_unauth_error
from extends.views import send_captcha_email
from frontmodel import configs
import re,datetime,logging
from django.views.decorators.http import require_http_methods
from frontmodel.decorators import front_login_required,front_user_infomation_is_full
from django.shortcuts import redirect,reverse
from django.core.cache import cache
from django.db.models import Q,Count
import api.front.views
from api.common.views import comment_time_period,add_answer
from methodmodel.models import  MethodArticleInfoModel,MethodCategoryModel,BannerModel,MethodArticleTopicModel
from newsmodel.models import NewsModel

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

CODE_TYPE_REGISTER = 'register'
CODE_TYPE_FORGET_PWD = 'forget_pwd'
CODE_TYPE_LOGIN = 'login'

@require_http_methods(['POST'])
def send_code(request):
    """
    POST webapp_front/send_code/
    wp 发送验证码,包含短信验证码和邮箱验证码

    req {
        identity: '' // 邮箱或手机号
        usage: '' // 用途 register、login、forget_pwd
    }

    """
    identity = request.POST.get('identity', None)
    usage = request.POST.get('usage',None)

    if not usage or usage not in [CODE_TYPE_REGISTER, CODE_TYPE_LOGIN, CODE_TYPE_FORGET_PWD]:
        return json_params_error(message='验证码用途错误')
    if not identity:
        return json_params_error(message='缺少手机号或邮箱')

    if re.match(configs.EMAIL_REGX, identity) or re.match(configs.PHONE_REGX, identity):
        user_exist = FrontUserModel.objects.filter(Q(email=identity) | Q(phone=identity)).exists()
    else:
        return json_params_error(message=u'手机号或邮箱格式错误')

    if usage == CODE_TYPE_REGISTER and user_exist:
        if re.match(configs.PHONE_REGX, identity):
            return json_params_error(message=u'手机号已被注册')
        else:
            return json_params_error(message=u'邮箱已被注册')
    elif usage == CODE_TYPE_FORGET_PWD and not user_exist:
        if re.match(configs.PHONE_REGX, identity):
            return json_params_error(message=u'手机号未注册')
        else:
            return json_params_error(message=u'邮箱未注册')
    elif usage == CODE_TYPE_LOGIN and not user_exist:
        if re.match(configs.PHONE_REGX, identity):
            return json_params_error(message=u'手机号未注册')
        else:
            return json_params_error(message=u'邮箱未注册')

    if '@' in identity:
        code = ''
        for i in range(6):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            code += ch
        if usage == CODE_TYPE_REGISTER:
            return _send_register_code_email(identity, code)
        if usage == CODE_TYPE_FORGET_PWD:
            return _send_forget_pwd_email(identity, code)
    else:
        cache_key = hashlib.md5(usage + identity).hexdigest()
        return _send_sms_code(cache_key, identity)


@require_http_methods(['POST'])
def forget_password(request):
    identity = request.POST.get('identity', None)
    validate_code = request.POST.get('code', None)
    # 去除首尾空格
    identity = None if identity == None else identity.strip()
    password = request.POST.get('password', None)

    logger.info({'identity': identity, 'password': 'hidden'})

    if re.match(configs.EMAIL_REGX, identity) or re.match(configs.PHONE_REGX, identity):
        try:
            exist_user = FrontUserModel.objects.get(Q(email=identity) | Q(phone=identity))
            exist_user.update_password(password)
        except FrontUserModel.DoesNotExist:
            return json_params_error(message=u'手机号或邮箱未注册')
    else:
        return json_params_error(message=u'手机号或邮箱格式错误')

    cache_key = hashlib.md5(CODE_TYPE_FORGET_PWD + identity).hexdigest()
    stored_code = cache.get(cache_key)['code']
    if not validate_code:
        return json_params_error(message=u'验证码不能为空')
    if not cache.get(cache_key):
        return json_params_error(message=u'验证码错误')
    if validate_code != stored_code:
        return json_params_error(message=u'验证码错误')

    if password:
        if len(password) < 4 or len(password) > 16:
            return json_params_error(message=u'密码长度在4~16位之间')
    else:
        return json_params_error(message=u'请输入密码')

    login_by_specific_backend(request, exist_user)
    cache.delete(cache_key)
    return json_result(message=u'修改成功')


def _send_register_code_email(email,code):
    message = u'你好!\n感谢你注册医咖会,\n请填写如下6位验证码:\n {}\n' \
              u'验证码在10分钟内有效，10分钟后需要重新激活邮箱\n\n' \
              u'如你未注册该网站，请忽略此邮件。\n' \
              u'此邮件为系统邮件请勿回复，如您想了解更多内容，欢迎访问我们的网站获取信息。'

    return send_code_email(email,'注册确认',message.format(code),code,key_head=CODE_TYPE_REGISTER)

def _send_forget_pwd_email(email,code):
    message = u'你好!\n你在{}提交了邮箱找回密码请求,\n请填写如下6位验证码：\n {}\n' \
              u'验证码在10分钟内有效，10分钟后需要重新激活邮箱\n\n' \
              u'此邮件为系统邮件请勿回复，如您想了解更多内容，欢迎访问我们的网站获取信息。'
    time_formated = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime())
    return send_code_email(email,'找回密码',message.format(time_formated,code),code,key_head=CODE_TYPE_FORGET_PWD)



def _send_sms_code(cache_key, phone, exipre_second=600):
    stored_value = cache.get(cache_key)
    if stored_value:
        if (timezone.now() - stored_value['send_time']).seconds < 60:
            return json_params_error(message=u'60秒内只能获取一次验证码', data={'phone': u'60秒内只能获取一次验证码'})

    code = alisms.send_verify_code(phone)
    value = dict(code=code, send_time=timezone.now())
    cache.set(cache_key, value, exipre_second)
    if alisms.DRYRUN:
        return json_result(message='短信已发送，测试模式：' + code)
    else:
        return json_result(message='短信已发送')


#注册
@require_http_methods(['GET','POST'])
def webapp_register(request):
    if request.method == 'GET':
        return json_result(message=u'这里是webapp注册页面')
    else:
        identity = request.POST.get('identity',None)
        validate_code =  request.POST.get('code',None)
        # 去除首尾空格
        identity = None if identity == None else identity.strip()

        password = request.POST.get('password',None)

        logger.info({'identity':identity,'password':'hidden'})

        if re.match(configs.EMAIL_REGX, identity):

            try:
                exist_user = FrontUserModel.objects.get(email =identity)
                return json_params_error(message=u'此邮箱已被注册!')
            except FrontUserModel.DoesNotExist:
                pass
            user = FrontUserModel(email=identity, password=password)
            user.create_user_by_email(email_need_validate=False)

        elif re.match(configs.PHONE_REGX, identity):
            try:
                exist_user = FrontUserModel.objects.get(phone=identity)
                return json_params_error(message=u'此手机已被注册')
            except FrontUserModel.DoesNotExist:
                pass
            user = FrontUserModel(phone=identity, password=password)
            user.create_user_by_phone()
        else:
            return json_params_error(message=u'手机号或邮箱格式错误')

        if password:
            if len(password)<4 or len(password)>16:
                return json_params_error(message=u'密码长度在4~16位之间')
        else:
            return json_params_error(message=u'请输入密码')

        cache_key = hashlib.md5(CODE_TYPE_REGISTER + identity).hexdigest()
        if not validate_code:
            return json_params_error(message=u'验证码不能为空')
        if not cache.get(cache_key):
            return json_params_error(message=u'验证码错误')
        stored_code = cache.get(cache_key)['code']
        # TODO 需要检查一下cache过期是直接删除还是会返回过期的属性，否则无法判断验证码过期还是没有验证码
        if not validate_code:
            return json_params_error(message=u'验证码错误', data={'captcha': u'验证码错误'})
        if validate_code != stored_code:
            return json_params_error(message=u'验证码错误', data={'captcha': u'验证码错误'})


        login_by_specific_backend(request,user)
        cache.delete(cache_key)
        return json_result(message=u'注册成功')



#登录
@require_http_methods(['GET','POST'])
def webapp_login(request):
    if request.method == 'GET':
        return json_result(message=u'这里是webapp登录页面')
    else:
        identity = request.POST.get('identity',None)
        password = request.POST.get('password',None)
        code =request.POST.get('code',None)

        logger.info({'identity':identity,'password':'hidden'})

        if identity and code:
            if not re.match(configs.PHONE_REGX, identity):
                return json_params_error(message=u'手机号格式错误')
            #短信登陆
            cache_key = hashlib.md5(CODE_TYPE_LOGIN + identity).hexdigest()
            if not cache.get(cache_key):
                return json_params_error(message=u'验证码错误')
            stored_code = cache.get(cache_key)['code']
            if not stored_code or (code != stored_code):
                return json_params_error(message=u'验证码错误')
            user = authenticate(phone=identity)
            if not user:
                return json_params_error(message=u'手机号未注册')
        elif identity and password:
            # 检查密码
            user = authenticate(identity=identity, password=password)
            if not user:
                return json_params_error(message=u'账号/密码错误')
        else:
            return json_params_error(message=u'账号/密码不能为空')

        if not user.is_active:
            return json_unauth_error(message=u'该账户被锁定,请联系管理员')

        login(request, user)
        return json_result(message=u'登录成功')



#退出
@front_login_required
def webapp_logout(request):
    logout(request)
    return redirect(reverse('webapp_login'))

#个人设置
@require_http_methods(['GET','POST'])
@front_login_required
def author_settings(request):
    if request.method == 'GET':
        return json_result(message=u'这是个人信息页面')
    else:
        corporation = request.POST.get('corporation',None) #所在公司
        professionId = request.POST.get('profession_id',None) #专业科室
        jobId = request.POST.get('job_id',None) #职称
        gender = request.POST.get('gender', 0) #性别
        avatar = request.POST.get('avatar',None)
        full_name = request.POST.get('full_name', None)

        try:
            gender = int(gender)
        except:
            pass

        logger.info({'corporation':corporation,'profession_id':professionId,'job_id':jobId,'gender':gender,'avatar':avatar})
        #过滤空格
        if corporation:
            corporation = corporation.replace(' ','')

        #判断提交的专业科室是否存在或者是否是最后一级
        if professionId:
            professionModel = ProfessionalSectionsModel.objects.get(pk = professionId)
            if professionModel:
                #判断职称是否为最后一级
                tmpProfessionModel = ProfessionalSectionsModel.objects.filter(Q(pk = professionId) & ~Q(professional_section = professionId)).first()
            else:
                return json_params_error(message=u'你选择的科室不存在')
        else:
            return json_params_error(message=u'请选择科室')

        #判断提交的职称是否存在或者是否是最后一级
        if jobId:
            jobModel = JobTitleModel.objects.get(pk = jobId)
            if jobModel:
                #判断职称是否为最后一级
                tmpJobModel = JobTitleModel.objects.filter(Q(pk = jobId) & ~Q(job_title = jobId)).first()
            else:
                return json_params_error(message=u'你选择的职称不存在')
        else:
            return json_params_error(message=u'请选择职称')

        if gender not in [0, 1]:
            return json_params_error(message=u'请选择真实性别')

        #如果用户状态为登录状态,则将提交的数据存储
        if hasattr(request,'front_user'):
            userModel = FrontUserModel.objects.filter(pk = request.front_user.id).first()
            if userModel:
                userModel.corporation = corporation or userModel.corporation
                userModel.profession = tmpProfessionModel
                userModel.jobtitle = tmpJobModel
                userModel.gender = gender
                userModel.avatar = avatar
                userModel.full_name = full_name or userModel.full_name
                userModel.save(update_fields=['corporation','profession','jobtitle','gender','avatar','full_name'])
                return json_result(message=u'个人资料已更新')
            else:
                return json_unauth_error(message=u'该用户不存在')
        else:
            return json_unauth_error(message=u'请先登录')

#专业科室
@front_login_required
def professional_sections(request,department_id=0):

    #传入科室id
    departmentId = int(department_id)

    logger.info({'department_id':departmentId})

    #判断科室是否传入,没有传入就返回第一级的科室列表
    if departmentId:
        #找出科室关联的下一级菜单
        professionalSectionsModel = ProfessionalSectionsModel.objects.filter(professional_section=departmentId).all()
        #如果下一级菜单存在,则表示不是最后一级
        if professionalSectionsModel:
            context = {
                'professionalSections': list(professionalSectionsModel.values()),
            }
            return json_result(data=context)
        #如果下一级不存在,则在库中查找是否有对应的科室，如果有则返回科室,如果没有则表示输入的信息非法。
        else:
            professionalSectionsModel = ProfessionalSectionsModel.objects.filter(pk=departmentId).values()
            if professionalSectionsModel:
                context = {
                    'professionalSections':list(professionalSectionsModel),
                }
                return json_result(data=context)
            else:
                return json_result(message=u'你提交的信息已传送到三界之外')

    else:
        professionalSectionsModel = ProfessionalSectionsModel.objects.filter(section_grade=1).values()
        context = {
            'professionalSections':list(professionalSectionsModel),
        }
        return json_result(data=context)

#职称
@front_login_required
def job_title(request,job_id=0):

    jobId = int(job_id)

    if jobId:
        #找出职称对应的下一级菜单
        jobTitleModel = JobTitleModel.objects.filter(job_title=jobId).all()
        #如果下一级菜单存在,则表示不是最后一级
        if jobTitleModel:
            context = {
                'jobTitles':list(jobTitleModel.values())
            }
            return json_result(data=context)
        #如果下一级不存在,则在库中查找是否有对应的职称,如果有则返回,如果没有则表示输入的信息非法。
        else:
            jobTitleModel = JobTitleModel.objects.filter(pk = jobId).values()
            if jobTitleModel:
                context = {
                    'jobTitles':list(jobTitleModel),
                }
                return json_result(data=context)
            else:
                return json_params_error(message=u'你提交的信息已传送到三界之外')
    else:
        jobTitleModel = JobTitleModel.objects.filter(job_grade=1).values()
        context = {
            'jobTitles':list(jobTitleModel),
        }
        return json_result(data=context)

#修改/找回密码
@require_http_methods(['GET','POST'])
def alter_password(request):
    if request.method == 'GET':
        return json_result(message=u'这是找回/修改密码页面')
    else:
        email = request.POST.get('email')
        emailCaptcha = request.POST.get('email_captcha')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        # 从cache中读取发送验证码时输入的邮箱，防止获取验证码后,又重新将邮箱修改为其他邮箱
        cache_data = cache.get(request.session.session_key)

        logger.info({'cache_data':cache_data,'password': password,'email':email,'emailCaptcha':emailCaptcha,'repeat_password':repeat_password})

        if email:
            if not re.match(configs.EMAIL_REGX,email):
                return json_params_error(message=u'邮箱格式不正确')
        else:
            return json_params_error(message=u'请输入邮箱')

        if emailCaptcha:
            #若cache_data是一个字典，那么表示已经点击发送邮件。如果不是字典，表示没有发送验证码邮件
            if isinstance(cache_data,dict):
                cache_captcha = cache_data['cache_captcha']

                if emailCaptcha.lower() != cache_captcha.lower():
                    return json_params_error(message=u'验证码错误')
            else:
                return json_params_error(message=u'请先发送验证码邮件')
        else:
            return json_params_error(message=u'请输入验证码')

        if password:
            if repeat_password:
                if not len(password) < 4 or len(password) > 20:
                    if password == repeat_password:
                        #判断cache 是否失效
                        if cache_data:
                            try:
                                user = FrontUserModel.objects.get(email=cache_data['email'])
                                user.update_password(password)
                                return json_result(message=u'密码修改成功!')
                            except:
                                return json_params_error(message=u'该邮箱未注册!')
                        else:
                            return json_params_error(message=u'验证码已失效')
                    else:
                        return json_params_error(message=u'两次密码不一样')
                else:
                    return json_params_error(message=u'密码长度在4~20位之间')
            else:
                return json_params_error(message=u'请再次输入密码')
        else:
            return json_params_error(message=u'请输入密码')

#给邮箱发送文本验证码
@require_http_methods(['POST'])
def send_email(request):
    email = request.POST.get('email')

    subject = u'[医咖会]-找回密码'
    message = {
        'first_content': u'这是来自[医咖会]的找回密码邮件,验证码：',
    }

    if email:
        if re.match(configs.EMAIL_REGX,email):
            result = send_captcha_email(request,email,subject=subject,message=message)
            if result:
                logger.info(u'邮箱%s的验证码是:%s,邮件发送成功'%(email,cache.get(request.session.session_key)['cache_captcha']))

                return json_result(message=u'验证码已发送到你的邮箱')
            else:
                logger.info(u'邮箱%s的验证码是:%s,邮件发送失败' % (email, request.session.get('check_captcha')))

                return json_params_error(message=u'邮件发送失败,请联系管理员')
        else:
            return json_params_error(message=u'请输入合法邮箱')
    else:
        return json_params_error(message=u'请输入邮箱')

# #问答列表
# def question_list(request,page=1):
#
# 	currentPage = int(page)
#
# 	#开始页和结束页,定义每页展示的条数
# 	start = (currentPage-1)*configs.NUM_PAGE
# 	end = start + configs.NUM_PAGE
#
# 	questionsModel = QuestionsModel.objects.filter(is_removed=0).order_by('-last_answer_time','-create_time')
# 	if questionsModel:
# 		questionsListModel = list(questionsModel.values())[start:end]
#
# 		#获得每个问题对应的用户属性,将用户属性和问题内容合并返回
# 		tmp_questionsModel = []
# 		for q in questionsListModel:
# 			user = FrontUserModel.objects.filter(id=q['author_id']).first()
# 			tmp_questionsModel.append({'username':user.username,'avatar':user.avatar,'desc':q})
#
# 		context = {
# 			'questions':tmp_questionsModel,
# 			'questions_count':questionsModel.count(),
# 			'currentPage':currentPage,
# 		}
# 		if request.is_ajax():
# 			return json_result(data=context)
# 		else:
# 			return json_result(data=context)
# 	else:
# 		return json_params_error(message=u'这是一片没有知识的荒原')
'''
'''

#问题详情
@front_login_required
def question_detail(request,question_id=0,page=1):

    try:
        questionId = int(question_id)
        currentPage = int(page)
    except:
        pass

    #定义开始和结束页，定义每页展示的条数
    start = (currentPage -1) *configs.NUM_PAGE
    end = start + configs.NUM_PAGE

    if questionId:
        questionModel = QuestionsModel.objects.filter(pk = questionId,is_removed=0).first()
        if questionModel:
            #统计阅读数
            questionModel.read_count()

            #计算该问题关联的一级评论的个数
            answerCount = AnswersModel.objects.filter(questions=questionModel,is_removed=0,relevance_answer=None).count()
            context = {
                'question': questionModel.content,
                'question_author': questionModel.author.username,
                'question_author_avatar': questionModel.author.avatar,
                'question_author_signature':questionModel.author.signature,
                'question_datetime': comment_time_period(questionModel.create_time),
                'answers_count':answerCount,
                'currentPage': currentPage,
                'question_id':questionModel.id,
                'category':questionModel.category.category,
            }
            #先过滤出一级评论
            answersModel = questionModel.answersmodel_set.filter(is_removed=0,relevance_answer=None).all().order_by('-create_time')

            #如果评论存在，则继续查找看是否有二级评论
            if answersModel:
                answersModel = answersModel[start:end]
                tmp_answers = []
                for a in answersModel:
                    #获取当前回答的点赞总数
                    praiseAnswerCount = PraiseAnswerModel.objects.filter(praise_answer=a).count()

                    #对于当前用户已点赞的,则显示黄色小手
                    isPraiseModel = PraiseAnswerModel.objects.filter(username=request.front_user,praise_answer=a).first()
                    if isPraiseModel:
                        is_praise = 1
                    else:
                        is_praise = 0

                    #查找出此回答关联的二级评论
                    secondLevelAnswersModel = AnswersModel.objects.filter(is_removed=0,relevance_answer=a).all()
                    #如果secondLevelAnsersModel为真，表示有二级评论，否则没有二级评论
                    tmp_second_level_answers = []
                    if secondLevelAnswersModel:
                        #定义二级评论临时列表
                        for s in secondLevelAnswersModel:
                            if s.relay_to:
                                relay_to = s.relay_to.username
                            else:
                                relay_to = None

                            #将二级评论存入列表
                            tmp_second_level_answers.append({
                                'answer_id':s.id,
                                'answer_user':s.author.username,
                                'answer_avatar':s.author.avatar,
                                'comment':s.comment,
                                'user_id':s.author.id,
                                'relay_to':relay_to,
                            })

                    tmp_answers.append({
                        'answer_id':a.id,
                        'answer_user':a.author.username,
                        'answer_user_avatar':a.author.avatar,
                        'comment':a.comment,
                        'create_time':comment_time_period(a.create_time),
                        'second_level_answers_count':secondLevelAnswersModel.count()-3,
                        'second_level_answers':tmp_second_level_answers[:3], #默认展示前3个回答
                        'is_praise':is_praise,
                        'praise_answer_count':praiseAnswerCount,
                    })

                context['answers'] = tmp_answers
                return json_result(message=u'查询成功',data=context)
            else:
                return json_result(data=context,message=u'暂无评论')
        else:
            return json_params_error(message=u'问题不存在/被删除')
    else:
        return json_params_error(message=u'这是一片没有知识的荒原')

#评论详情
@front_login_required
def answer_detail(request,question_id=0,answer_id=0,page=1):
    try:
        currentPage = int(page)
        questionId = int(question_id)
        answerId = int(answer_id)
    except:
        return json_params_error(message=u'请输入合法的信息')

    logger.info({'questionId': questionId,'answerId':answerId,'page':currentPage})

    start = (currentPage-1)*configs.NUM_PAGE
    end = start+configs.NUM_PAGE

    if questionId or answerId:
        questionModel = QuestionsModel.objects.filter(pk = questionId,is_removed=0).first()
        if questionModel:
            answerModel = AnswersModel.objects.filter(pk=answerId,questions=questionModel,is_removed=0).first()

            if answerModel:
                context = {
                    'answer_username':answerModel.author.username,
                    'answer_user_avatar':answerModel.author.avatar,
                    'comment':answerModel.comment,
                    'create_time':comment_time_period(answerModel.create_time),
                    'answer_id':answerModel.id,
                }
                # 检索二级评论
                secondLevelAnswersModel = AnswersModel.objects.filter(questions=questionModel,relevance_answer=answerModel, is_removed=0).all()[start:end]
                if secondLevelAnswersModel:
                    tmp_second_level_answer = []
                    for a in secondLevelAnswersModel:
                        if a.relay_to:
                            relay_to = a.relay_to.username
                        else:
                            relay_to = None

                        tmp_second_level_answer.append({
                            'second_level_answer_user': a.author.username,
                            'second_level_answer_user_avatar': a.author.avatar,
                            'second_level_answer': a.comment,
                            'relay_to':relay_to,
                            'second_level_answer_id':a.id,
                            'second_level_answer_user_id':a.author.id,
                        })

                    context['second_level_answers_count'] = secondLevelAnswersModel.count()
                    context['second_level_answers'] = tmp_second_level_answer

                    return json_result(data=context)
                else:
                    return json_params_error(message=u'请专业人员来点评吧')
            else:
                return json_params_error(message=u'回答不存在/被删除')
        else:
            return json_params_error(message=u'问题不存在/被删除')
    else:
        return json_params_error(message=u'这是一片没有知识的荒原')

#发布问题
@require_http_methods(['GET','POST'])
@front_login_required
@front_user_infomation_is_full#个人资料是否完善
def release_question(request):
    if request.method == 'GET':
        return json_result(message=u'这里是发布问题页面')
    else:
        content = request.POST.get('content',None)
        questionCategoryId = request.POST.get('question_category_id', 0)

        if content:
            if questionCategoryId:
                questionCategoryModel = QuestionCategoryModel.objects.filter(pk=questionCategoryId).first()
                if questionCategoryModel:
                    questionModel = QuestionsModel(author=request.front_user,content=content, category=questionCategoryModel,last_answer_time=datetime.datetime.now())
                    questionModel.save()

                    return json_result(message=u'发布问题成功!')
            else:
                return json_params_error(message=u'请选择分类!')
        else:
            return json_params_error(message=u'内容不能为空!')

#发表评论
@require_http_methods(['GET','POST'])
@front_login_required
@front_user_infomation_is_full #个人资料是否完善
def webapp_add_answer(request):
    #
    # if request.method == 'GET':
    #
    # 	return json_result(message=u'这里是添加评论页面')
    # else:
    # 	questionId = request.POST.get('question_id',None) #当前问题id
    # 	comment = request.POST.get('comment',None) #评论内容
    #
    # 	logger.info({'user':request.front_user.username,'questionId':questionId,'relevanceAnswerId':relevanceAnswerId,'comment':comment})
    #
    # 	#增加楼梯形式的评论
    # 	if questionId:
    # 		questionModel = QuestionsModel.objects.filter(pk=questionId,is_removed=0).first()
    # 		if questionModel:
    # 			#判断关联的回答id是否为真，如果为真则为子评论，如果不为真则为父评论
    # 			if relevanceAnswerId:
    # 				#查找库中是否存在此问题对应的回答且该回答没有被删除
    # 				answerModel = AnswersModel.objects.filter(pk = relevanceAnswerId,questions=questionModel,is_removed=0).first()
    # 				if answerModel:
    # 					answersModel = AnswersModel(author=request.front_user,questions=questionModel,comment=comment,relevance_answer=answerModel)
    # 					#更新问题模型中的最后评论时间
    # 					#根据需求，二级评论不需要对问题列表进行排序
    # 					questionModel.last_answer_time = datetime.datetime.now()
    # 					questionModel.save(update_fields=['last_answer_time'])
    # 					answersModel.save()
    #
    # 					logger.info({
    # 						'user':request.front_user,
    # 						'questionId':questionId,
    # 						'comment':comment,
    # 						'relevance_answer_id':relevanceAnswerId,
    # 					})
    #
    # 					return json_result(message=u'发表评论成功!')
    # 				else:
    # 					return json_params_error(message=u'你回复的回答已被删除!')
    # 			else:
    # 				#关联的回答id不为真,为父评论
    # 				answersModel = AnswersModel(author=request.front_user,questions=questionModel,comment=comment)
    # 				# 更新问题模型中的最后评论时间
    # 				questionModel.last_answer_time = datetime.datetime.now()
    # 				answersModel.save()
    # 				questionModel.save(update_fields=['last_answer_time'])
    #
    # 				logger.info({
    # 					'user': request.front_user,
    # 					'questionId': questionId,
    # 					'comment': comment,
    # 					'relevance_answer_id': relevanceAnswerId,
    # 				})
    #
    # 				return json_result(message=u'发表评论成功!')
    # 		else:
    # 			return json_params_error(message=u'问题不存在/被删除!')
    # 	else:
    # 		return json_params_error(message=u'这是一片没有知识的荒原!')
    return add_answer(request)

#我的问题
@front_login_required
def my_questions(request,page=1):
    try:
        currentPage = int(page)
    except:pass

    numPage = int(configs.NUM_PAGE)
    start = (currentPage-1)*numPage
    end = start + configs.NUM_PAGE

    #获得当前用户提交的问题列表
    questionListModel = QuestionsModel.objects.filter(author = request.front_user,is_removed=0).all().order_by('-last_answer_time','-create_time')
    #
    # if questionListModel:
    # 	questions = list(questionListModel.values('id','content','create_time'))[start:end]
    #
    # 	context = {
    # 		'username':request.front_user.username,
    # 		'avatar':request.front_user.avatar,
    # 		'questions':questions,
    # 		'questions_count':questionListModel.count(),
    # 		'currentPage':currentPage,
    # 	}
    # 	if request.is_ajax():
    # 		return json_result(data=context)
    # 	else:
    # 		return json_result(data=context)
    # else:
    # 	context = {
    # 		'username':request.front_user.username,
    # 		'avatar':request.front_user.avatar,
    # 		'questions_count': 0,
    # 	}
    # 	return json_result(message=u'你还没有发表过问题!',data=context)

    context = {
        'username': request.front_user.username,
        'avatar': request.front_user.avatar,
        'signature': request.front_user.signature,
    }

    if questionListModel:

        questionCount = questionListModel.count()

        pageCount = questionCount / numPage
        if questionCount % numPage > 0:
            pageCount +=1

        questionListModel = questionListModel[start:end]

        tmp_questions = []
        # 遍历过滤后的问题列表,如果当前问题有回复，则取出最后的回复信息，如果没有回复则取出问题信息

        for r in questionListModel:

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
                    'answers_count': None,
                })

        context['questions_list'] = tmp_questions
        context['question_count'] = questionCount
        context['current_page'] = currentPage
        context['page_count'] = pageCount

        return json_result(data=context)
    else:

        return json_result(message=u'该用户惜字如金!',data=context)

# #问题搜索
# @require_http_methods(['POST'])
# def search(request):
# 	currentPage = request.POST.get('page',1)
# 	searchWord = request.POST.get('search_word',None)
#
# 	try:
# 		currentPage = int(currentPage)
# 	except:
# 		return json_params_error(u'请输入正确的页码')
#
# 	logger.info({'searchWord':searchWord,'currentPage':currentPage})
#
# 	if searchWord:
# 		#检索相关的问题
# 		'''
# 			这里有个bug,因为目前存储格式是富文本，因此在检索和标签相关的单词的时候，有可能会匹配出所有信息
# 		'''
# 		questionModel = QuestionsModel.objects.filter(content__icontains = searchWord ,is_removed= 0 ).order_by('-last_answer_time','-create_time')
# 		if questionModel:
# 			#每页显示条数
# 			numPage = int(configs.NUM_PAGE)
# 			start = (currentPage -1 )*numPage
# 			end = start +numPage
#
# 			#计算检索出来的问题总数
# 			questionCount = questionModel.count()
#
# 			#将检索的数据转换成json
# 			questions = list(questionModel.values('id','content','author','create_time')[start:end])
#
# 			tmpQuestions = []
# 			for q in questions:
# 				if q['author']:
# 					user = FrontUserModel.objects.filter(pk = q['author']).first()
# 					if user:
# 						tmpQuestions.append({'username':user.username,'avatar':user.avatar,'desc':q})
# 				else:
# 					return json_params_error(message=u'这是一个匿名问题')
#
# 			context = {
# 				'currentPage':currentPage,
# 				'questionCount':questionCount,
# 				'questions':tmpQuestions,
# 			}
#
# 			if request.is_ajax():
# 				return json_result(data=context)
# 			else:
# 				return json_result(data=context)
#
# 		else:
# 			return json_params_error(message=u'暂无相关的信息')
# 	else:
# 		return json_params_error(message=u'请输入搜索关键词')
#

'''
################     微信自定义菜单接口开始    ###################
'''

#文章分类摘要
def article_category_info(request,category_id=0):
    try:
        categoryId = int(category_id)
    except:pass

    if categoryId:
        articleCategoryMenuModel = ArticleCategoryMenuModel.objects.filter(pk = categoryId).first()
        if articleCategoryMenuModel:
            context = {
                'id':articleCategoryMenuModel.id,
                'category':articleCategoryMenuModel.category,
                'summary':articleCategoryMenuModel.summary,
            }
            return json_result(data=context)
        else:
            return json_params_error(message=u'你尝试访问一个不存在的分类!')
    else:
        return json_params_error(message=u'你尝试访问一个不存在的分类信息!')

#分类文章列表
def article_category_list(request,category_id=0,page=1):
    try:
        categoryId = int(category_id)
        currentPage = int(page)
    except:
        pass

    if categoryId:
        articleCategoryMenuModel = ArticleCategoryMenuModel.objects.filter(pk=categoryId).first()
        if articleCategoryMenuModel:
            articleIndexModel = ArticleIndexModel.objects.filter(category=articleCategoryMenuModel).values('id','title','category','index')
            if articleIndexModel:
                numPage = int(configs.PC_FRONT_NUM_PAGE)
                start = (currentPage-1)*numPage
                end = start +numPage

                context = {
                    'article_index_list': list(articleIndexModel)[start:end],
                    'currentPage': currentPage,
                }
                return json_result(data=context)
            else:
                return json_result(message=u'此分类下暂无文章!')
        else:
            return json_params_error(message=u'你尝试访问一个不存在的分类!')
    else:
        return json_params_error(message=u'你尝试访问一个不存在的分类信息!')

#搜索分类下的文章
@require_http_methods(['GET','POST'])
def search_category_article(request,category_id,page=1):
    try:
        categoryId = int(category_id)
        currentPage = int(page)
    except:
        pass
    if request.method == 'GET':
        return json_result(message=u'这是搜索分类下的文章页面!')
    else:
        title = request.POST.get('title',None)
        if title:
            if categoryId:
                articleCategoryMenuModel = ArticleCategoryMenuModel.objects.filter(pk=categoryId).first()
                if articleCategoryMenuModel:
                    articleIndexModel = ArticleIndexModel.objects.filter(category=articleCategoryMenuModel,title__icontains=title).values('id', 'title', 'category', 'index')
                    if articleIndexModel:
                        numPage = int(configs.PC_FRONT_NUM_PAGE)
                        start = (currentPage - 1) * numPage
                        end = start + numPage

                        context = {
                            'article_index_list': list(articleIndexModel)[start:end],
                            'currentPage': currentPage,
                        }
                        return json_result(data=context)
                    else:
                        return json_result(message=u'暂无相关文章!')
                else:
                    return json_params_error(message=u'你尝试访问一个不存在的分类!')
            else:
                return json_params_error(message=u'你尝试访问一个不存在的分类信息!')
        else:
            return json_params_error(message=u'请输入搜索的关键词!')
'''
################     微信自定义菜单接口结束    ###################
'''


'''
    author : zhangx
    date : 20171130
    mark :
        1、增加资源分发注册功能。
        2、用户在阅读微信文章的时候若想获取原文资源，则需要通过注册，注册成功后才会发送文章原文。
        3、若用户已经注册,则直接点击获取资源。
        4、后台统一对资源进行下发

'''
#通过阅读微信文章获取资源的注册页面
@require_http_methods(['GET','POST'])
def get_resource_register(request,article_id=0):

    try:
        articleId = int(article_id)
    except:pass

    if request.method == 'GET':
        return json_result(message=u'阅读微信文章的用户获取资源注册页面')
    else:
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repeat_password = request.POST.get('repeat_password', None)

        logger.info({'email': email, 'username': username, 'password': password, 'repeat_password': repeat_password,'article_id':articleId})

        # 验证用户名
        if username:
            username = username.replace(' ', '')  # 去除空格
            if username in configs.ILLEGALITY_NAME:
                return json_params_error(message=u'请输入合法用户名!')

            repeat_username = FrontUserModel.objects.filter(username=username).first()
            if repeat_username:
                return json_params_error(message=u'该用户已被注册!可直接获取资源!')
        else:
            return json_params_error(message=u'请输入用户名!')

        # 验证邮箱
        if email:
            if not re.match(configs.EMAIL_REGX, email):
                return json_params_error(message=u'请输入合法邮箱!')

            emailModel = FrontUserModel.objects.filter(email=email).first()
            if emailModel:
                return json_params_error(message=u'该邮箱已被注册!可直接获取资源!')
        else:
            return json_params_error(message=u'请输入邮箱!')

        if password:
            if len(password) < 4 or len(password) > 20:
                return json_params_error(message=u'密码长度在4~20位之间!')
        else:
            return json_params_error(message=u'请输入密码!')

        if repeat_password:
            if password != repeat_password:
                return json_params_error(message=u'两次密码不一致!')
        else:
            return json_params_error(message=u'请确认密码!')

        user = FrontUserModel(email=email, username=username, password=password)
        user.save()
        # 注册成功后,直接登录
        login_by_specific_backend(request, user)


        #将注册的用户信息同步到获取资源申请表中
        if articleId:
            articleIndexModel = ArticleIndexModel.objects.filter(pk=articleId).first()
            if articleIndexModel:
                userModel = FrontUserModel.objects.filter(username=username).first()
                if userModel:
                    getResourceModel = GetResourceModel(username=userModel, article_id=articleIndexModel)
                    getResourceModel.save()
                    return json_result(message=u'小咖正在处理您的申请，稍后请记得查看邮箱~')
                else:
                    return json_params_error(message=u'此用户不存在!')
            else:
                return json_params_error(message=u'暂无此资源!')
        else:
            return json_params_error(message=u'你尝试获取一个不存在的资源!')

#已注册的用户获取资源
def get_resource_user_is_active(request,article_id=0):
    try:
        articleId = int(article_id)
    except:
        pass

    if request.method == 'GET':
        return json_result(message=u'已注册的用户获取资源页面!')
    else:
        email = request.POST.get('email',None)
        if articleId:
            articleIndexModel = ArticleIndexModel.objects.filter(pk = articleId).first()
            if articleIndexModel:
                if email:
                    userModel = FrontUserModel.objects.filter(email=email).first()
                    if userModel:
                        getResourceModel = GetResourceModel(username=userModel,article_id=articleIndexModel)
                        getResourceModel.save()
                        return json_result(message=u'资源获取申请成功!请等待管理员处理!')
                    else:
                        return json_params_error(message=u'此邮箱还未注册过医咖会!')
                else:
                    return json_params_error(message=u'你尝试发送给一个不存在的用户!')
            else:
                return json_params_error(message=u'暂无此资源!')
        else:
            return json_params_error(message=u'你尝试获取一个不存在的资源!')

'''
    author :zhangx
    date: 20180108
    mark：
        以下是webapp3.0版本内容
'''

#最新回答列表首页
def recently_ask_list(request,category_id=0,page=1):
    '''
        1、这里包含问答分类列表
        2、最新问答问题列表
    '''
    return api.front.views.recently_questions(request,category_id=category_id,page=page)

#热门问答列表
def hold_ask_list(request,category_id=0,page=1):
    return api.front.views.hold_questions(request,category_id=category_id,page=page)

#搜索
@require_http_methods(['GET','POST'])
def search_ask(request,page=1):
    return api.front.views.search_questions_and_answers(request,section_id=3,time=0,page=page)

#点赞和取消点赞回答
def praise_answer(request,answer_id=0):
    return api.front.views.praise_answer(request,answer_id=answer_id)

#问题分类列表
def question_category_list(request):
    return api.front.views.front_question_category_list(request)

'''
    author:zhangx
    date: 20180323
    mark:
        webapp4.0版本内容
'''

#首页banner
def banner(request):
    bannerModel = BannerModel.objects.filter(is_active=1,type=2).order_by('rank').values('id', 'name', 'link').order_by('rank')
    bannerModel = list(bannerModel)
    return json_result(data=bannerModel)

#首页最新的研究方法
def recently_method_article(request):
    methodArticleInfoModel = MethodArticleInfoModel.objects.filter(status__in=[1, 2]).all().order_by('-arrange', '-create_time')[0:3]
    if methodArticleInfoModel:
        article_list = []
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
                'app_thumbnail': m.app_thumbnail,
                'create_time': comment_time_period(m.create_time),
                'category': category,
                'category_id': m.category.id,
            })
        return json_result(data=article_list)
    else:
        return json_params_error(message=u'暂无研究方法!')

#首页最新的研究问答
def recently_ask(request):
    recentlyQuestionsModel = QuestionsModel.objects.filter(is_removed=0).order_by('-top', '-last_answer_time', '-create_time').all()[0:3]
    if recentlyQuestionsModel:
        tmp_questions = []
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

        return json_result(data=tmp_questions)
    else:
        return json_params_error(message=u'暂无问答信息!')

#首页最新研究进展
def recently_news(request):
    newsModel = NewsModel.objects.filter(status__in=[1, 2]).all()[0:3]
    if newsModel:
        news_list = []
        for n in newsModel:
            if n.category:
                category = n.category.category
            else:
                category = None
            news_list.append({
                'id': n.id,
                'title': n.title,
                'summary': n.summary,
                'app_thumbnail': n.app_thumbnail,
            })
        return json_result(data=news_list)
    else:
        return json_params_error(message=u'暂无最新进展')

#研究方法文章列表
def method_articles(request,page=1,category_id=0):
    return api.front.views.method_articles(request,page=page,category_id=category_id)

#研究方法分类banner
def method_category_banner(request):
    # 先过滤出一级分类,去掉更多教程分类
    methodCategoryModel = MethodCategoryModel.objects.exclude(pk=13).filter(relevance_category__isnull=True, is_active=1).all()
    if methodCategoryModel:
        tmp_category = []
        for m in methodCategoryModel:
            tmp_category.append({
                'id':m.id,
                'category':m.category,
                'banner':m.banner,
            })
        return json_result(data=tmp_category)
    else:
        return json_params_error(message=u'暂无分类!')

#研究方法专题合集
def method_topic_list(request):
    methodArticleTopicModel = MethodArticleTopicModel.objects.filter(status=2).annotate(article_count=Count('topicrelatedmethodarticlemodel')).values('id', 'title', 'summary', 'app_thumbnail', 'thumbnail', 'article_count').order_by('arrange')

    methodArticleTopicModel = list(methodArticleTopicModel)
    return json_result(data=methodArticleTopicModel)

#研究方法专题详情
def method_topic_detail(request,topic_id=0,page=1):
    return api.front.views.method_topic_detail(request,topic_id=topic_id,page=page)

#研究方法专题文章详情
def method_topic_article_detail(request,article_id=0):
    context = api.front.views.method_article_detail(request,article_id=article_id)
    return json_result(data=context)

#研究方法文章详情
def method_article_detail(request,article_id=0):
    context = api.front.views.method_article_detail(request,article_id=article_id)
    return json_result(data=context)

#研究方法发表问题
def method_release_ask(request):
    return api.front.views.front_release_question(request)

#研究方法文章的问答列表
def method_article_detail_ask_list(request,article_id=0,ask_page=1):
    return api.front.views.method_article_detail_ask_list(request,article_id=article_id,ask_page=ask_page)

#研究进展首页新闻列表
def news(request,category_id=0, page=1):
    return api.front.views.news(request,page=page,category_id=category_id)

#研究进展新闻详情
def news_detail(request,news_id=0,page=1):
    return api.front.views.news_detail(request,news_id=news_id,page=page)

#搜索文章
def search_article(request,section_id=1,page=1):
    '''
        section_id=1：研究方法
        section_id=2: 研究进展
    '''
    return api.front.views.search_article(request,section_id=section_id,page=page,time_id=4)

#添加研究进展评论
def add_news_comment(request,news_id=0):
    return api.front.views.add_news_comment(request,news_id=news_id)











