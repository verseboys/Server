#coding:utf-8

from frontmodel.models import FrontUserModel,UserBuyOrderModel
from questionsandanswersmodel.models import QuestionsModel,AnswersModel,QuestionCategoryModel
#from articlemodel.models import ArticleModel, CommentModel,TagsModel,SectionModel
from supervisormodel.models import ArticleCategoryMenuModel,ArticleIndexModel,GetResourceModel
from extends.buildjson import json_result,json_params_error,json_method_error,json_unauth_error,json_redirect_error
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect,reverse
import sys,logging,time,datetime,os,json
from frontmodel import configs
from yizhu import settings
from api.common.views import question_detail
from extends.send_email import send_attach_email
from django.db.models import Q,Count,Sum
from django.db.models.functions import Greatest, Coalesce
from methodmodel.models import MethodCategoryModel,MethodArticleInfoModel,MethodArticleContentModel,MethodArticleContentSectionModel,MethodArticleRelatedReadingModel,BannerModel,MethodArticleTopicModel,TopicRelatedMethodArticleModel,KeyWordGroupModel,KeyWordModel,KeyWordRelevanceArticleModel
from newsmodel.models import NewsCategoryModel,NewsModel,NewsCommentModel,NewsRelatedReadingModel,HoldNewsModel
from videomodel.models import VideoModel,CourseModel,VideoCommentModel,VideoRelatedDataModel
import api.front.views
from supervisormodel.models import UserFeedBack
from anniversary.models import medalModel,userMedalModel,anniversaryModel,specialTopicCommentModel,specialTopicCommentLikeModel,specialTopicCommentReplyModel
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.forms.models import model_to_dict
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

from django.contrib.auth.decorators import REDIRECT_FIELD_NAME, user_passes_test
from django.contrib.auth.models import User as DjangoUser
def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    内容摘自 django.contrib.auth.decorators.login_required，将条件改为要求必须是 DjangoUser
    背景：目前将网站、管理后台使用同一套 session 系统，因此 request.user 可能是 Django 的 User，
    也可能是 FrontUserModel
    """
    actual_decorator = user_passes_test(
        lambda u: isinstance(u, DjangoUser) and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

#登录
@require_http_methods(['GET','POST'])
def sup_login(request):
	if request.method == 'GET':
		return json_result(message=u'这里是登录页面')
	else:
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)

		logger.info({'username':username,'password':password})

		user = authenticate(username=username,password=password)

		if user:
			if user.is_active:
				login(request, user)

				return json_result(message=u'登录成功', data={'username': username})
			else:
				return json_params_error(message=u'此管理员已经被封杀,请联系超级管理员!')
		else:
			return json_params_error(message=u'账号/密码错误')


#退出
@login_required
def sup_logout(request):
	logout(request)
	return redirect(reverse('sup_login'))

#用户管理
@login_required
def user_management(request,page=1):

	try:
		currentPage = int(page)
	except:pass

	usersModel = FrontUserModel.objects.all().values('id', 'username', 'avatar', 'create_time', 'is_active').order_by('-create_time')

	if usersModel:
		#每页显示条数
		numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
		start = (currentPage-1)*numPage
		end = start+numPage
		
		#计算出用户总数
		userCount = usersModel.count()
		#计算出总页数
		pageCount = userCount/numPage
		if userCount%numPage >0:
			pageCount +=1
		
		#对用户总数进行切片
		usersModel = list(usersModel)[start:end]

		context = {
			'users':usersModel,
			'currentPage':currentPage,
			'pageCount':pageCount,
		}
		return json_result(data=context)

#用户详情
@login_required
def user_detail(request,user_id=0):
	try:
		userId = int(user_id)
	except:pass

	logger.info({'user_id':userId})
	
	userModel = FrontUserModel.objects.filter(pk = userId).first()
	if userModel:
		#判断用户是否有科室
		if userModel.profession:
			departmentName = userModel.profession.department_name
		else:
			departmentName = None
		
		#判断用户是否有职称
		if userModel.jobtitle:
			jobName = userModel.jobtitle.job_name
		else:
			jobName = None
		
		#判断用户是否有头像
		if userModel.avatar:
			avatar = userModel.avatar
		else:
			avatar = None
		
		#判断公司是否填写
		if userModel.corporation:
			corporation = userModel.corporation
		else:
			corporation = None
			
		#判断用户的手机号是否存在
		if userModel.mobile:
			mobile = userModel.mobile
		else:
			mobile = None
		
		context = {
			'id':userModel.id,
			'username':userModel.username,
			'email':userModel.email,
			'mobile':mobile,
			'gender':userModel.get_gender_display(),
			'avatar':avatar,
			'corporation': corporation,
			'profession':departmentName,
			'jobtitle':jobName,
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'你尝试查看一个不存在的用户')

#用户锁定
@require_http_methods(['POST'])
@login_required
def lock_user(request):
	userId = request.POST.get('user_id',0)
	userModel = FrontUserModel.objects.filter(pk = userId).first()
	if userModel:
		userModel.is_active = 0
		userModel.save(update_fields=['is_active'])
		context = {
			'user': userModel.username
		}
		return json_result(data=context,message=u'用户已被锁定')
	else:
		return json_params_error(message=u'你尝试锁定一个不存在的用户')



#搜索用户
#20180306新增搜索用户接口
# @login_required
@require_http_methods(['GET','POST'])
def search_user(request, page=1):
	try:
		currentPage = int(page)
	except:
		pass
	if request.method == 'POST':
		searchKeyWords = request.POST.get('search_key_words',None)

		if searchKeyWords:

			usersModel = FrontUserModel.objects.filter(Q(username__icontains=searchKeyWords) | Q(email__icontains=searchKeyWords)).values('id', 'username', 'avatar', 'create_time', 'is_active').order_by('-create_time')

			if usersModel:
				# 每页显示条数
				numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
				start = (currentPage - 1) * numPage
				end = start + numPage

				# 计算出用户总数
				userCount = usersModel.count()
				# 计算出总页数
				pageCount = userCount / numPage
				if userCount % numPage > 0:
					pageCount += 1

				# 对用户总数进行切片
				usersModel = list(usersModel)[start:end]

				context = {
					'users': usersModel,
					'currentPage': currentPage,
					'pageCount': pageCount,
				}
				return json_result(data=context)
			return json_params_error(message=u'查无此人!')
		else:
			return json_params_error(message=u'用户名不能为空!')


#新增按日期过滤用户的接口
@require_http_methods(["GET"])
@login_required
def filter_user_date(request):
	'''
	根据后台管理员选择的日期对用户列表进行按日期区间进行筛选,并且以excel格式导出
	由于目前需求简单，只需要按日期区间筛选出相应日期范围内的用户数据，并且导出
	GET /supervisor/filter_user_date?start_date=xxx&end_date=xxx
	Querystring: start_date,end_date 必选 ,格式为 "2019-04-01"
		前端实现: 只有当start_date 和 end_date都已选择日期，然后点击导出，才会调用该请求
	Status: 正常时返回200
	Response: 返回日期区间内的用户数据，数据结构见以下实例。
	{
		"message": "",
		"code": 200,
		"data": {
			"users": [
				{
					"username": "medi_4582388",
					"is_active": 1,
					"email": "mameng@natureself.cn",
					"create_time": "2019-04-03T17:13:31.500",
					"avatar": "yika_admin.png",
					"id": 8777
				},
			]
		}
	}
	'''


	users = FrontUserModel.objects.all().values('id', 'username', 'email', 'avatar', 'create_time','is_active').order_by('-create_time')
	if 'start_date' in  request.GET:
		start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%Y-%m-%d")
	 	users = users.filter(create_time__gte=start_date)

	if 'end_date' in  request.GET:
		end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%Y-%m-%d")
		users = users.filter(create_time__lte=end_date + datetime.timedelta(days=1))

	return json_result(data={'users':  list(users)})

'''
##########################################################

	下面的接口是微信端( webapp)问答管理系统的后台管理的接口

################     微信端接口开始     ###################
'''

#问题列表
@login_required
def question_list(request,page=1):

	currentPage = int(page)

	questionModel = QuestionsModel.objects.filter(is_removed=0).all() \
																.annotate(last_activity=Coalesce(Greatest('create_time', 'last_answer_time'),'create_time')) \
															  .order_by('-last_activity')
	if questionModel:
		#每页显示条数
		numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
		start = (currentPage-1)*numPage
		end =start + numPage
		
		#计算问题总数
		questionCount = questionModel.count()
		
		#计算出总页数
		pageCount = questionCount/numPage
		if questionCount%numPage>0:
			pageCount +=1

		#在values中获取外键属性的方式：author__username
		questionModel = list(questionModel.values('id','content','author__username','create_time')[start:end])
		
		context = {
			'questions':questionModel,
			'currentPage':currentPage,
			'pageCount':pageCount,
		}
		return json_result(data=context)
		
	else:
		return json_params_error(message=u'暂无问题')

#问题详情
'''
	date: 20170823
	author:zhangx
	mark:
		修改问答详情
'''
@login_required
def supervisor_question_detail(request,question_id=0,answer_id=0,parent_page=1,child_page=1):
	context = question_detail(request, question_id=question_id, answer_id=answer_id, parent_page=parent_page, child_page=child_page)

	return json_result(data=context)


@require_http_methods(['POST'])
@login_required
def delete_question(request):
	questionId = request.POST.get('question_id', 0)
	
	try:
		questionId = int(questionId)
	except:
		pass

	if questionId:
		questionModel = QuestionsModel.objects.filter(pk = questionId,is_removed=0).first()
		if questionModel:
			#获得问题关联的回答并删除
			answersModel = questionModel.answersmodel_set.all()
			questionModel.is_removed = 1
			answersModel.update(is_removed= 1 ) #将所有关联的回答状态置为真
			questionModel.save(update_fields=['is_removed'])
			
			return json_result(message=u'删除问题成功,关联的回答已删除')
		else:
			return json_params_error(message=u'你尝试删除一个不存在的问题')
	else:
		return json_params_error(message=u'你访问的链接不存在')

#删除回答
@require_http_methods(['POST'])
@login_required
def delete_answer(request):
	answerId = request.POST.get('answer_id', 0)

	try:
		answerId = int(answerId)
	except:
		pass

	logger.info({'answer_id':answerId})
	#删除回答的时候需要同时区分是二级评论还是一级评论，
	#如果是一级评论还需要判断这个评论是否是最后一条评论，
	#如果是最后一条评论，则需要更新问题模型中的最新评论时间
	#一级回答被删除，那么关联的二级回答也需要全部删除
	if answerId:
		answerModel = AnswersModel.objects.filter(pk = answerId,is_removed=0).first()

		if answerModel:
			#如果要删除的评论存在且没有被删除，则判断是否为一级评论
			parentAnswerModel = AnswersModel.objects.filter(pk = answerId,is_removed=0,relevance_answer=None).first()

			# 如果parentAnswerModel为真,则为一级评论。
			if parentAnswerModel:
				logger.info({'parentAnswerModel': parentAnswerModel.id})
				#需要判断这个评论是否为最后一条评论
				#直接通过评论反查关联的问题
				questionModel = QuestionsModel.objects.filter(pk = parentAnswerModel.questions.id,is_removed=0).first()

				logger.info({'questionModel': questionModel.id})

				#获取这个问题所有的一级评论
				allAnswerModel = AnswersModel.objects.filter(questions=questionModel,is_removed=0,relevance_answer=None).all()

				#如果一级评论总数大于1,则表示有多条评论
				if allAnswerModel.count()>1:
					# 如果是最后一条评论,那么在删除这条评论的同时需要将问题模型中的最后评论时间更新为倒数第2条评论的时间
					lastAnswerModel = allAnswerModel.last()#最后一条评论
					lastButOneAnswerModel = allAnswerModel[allAnswerModel.count()-2:allAnswerModel.count()-1] #倒数第二条评论
					logger.info({'lastButOneAnswerModel': lastButOneAnswerModel[0].create_time})

					if parentAnswerModel == lastAnswerModel:
						questionModel.last_answer_time = lastButOneAnswerModel[0].create_time
						questionModel.save(update_fields=['last_answer_time'])
					parentAnswerModel.is_removed = 1
					parentAnswerModel.save(update_fields=['is_removed'])
					return json_result(message=u'删除回答成功')

				else:
					#表示只有一条评论
					#需要判断这个评论下是否有关联的二级评论
					secondLevelAnswerModel = AnswersModel.objects.filter(is_removed=0,relevance_answer=answerId).all()
					if secondLevelAnswerModel:
						secondLevelAnswerModel.update(is_removed = 1)

					answerModel.is_removed = 1
					#删除这条评论的时候需要更新问题模型的最后回答时间
					logger.info({'questionModel.create_time': questionModel.create_time})

					questionModel.last_answer_time = questionModel.create_time
					answerModel.save(update_fields=['is_removed'])
					questionModel.save(update_fields = ['last_answer_time'])

					return json_result(message=u'删除回答成功')
			else:
				#则为二级评论，直接删除即可
				answerModel.is_removed = 1
				answerModel.save(update_fields=['is_removed'])

				return json_result(message=u'删除回答成功')
		else:
			return json_params_error(message=u'你尝试删除一个不存在的回答')
	else:
		return json_params_error(message=u'你访问的链接不存在')
	
#问题搜索
@require_http_methods(['POST'])
@login_required
def search_question(request):
	
	currentPage = request.POST.get('page',1)
	searchWord = request.POST.get('search_word',None)
	
	currentPage = int(currentPage)
	
	logger.info({'searchWord':searchWord})

	if searchWord:
		#这里过滤掉富文本标签
		questionModel = QuestionsModel.objects.filter(content__icontains = searchWord,is_removed=0).all()
		if questionModel:
			
			#每页显示条数
			numPage = int(configs.NUM_PAGE)
			start = (currentPage-1)*numPage
			end = start +numPage
			
			#计算出问题总数
			questionCount = questionModel.count()
			
			#计算出总页数
			pageCount = questionCount/numPage
			if questionCount %numPage >0:
				pageCount +=1
			
			#对问题总数进行切片
			questionModel = list(questionModel.values('id','content','author__username','create_time')[start:end])
			
			context = {
				'questions':questionModel,
				'currentPage':currentPage,
				'pageCount':pageCount,
			}
			return json_result(data=context)
		else:
			return json_params_error(message=u'暂无相关的信息')
	else:
		return json_params_error(message=u'请输入搜索关键词')

'''
################     微信端接口结束     ###################
'''

'''
##########################################################
	下面是PC端管理后台接口
################     PC端接口开始     ###################
'''

#研究方法管理、研究进展管理列表
#20180205在研究方法和研究进展改版后已废弃
# @login_required
# def articles_list(request,section_id=1,page=1):
#
# 	try:
# 		sectionId = int(section_id)
# 		currentPage = int(page)
# 	except:
# 		pass
#
# 	logger.info({'sectionId': sectionId, 'currentPage': currentPage})
#
# 	# 文章状态 0：删除 1:发布 2：推荐 3：草稿
# 	if sectionId or currentPage:
# 		sectionModel = SectionModel.objects.filter(pk=sectionId).first()
# 		if sectionModel:
# 			# filter:表示 =  exclude:表示!=
# 			articleModel = ArticleModel.objects.exclude(status=0).filter(section=sectionModel).all()
#
# 			# 每页显示条数
# 			numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
# 			start = (currentPage - 1) * numPage
# 			end = start + numPage
#
# 			# 计算文章总数
# 			articleCount = articleModel.count()
#
# 			# 计算出总页数
# 			pageCount = articleCount / numPage
# 			if articleCount % numPage > 0:
# 				pageCount += 1
#
# 			list_articleModel = list(articleModel.values('id', 'title', 'author__username', 'front_author__username', 'publish_time', 'status'))[start:end]
#
# 			context = {
# 				'articles': list_articleModel,
# 				'currentPage': currentPage,
# 				'pageCount': pageCount,
# 			}
# 			return json_result(data=context)
# 		else:
# 			return json_params_error(message=u'选择的分类不存在!')
# 	else:
# 		return json_params_error(message=u'文章分类/页码错误!')
''''''
# #搜索文章
# 20180205在研究方法和研究进展改版后已废弃
# @require_http_methods(['POST'])
# @login_required
# def search_article(request,section_id=1,page=1):
#
# 	search_keyword = request.POST.get('search_keyword', None)
# 	try:
# 		sectionId = int(section_id)
# 		currentPage = int(page)
# 	except:
# 		pass
#
# 	logger.info({'sectionId':sectionId,'currentPage':currentPage,'search_keyword':search_keyword})
#
# 	if search_keyword:
# 		sectionModel = SectionModel.objects.filter(pk=sectionId).first()
# 		if sectionModel:
# 			articleModel = ArticleModel.objects.exclude(status=0).filter(title__icontains=search_keyword,section=sectionModel).all()
# 			if articleModel:
# 				#每页显示条数
# 				numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
# 				start = (currentPage -1 )*numPage
# 				end = start + numPage
#
# 				#计算出文章总数
# 				articleCount = articleModel.count()
#
# 				#计算出总页数
# 				pageCount = articleCount/numPage
# 				if articleCount %numPage>0:
# 					pageCount +=1
#
# 				list_articleModel = list(articleModel.values('id', 'title', 'author__username', 'front_author__username', 'publish_time','status'))[start:end]
#
# 				context = {
# 					'articles': list_articleModel,
# 					'currentPage': currentPage,
# 					'pageCount': pageCount,
# 				}
# 				return json_result(data=context)
#
# 			else:
# 				return json_params_error(message=u'暂无相关文章!')
# 		else:
# 			return json_params_error(message=u'选择的分类不存在!')
# 	else:
# 		return json_params_error(message=u'搜索的关键词不能为空!')

''''''
#发表文章
#20180205在研究方法和研究进展改版后已废弃
# @require_http_methods(['GET','POST'])
# @login_required
# def publish_article(request):
# 	if request.method =='GET':
# 		return json_result(message=u'发表文章页面')
# 	else:
# 		#获取当前时间
# 		now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#
# 		title = request.POST.get('title',None)
# 		summary = request.POST.get('summary',None)
# 		content = request.POST.get('content',None)
# 		thumbnail = request.POST.get('thumbnail',None)
# 		tags = request.POST.getlist('tags',None)
# 		sectionId = request.POST.get('section_id',1)
# 		publish_time = request.POST.get('publish_time',now_time)
# 		status = request.POST.get('status',3)
#
# 		#将publish_time转换成时间格式
# 		try:
# 			tmp_publish_time = time.strptime(publish_time,"%Y-%m-%d %H:%M:%S")
# 			Y,m,d,H,M,S = tmp_publish_time[0:6]
# 			tmp_time = datetime.datetime(Y,m,d,H,M,S)
# 		except:
# 			pass
#
# 		logger.info({'title':title,'summary':summary,'content':content,'thumbnail':thumbnail,'tags':tags,'sectionId':sectionId,'publish_time':publish_time,'status':status})
#
# 		if title:
# 			if content:
# 				sectionModel = SectionModel.objects.filter(pk = int(sectionId)).first()
# 				if sectionModel:
# 					articleModel = ArticleModel(title=title,summary=summary,content=content,thumbnail=thumbnail,publish_time=tmp_time,author=request.user,section=sectionModel,status=status)
# 					articleModel.save()
# 					if tags:
# 						try:
# 							for t in tags:
# 								#这里用try 是为了解决前台不填写标签时，默认提交过来是一个空字符串，表示list值为真
# 									tagModel = TagsModel.objects.filter(pk = int(t)).first()
# 									if tagModel:
# 										articleModel.tags.add(tagModel)
# 									else:
# 										return json_params_error(message=u'你添加的标签不存在!')
# 						except:pass
#
# 					return json_result(message=u'文章发表成功!')
# 				else:
# 					return json_params_error(message=u'你选择的板块不存在!')
# 			else:
# 				return json_params_error(message=u'文章内容不能为空!')
# 		else:
# 			return json_params_error(message=u'文章标题不能为空!')
''''''
#编辑文章
# 20180205在研究方法和研究进展改版后已废弃
# @require_http_methods(['GET','POST'])
# @login_required
# def edit_article(request,article_id=0):
#
# 	try:
# 		articleId = int(article_id)
# 	except:pass
#
# 	logger.info({'articleId':articleId})
#
# 	if articleId:
# 		articleModel = ArticleModel.objects.exclude(status=0).filter(pk=articleId).first()
# 		tags = articleModel.tags.all()
#
# 		tmp_tags =[]
# 		if tags:
# 			# 将文章对应的标签返回
# 			for t in tags:
# 				#tagModel = TagsModel.objects.filter(pk= t.id).values('id', 'tag')
# 				tmp_tags.append({
# 					'id':t.id,
# 					'tag':t.tag,
# 				})
#
# 		logger.info({'tmp_tags': tmp_tags})
#
# 		if articleModel:
# 			if request.method == 'GET':
# 				context = {
# 					'id': articleModel.id,
# 					'title': articleModel.title,
# 					'summary': articleModel.summary,
# 					'content': articleModel.content,
# 					'thumbnail': articleModel.thumbnail, #responseJSON不接收对象，而ImageField是一个对象，因此需要转成str
# 					'publish_time': articleModel.publish_time,
# 					'section_id': articleModel.section.id,
# 					'tags': tmp_tags,
# 					'status': articleModel.status,
# 				}
# 				return json_result(message=u'查询成功',data=context)
# 			else:
# 				# 获取当前时间
# 				now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#
# 				title = request.POST.get('title', None)
# 				summary = request.POST.get('summary', None)
# 				content = request.POST.get('content', None)
# 				thumbnail = request.POST.get('thumbnail',None)
# 				tags = request.POST.getlist('tags', None)
# 				publish_time = request.POST.get('publish_time', now_time)
# 				status = request.POST.get('status',3)
#
# 				# 将publish_time转换成时间格式
# 				try:
# 					tmp_publish_time = time.strptime(publish_time, "%Y-%m-%d %H:%M:%S")
# 					Y, m, d, H, M, S = tmp_publish_time[0:6]
# 					tmp_time = datetime.datetime(Y, m, d, H, M, S)
# 				except:
# 					pass
#
# 				logger.info({'title': title, 'summary': summary, 'content': content, 'thumbnail': thumbnail, 'tags': tags, 'articleId': articleId, 'publish_time': publish_time, 'status': status})
#
# 				if title:
# 					if content:
# 						articleModel.title = title
# 						articleModel.summary = summary
# 						articleModel.content = content
# 						articleModel.thumbnail = thumbnail
# 						articleModel.publish_time = tmp_time
# 						articleModel.author = request.user
# 						articleModel.status = status
# 						articleModel.save()
# 						if tags:
# 							try:
# 								for t in tags:
# 									tagModel = TagsModel.objects.filter(pk=t).first()
# 									articleModel.tags.add(tagModel)
# 							except:pass
#
# 						return json_result(message=u'文章修改成功')
#
# 					else:
# 						return json_params_error(message=u'文章内容不能为空!')
# 				else:
# 					return json_params_error(message=u'文章标题不能为空!')
# 		else:
# 			return json_params_error(message=u'此文章还未发表')
# 	else:
# 		return json_params_error(message=u'你访问的信息不合法!')

''''''
#删除文章
# 20180205在研究方法和研究进展改版后已废弃
# @require_http_methods(['POST'])
# @login_required
# def delete_article(request):
# 	articleId = request.POST.get('article_id',0)
# 	try:
# 		articleId = int(articleId)
# 	except:pass
#
# 	logger.info({'article_id':articleId})
#
# 	articleModel = ArticleModel.objects.filter(pk = articleId).first()
# 	if articleModel:
# 		articleModel.status = 0
# 		articleModel.save(update_fields=['status'])
# 		return json_result(message=u'文章删除成功!')
# 	else:
# 		return json_params_error(message=u'你尝试删除一篇不存在的文章!')
''''''
#添加标签
# 20180205在研究方法和研究进展改版后已废弃
# @require_http_methods(['GET','POST'])
# @login_required
# def add_tag(request):
# 	if request.method == 'GET':
# 		return json_result(message=u'添加标签页面!')
# 	else:
# 		tag = request.POST.get('tag','') #默认为空字符串，防止字符串方法报错
# 		relevanceTagId = request.POST.get('relevance_tag_id',0)
# 		try:
# 			tag = tag.strip()
# 			relevanceTagId = int(relevanceTagId)
# 		except:pass
#
# 		logger.info({'tag':tag,'relevanceTagId':relevanceTagId})
#
# 		if tag:
# 			tagsModel = TagsModel.objects.filter(tag= tag).first()
# 			if not tagsModel:
# 				if relevanceTagId:
# 					relevanceTagModel = TagsModel.objects.filter(pk =relevanceTagId,relevance_tag=None).first()
# 					if relevanceTagModel:
# 						relevanceTag = TagsModel(tag=tag,grade=2,relevance_tag=relevanceTagModel)
# 						relevanceTag.save()
# 						#添加成功后返回添加的标签属性
# 						tagModel = TagsModel.objects.filter(tag=tag).first()
# 						context = {
# 							'id':tagModel.id,
# 							'tag':tagModel.tag,
# 						}
# 						return json_result(message=u'成功添加二级标签!',data=context)
# 					else:
# 						return json_params_error(message=u'请选择合法的一级标签!')
# 				else:
# 					tagModel = TagsModel(tag=tag,grade=1)
# 					tagModel.save()
# 					# 添加成功后返回添加的标签属性
# 					tagModel = TagsModel.objects.filter(tag=tag).first()
# 					context = {
# 						'id': tagModel.id,
# 						'tag': tagModel.tag,
# 					}
# 					return json_result(message=u'成功添加一级标签!', data=context)
# 			else:
# 				return json_params_error(message=u'该标签已存在!')
# 		else:
# 			return json_params_error(message=u'标签不能为空!')
''''''
#删除标签
# 20180205在研究方法和研究进展改版后已废弃
# @require_http_methods(['POST'])
# @login_required
# def delete_tag(request):
# 	tagId = request.POST.get('tag_id',0)
#
# 	try:
# 		tagId = int(tagId)
# 	except:pass
#
# 	logger.info({'tagId':tagId})
#
# 	if tagId:
# 		tagModel = TagsModel.objects.filter(pk = tagId).first()
# 		if tagModel:
# 			#检查要删除的标签是否有关联的二级标签，如果有则将二级标签删除
# 			relevanceTagModel = TagsModel.objects.filter(relevance_tag= tagModel).all()
# 			if relevanceTagModel:
# 				relevanceTagModel.delete()
# 			tagModel.delete()
# 			return json_result(message=u'成功删除标签!')
# 		else:
# 			return json_params_error(message=u'你尝试删除一个不存在的标签!')
# 	else:
# 		return json_params_error(message=u'删除的标签不能为空!')
''''''
#修改标签
# 20180205在研究方法和研究进展改版后已废弃
# @require_http_methods(['POST'])
# @login_required
# def alter_tag(request):
#
# 	tagId = request.POST.get('tag_id',0)
# 	tag = request.POST.get('tag',None)
# 	try:
# 		tagId = int(tagId)
# 		tag = tag.strip()
# 	except:pass
#
# 	logger.info({'tag': tag, 'tagId':tagId})
#
# 	if tagId:
# 		if tag:
# 			#需要判断提交的标签和现有标签是否重复
# 			repetitionTagModel = TagsModel.objects.filter(tag=tag).first()
# 			if not repetitionTagModel:
# 				tagModel = TagsModel.objects.filter(pk = tagId).first()
# 				if tagModel:
# 					tagModel.tag = tag
# 					tagModel.save()
# 					return json_result(message=u'成功修改标签!')
# 				else:
# 					return json_params_error(message=u'你在尝试修改一个不存在的标签!')
# 			else:
# 				return json_params_error(message=u'该标签已存在!')
# 		else:
# 			return json_params_error(message=u'标签不能为空!')
# 	else:
# 		return json_params_error(message=u'请选择你要修改的标签!')
''''''
# 一级标签
# 20180205在研究方法和研究进展改版后已废弃
# @login_required
# def tag_list(request):
# 	tagsModel = TagsModel.objects.filter(relevance_tag=None).values('id', 'tag')
#
# 	if tagsModel:
# 		context = {
# 			'tags': list(tagsModel),
# 		}
# 		return json_result(message=u'查询成功', data=context)
# 	else:
# 		return json_result(message=u'暂无任何标签!')

#二级标签
# 20180205在研究方法和研究进展改版后已废弃
# @login_required
# def relevance_tag(request,tag_id):
# 	try:
# 		tagId = int(tag_id)
# 	except:
# 		pass
#
# 	tagsModel = TagsModel.objects.filter(relevance_tag=tagId).values('id','tag')
# 	if tagsModel:
# 		context = {
# 			'tags': list(tagsModel),
# 		}
# 		return json_result(message=u'查询成功', data=context)
# 	else:
# 		return json_result(message=u'暂无任何标签!')

# #评论管理
# @login_required
# def comment_list(request,page=1):
# 	commentsModel = CommentModel.objects.filter(status=1).all()
# 	try:
# 		currentPage = int(page)
# 	except:
# 		pass
# 	#定义每页显示评论条数
# 	numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
# 	start = (currentPage-1)*numPage
# 	end = start + numPage
#
# 	#计算评论总数
# 	commentCount = commentsModel.count()
#
# 	#计算总页数
# 	pageCount = commentCount / numPage
# 	if commentCount % numPage >0:
# 		pageCount +=1
#
# 	comment_list = list(commentsModel.values('id', 'author__username', 'comment', 'create_time'))[start:end]
#
# 	if commentsModel:
# 		context = {
# 			'comments': comment_list,
# 			'pageCount':pageCount,
# 			'currentPage':currentPage,
# 		}
# 		return json_result(message=u'查询成功',data=context)
# 	else:
# 		return json_result(message=u'暂无任何评论!')
#
# #删除评论
# @require_http_methods(['POST'])
# @login_required
# def delete_comment(request):
# 	commentId = request.POST.get('comment_id')
# 	try:
# 		commentId = int(commentId)
# 	except:pass
#
# 	logger.info({'commentId':commentId})
#
# 	if commentId:
# 		commentModel = CommentModel.objects.filter(status=1,pk= commentId).first()
# 		# 如果要删除的评论存在，那么就判断是否有关联的二级评论? 如果有,就把关联的二级评论状态status=0。没有就直接修改状态
# 		if commentModel:
# 			relevanceCommentModel = CommentModel.objects.filter(status=1,relevance_comment=commentModel).all()
# 			if relevanceCommentModel:
# 				#因为是删除多条，多条数据是没有save属性的，因此需要用到update更新
# 				relevanceCommentModel.update(status=0)
# 			commentModel.status = 0
# 			commentModel.save(update_fields=['status'])
# 			return json_result(message=u'成功删除评论!')
#
# 		else:
# 			return json_params_error(message=u'你尝试删除一个不存在的评论!')
# 	else:
# 		return json_params_error(message=u'请确认你输入的信息合法!')

#搜索评论
@require_http_methods(['POST'])
@login_required
def search_comment(request,page=1):

	searchComment = request.POST.get('search_comment',None)
	try:
		currentPage = int(page)
	except:
		pass

	logger.info({ 'searchComment': search_comment})

	if search_comment:
		commentModel = CommentModel.objects.filter(comment__icontains = searchComment,status=1).all()
		if commentModel:
			# 每页显示条数
			numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
			start = (currentPage - 1) * numPage
			end = start + numPage

			# 计算出文章总数
			commentCount = commentModel.count()

			# 计算出总页数
			pageCount = commentCount / numPage
			if commentCount % numPage > 0:
				pageCount += 1

			list_commentModel = list(commentModel.values('id', 'author__username','comment','create_time','status'))[start:end]

			context = {
				'comments': list_commentModel,
				'currentPage': currentPage,
				'pageCount': pageCount,
			}
			return json_result(message=u'查询成功!',data=context)

		else:
			return json_params_error(message=u'暂无相关评论!')
	else:
		return json_params_error(message=u'搜索的关键词不能为空!')

'''
################     PC端接口结束     ###################
'''

'''
################     微信自定义菜单接口开始     ###################
'''

#添加微信自定义菜单分类
@require_http_methods(['GET','POST'])
@login_required
def add_category(request):
	if request.method == 'GET':
		return json_result(message=u'这里是添加微信自定义菜单分类页面!')
	else:
		category = request.POST.get('category',None)
		summary = request.POST.get('summary',None)

		try:
			category = str(category).strip()
		except:
			pass

		if category:
			articleCategoryMenuModel = ArticleCategoryMenuModel.objects.filter(category=category).first()
			if not articleCategoryMenuModel:
				addCategoryModel = ArticleCategoryMenuModel(category=category,summary=summary)
				addCategoryModel.save()
				return json_result(message=u'添加分类成功!')
			else:
				return json_params_error(message=u'此分类已存在!')
		else:
			return json_params_error(message=u'分类不能为空!')

#修改微信自定义菜单分类和摘要
@require_http_methods(['GET','POST'])
@login_required
def alter_category(request,category_id=0):
	try:
		categoryId = int(category_id)
	except:pass

	if categoryId:
		articleCategoryMenuModel = ArticleCategoryMenuModel.objects.filter(pk=categoryId).first()
		if articleCategoryMenuModel:
			if request.method == 'GET':
					context = {
						'id':articleCategoryMenuModel.id,
						'category':articleCategoryMenuModel.category,
						'summary':articleCategoryMenuModel.summary,
					}
					return json_result(data=context)

			else:
				category = request.POST.get('category',articleCategoryMenuModel.category)
				summary = request.POST.get('summary', articleCategoryMenuModel.summary)

				try:
					category = str(category).strip()
					summary = str(summary).strip()
				except:
					pass

				if category:
					#判断提交的分类信息是否重复
					tmp_category = ArticleCategoryMenuModel.objects.filter(category=category).first()
					if tmp_category:
						if tmp_category.id != articleCategoryMenuModel.id:
							return json_params_error(message=u'此分类已存在!')

					articleCategoryMenuModel.category = category
					articleCategoryMenuModel.summary = summary
					articleCategoryMenuModel.save()
					return json_result(message=u'成功修改分类信息')
				else:
					return json_params_error(message=u'分类不能为空!')
		else:
			return json_params_error(message=u'你尝试访问一个不存在的分类信息!')
	else:
		return json_params_error(message=u'你尝试查看一个不存在的分类!')

#删除菜单分类
@login_required
def delete_category(request,category_id=0):
	try:
		categoryId = int(category_id)
	except:pass
	if categoryId:
		articleCategoryMenuModel = ArticleCategoryMenuModel.objects.filter(pk = categoryId).first()
		if articleCategoryMenuModel:
			articleCategoryMenuModel.delete()
			return json_result(message=u'成功删除分类信息!')
		else:
			return json_params_error(message=u'你尝试删除一个不存在的分类!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的分类!')

#微信自定义菜单分类列表
@login_required
def article_category_list(request):
	articleCategoryMenumModel = ArticleCategoryMenuModel.objects.values('id','category','summary')
	context = {
		'article_category_list':list(articleCategoryMenumModel),
	}
	return json_result(data=context)

#添加文章索引
@require_http_methods(['GET','POST'])
@login_required
def add_article_index(request):
	if request.method == 'GET':
		return json_result(message=u'这里是微信自定义菜单添加文章索引页面!')
	else:
		title = request.POST.get('title',None)
		categoryId = request.POST.get('category_id',None)
		index = request.POST.get('index',None)

		try:
			categoryId = int(categoryId)
		except:pass

		if title:
			if categoryId:
				articleCategoryMenuModel = ArticleCategoryMenuModel.objects.filter(pk = categoryId).first()
				if articleCategoryMenuModel:
					articleIndexModel = ArticleIndexModel(title=title,category=articleCategoryMenuModel,index=index)
					articleIndexModel.save()
					return json_result(message=u'成功添加文章索引!')
				else:
					return json_params_error(message=u'你尝试选择一个不存在的分类信息!')
			return json_params_error(message=u'请选择分类!')
		else:
			return json_params_error(message=u'文章标题不能为空!')

#修改文章索引
@require_http_methods(['GET','POST'])
@login_required()
def alter_article_index(request,article_id=0):
	try:
		articleId = int(article_id)
	except:pass

	if request.method == 'GET':
		articleIndexModel = ArticleIndexModel.objects.filter(pk = articleId).first()
		if articleIndexModel:
			context = {
				'id':articleIndexModel.id,
				'title':articleIndexModel.title,
				'category_id':articleIndexModel.category.id,
				'category_name':articleIndexModel.category.category,
				'index':articleIndexModel.index,
			}
			return json_result(data=context)
		else:
			return json_params_error(message=u'你尝试访问一个不存在的文章索引信息!')
	else:
		title = request.POST.get('title',None)
		categoryId = request.POST.get('category_id',None)
		index = request.POST.get('index',None)

		try:
			categoryId = int(categoryId)
		except:pass

		if title:
			if categoryId:
				articleCategoryMenuModel = ArticleCategoryMenuModel.objects.filter(pk=categoryId).first()
				if articleCategoryMenuModel:
					articleIndexModel = ArticleIndexModel.objects.filter(pk= articleId).first()
					if articleIndexModel:
						articleIndexModel.title = title
						articleIndexModel.category = articleCategoryMenuModel
						articleIndexModel.index = index
						articleIndexModel.save()
						return json_result(message=u'成功修改文章索引信息!')
				else:
					return json_params_error(message=u'你尝试选择一个不存在的分类信息!')
			return json_params_error(message=u'请选择分类!')
		else:
			return json_params_error(message=u'文章标题不能为空!')

#删除文章索引
@login_required
def delete_article_index(request,article_id=0):
	try:
		articleId = int(article_id)
	except:pass

	if articleId:
		articleIndexModel = ArticleIndexModel.objects.filter(pk=articleId).first()
		if articleIndexModel:
			articleIndexModel.delete()
			return json_result(message=u'成功删除文章索引!')
		else:
			return json_params_error(message=u'你尝试删除一个不存在的文章索引信息!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的文章索引信息!')

#文章索引列表
@login_required
def article_index_list(request,page=1):
	try:
		currentPage = int(page)
	except:
		pass

	articleIndexModel = ArticleIndexModel.objects.all()

	if articleIndexModel:

		numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
		start = (currentPage - 1) * numPage
		end = start + numPage

		#计算文章索引总页数
		articleIndexCount = articleIndexModel.count()
		pageCount = articleIndexCount /numPage
		if articleIndexCount %numPage>0:
			pageCount +=1

		articleIndexModel = list(articleIndexModel.values('id', 'title', 'category__category', 'index'))[start:end]

		context = {
			'article_index_list':articleIndexModel,
			'currentPage':currentPage,
			'pageCount':pageCount,
		}
		return json_result(data=context)
	else:
		return json_result(message=u'暂无文章索引!')

#搜索文章索引
@require_http_methods(['GET','POST'])
@login_required
def search_article_index(request,page=1):
	try:
		currentPage = int(page)
	except:
		pass

	if request.method == 'GET':
		return json_result(message=u'这里是搜索文章索引信息页面!')
	else:
		searchArticleIndex = request.POST.get('search_article_index',None)
		if searchArticleIndex:

			articleIndexModel = ArticleIndexModel.objects.filter(title__icontains=searchArticleIndex).all()

			numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
			start = (currentPage - 1) * numPage
			end = start + numPage

			# 计算文章索引总页数
			articleIndexCount = articleIndexModel.count()
			pageCount = articleIndexCount / numPage
			if articleIndexCount % numPage > 0:
				pageCount += 1

			articleIndexModel = list(articleIndexModel.values('id', 'title', 'category__category', 'index'))[start:end]

			context = {
				'article_index_list': articleIndexModel,
				'currentPage': currentPage,
				'pageCount': pageCount,
			}
			return json_result(data=context)
		else:
			return json_params_error(message=u'关键词不能为空!')

'''
################     微信自定义菜单接口结束    ###################
'''

'''
	date: 20170816
	author: zhangx
	mark:
		PC版中问答板块管理
'''

#添加问答分类和摘要
@require_http_methods(['GET','POST'])
@login_required
def add_question_category(request):
	if request.method == 'GET':
		return json_result(message=u'问答板块添加问题分类页面!')
	else:
		category = request.POST.get('category',None)
		#summary = request.POST.get('summary',None)

		logger.info({'category':category})

		try:
			category = str(category).strip()
		except:pass

		if category:
			questionCategoryModel = QuestionCategoryModel.objects.filter(category=category).first()
			if not questionCategoryModel:
				addQuestionCategoryModel = QuestionCategoryModel(category=category)
				addQuestionCategoryModel.save()
				categoryId = QuestionCategoryModel.objects.filter(category=category).first()
				return json_result(message=u'成功添加问题分类!',data={'category_id':categoryId.id})
			else:
				return json_params_error(message=u'此问题分类已存在!')
		else:
			return json_params_error(message=u'分类名称不能为空!')

#编辑问题分类和摘要
@login_required
@require_http_methods(['GET','POST'])
def alter_question_and_answer_category(request,category_id=0):
	try:
		categoryId = int(category_id)
	except:pass

	logger.info({'category_id':categoryId})

	if categoryId:
		questionCategoryModel = QuestionCategoryModel.objects.filter(pk = categoryId).first()
		if questionCategoryModel:
			if request.method == 'GET':
				context = {
					'id':questionCategoryModel.id,
					'category':questionCategoryModel.category,
					'summary':questionCategoryModel.summary,
				}
				return json_result(data=context)
			else:
				category = request.POST.get('category',questionCategoryModel.category)
				summary = request.POST.get('summary',questionCategoryModel.summary)

				logger.info({'category_id':categoryId,'category':category,'summary':summary})

				try:
					catetory = str(category).strip()
				except:pass

				if catetory:
					alterQuestionCategoryModel = QuestionCategoryModel.objects.filter(category=category).first()
					if alterQuestionCategoryModel:
						if alterQuestionCategoryModel.id != questionCategoryModel.id:
							return json_params_error(message=u'此问题分类已存在!')
					alterQuestionCategoryModel.catetory = catetory
					alterQuestionCategoryModel.summary = summary
					alterQuestionCategoryModel.save()
					return json_result(message=u'成功修改问题分类信息!')
				else:
					return json_params_error(message=u'分类名称不能为空!')
		else:
			return json_params_error(message=u'你尝试访问一个不存在的分类信息!')
	else:
		return json_params_error(message=u'你尝试修改一个不存在的分类!')

#问答分类删除
@login_required
def delete_question_category(request,question_category_id=0):
	try:
		questionCategoryId = int(question_category_id)
	except:pass

	logger.info({'question_category_id':questionCategoryId})

	if questionCategoryId:
		questionCategoryModel = QuestionCategoryModel.objects.filter(pk=questionCategoryId).first()
		if questionCategoryModel:
			questionCategoryModel.delete()
			return json_result(message=u'成功删除问题分类!')
		else:
			return json_params_error(message=u'你尝试删除一个不存在的分类!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的分类!')

#问答分类列表展示
@login_required
def question_category_list(request):
	questionCategoryListModel = list(QuestionCategoryModel.objects.values('id', 'category', 'summary'))

	if questionCategoryListModel:
		context = {
			'question_category_list':questionCategoryListModel,
		}
		return json_result(data=context)
	else:
		return json_result(message=u'暂无问答分类信息!')

#修改问题
@login_required
@require_http_methods(['GET','POST'])
def alter_question(request,question_id):
	try:
		questionId = int(question_id)
	except:pass

	logger.info({'question_id':questionId})

	if questionId:
		questionModel = QuestionsModel.objects.filter(pk = questionId,is_removed=0).first()
		if questionModel:
			if request.method == 'GET':
				context = {
					'id':questionModel.id,
					'content':questionModel.content,
				}
				return json_result(data=context)
			else:
				content = request.POST.get('content',questionModel.content)

				logger.info({'question_id':questionId,'content':content})

				try:
					content = str(content).strip()
				except:pass
				if content:
					questionModel.content = content
					questionModel.save(update_fields =['content'])
					return json_result(message=u'问题修改成功!')
				else:
					return json_params_error(message=u'问题不能为空!')
		else:
			return json_params_error(message=u'你尝试修改一个不存在的问题!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的问题!')

#修改问题分类
@login_required
def alter_question_category(request,question_id=0,question_category_id=0):
	try:
		questionId = int(question_id)
		questionCategoryId = int(question_category_id)
	except:pass

	logger.info({'question_id':questionId,'question_category_id':questionCategoryId})

	if questionId:
		if questionCategoryId:
			questionModel = QuestionsModel.objects.filter(pk=questionId,is_removed=0).first()
			if questionModel:
				questionCategoryModel = QuestionCategoryModel.objects.filter(pk=questionCategoryId).first()
				if questionCategoryModel:
					questionModel.category = questionCategoryModel
					questionModel.save(update_fields=['category'])
					return json_result(message=u'成功修改问题分类!')
				else:
					return json_params_error(message=u'你选择的分类不存在!')
			else:
				return json_params_error(message=u'你尝试修改一个不存在的问题分类!')
		else:
			return json_params_error(message=u'问题分类不能为空!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的问题!')

#修改问题的回答
@login_required
@require_http_methods(['GET','POST'])
def alter_answer(request,answer_id=0):
	try:
		answerId = int(answer_id)
	except:pass

	logger.info({'answer_id':answerId})

	if answerId:
		answerModel = AnswersModel.objects.filter(pk = answerId,is_removed=0).first()
		if answerModel:
			if request.method == 'GET':
				context = {
					'id':answerModel.id,
					'comment':answerModel.comment,
				}
				return json_result(data=context)
			else:
				comment = request.POST.get('comment',answerModel.comment)

				logger.info({'answer_id': answerId,'comment':comment})

				try:
					comment = str(comment).strip()
				except:pass

				if comment:
					answerModel.comment = comment
					answerModel.save(update_fields=['comment'])
					return json_result(message=u'成功修改回答内容!')
				else:
					return json_params_error(message=u'回答的内容不能为空!')
		else:
			return json_params_error(message=u'你尝试修改一个不存在的回答!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的回答!')


'''
	author : zhangx
	date : 20171130
	mark :
		1、增加资源分发批量发送邮件功能。

		2、用户在阅读微信文章的时候若想获取原文资源，则需要通过注册，注册成功后才会发送文章原文。
		3、若用户已经注册,则直接点击获取资源。
		4、后台统一对资源进行下发
'''
#申请文章资源的用户列表
@login_required
def get_resource_user_list(request,page=1,is_send=0):
	try:
		currentPage = int(page)
		isSend = int(is_send)
	except:pass

	numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
	start = (currentPage-1)* numPage
	end = start + numPage

	if isSend:
		if isSend in [1,2]:
			getResourceModel = GetResourceModel.objects.filter(is_send=isSend).all()
		else:
			return json_params_error(message=u'你尝试查看一个不存在的发送分类!')
	else:
		getResourceModel = GetResourceModel.objects.all()

	if getResourceModel:
		resourceCount = getResourceModel.count()

		pageCount = resourceCount / numPage
		if resourceCount % numPage > 0:
			pageCount += 1

		user_info = []
		for r in getResourceModel:
			user_info.append({
				'email':r.username.email,
				'username':r.username.username,
				'article_id':r.article_id.id,
				'is_send':r.is_send,
			})

		context = {
			'user_list':user_info[start:end],
			'current_page':currentPage,
			'page_count':pageCount,
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无用户申请资源!')

#发送资源
@login_required
@require_http_methods(['GET','POST'])
def send_resource(request):
	if request.method == 'GET':
		return json_result(message=u'发送资源页面')
	else:
		emailList = request.POST.getlist('email_list',None)
		#subject = request.POST.get('subject',None)
		body = request.POST.get('body',None)
		filePath = request.FILES.get('file_path',None)

		# emailList 表单提交过来的list 是一个unicode,需要分割
		emailList = emailList[0].split(',')

		logger.info({'email_list':emailList,'body':body,'file_path':filePath})

		if send_attach_email(request, email_list=emailList, body=body, file_path=filePath):
		#遍历邮箱修改用户的发送状态
			for e in emailList:
				getResourceModel = GetResourceModel.objects.filter(username__email=e).first()
				if getResourceModel:
					getResourceModel.is_send = 2
					getResourceModel.save()
				else:
					return json_params_error(message=u'此用户没有申请资源!')
			return json_result(message=u'邮件发送成功!')
		else:
			return json_params_error(message=u'邮件发送失败!')

#资源分发页面的搜索
@login_required
@require_http_methods(['GET','POST'])
def search_get_resource(request,page=1):
	try:
		currentPage = int(page)
	except:
		pass

	if request.method == 'GET':
		return json_result(message=u'资源分发的搜索页面!')
	else:
		searchResourceInfo = request.POST.get('search_resource_info',None)

		numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
		start = (currentPage - 1) * numPage
		end = start + numPage

		if searchResourceInfo:
			searchResourceInfoModel = GetResourceModel.objects.filter(Q(username__email__icontains=searchResourceInfo)|Q(username__username__icontains=searchResourceInfo)|Q(article_id__pk__icontains=searchResourceInfo)).all()
			if searchResourceInfoModel:
				resourceCount = searchResourceInfoModel.count()
				pageCount = resourceCount /numPage
				if resourceCount % numPage>0:
					pageCount +=1

				user_info = []
				for r in searchResourceInfoModel:
					user_info.append({
						'email': r.username.email,
						'username': r.username.username,
						'article_id': r.article_id.id,
						'is_send': r.is_send,
					})
				context = {
					'user_list': user_info[start:end],
					'current_page': currentPage,
					'page_count': pageCount,
				}
				return json_result(data=context)
			else:
				return json_params_error(message=u'暂无相关信息!')
		else:
			return json_params_error(message=u'请输入搜索关键词!')

#资源申请信息邮件发送状态设置
@login_required
@require_http_methods(['GET','POST'])
def is_send_resource(request):

	if request.method == 'GET':
		return json_result(message=u'设置资源申请信息邮件发送状态页面!')
	else:
		email = request.POST.get('email',None)
		articleId = request.POST.get('article_id',None)
		isSend = request.POST.get('is_send',None)

		try:
			isSend = int(isSend)
			articleId = int(articleId)
		except:
			pass

		if email:
			if articleId:
				articleIndexModel = ArticleIndexModel.objects.filter(pk = articleId).first()
				if articleIndexModel:
					if isSend in [1,2]:
						getResourceModel = GetResourceModel.objects.filter(username__email=email,article_id=articleIndexModel).first()
						if getResourceModel:
							getResourceModel.is_send = isSend
							getResourceModel.save()
							return json_result(message=u'设置成功!',data=getResourceModel.is_send)
						else:
							return json_params_error(message=u'此用户没有申请资源!')
					else:
						return json_params_error(message=u'你尝试将资源申请信息设置为不存在的状态!')
				else:
					return json_params_error(message=u'你尝试查看一个不存在的文章资源!')
			else:
				return json_params_error(message=u'申请资源的文章信息不能为空!')
		else:
			return json_params_error(message=u'你尝试标注一个不存在的资源申请信息!')

'''
	author: zhangx
	date：20171206
	mark:
		1、研究方法3.0版本
		2、不提供删除分类功能，删除分类会引发文章缺少分类报错
'''

#添加研究方法分类
@login_required
@require_http_methods(['GET','POST'])
def add_method_category(request):
	if request.method == 'GET':
		return json_result(message=u'添加研究方法分类页面!')
	else:
		category = request.POST.get('category',None)
		relevanceCategoryId = request.POST.get('relevance_category_id',0)
		column = request.POST.get('column',None) #用户区分当前分类展示到哪一列,前台文章分类排序特性需求
		isActive = request.POST.get('is_active',1)

		try:
			relevanceCategoryId = int(relevanceCategoryId)
			isActive = int(isActive)
		except:pass

		if category:
			# methodCategoryModel = MethodCategoryModel.objects.filter(category=category).first()
			# if methodCategoryModel:
			# 	return json_params_error(message=u'此分类已存在!')
			# else:
			if relevanceCategoryId:

				relevanceCategoryModel = MethodCategoryModel.objects.filter(pk = relevanceCategoryId).first()
				if relevanceCategoryModel:
					#将子分类的type值，设置和父分类相同
					addMethodCategoryModel = MethodCategoryModel(category=category,relevance_category=relevanceCategoryModel, is_active=isActive, column=column,type=relevanceCategoryModel.type)
					addMethodCategoryModel.save()

					#设置分类的默认排序值
					addMethodCategoryModel.rank = addMethodCategoryModel.id
					addMethodCategoryModel.save(update_fields=['rank'])

					return json_result(message=u'成功添加2级分类!')
				else:
					return json_params_error(message=u'你尝试关联一个不存在的分类!')
			else:
				addMethodCategoryModel = MethodCategoryModel(category=category, is_active=isActive,column=column)
				addMethodCategoryModel.save()

				# 设置分类的默认排序值
				addMethodCategoryModel.rank = addMethodCategoryModel.id
				addMethodCategoryModel.save(update_fields=['rank'])
				return json_result(message=u'成功添加分类!')
		else:
			return json_params_error(message=u'请填写分类名称!')

#修改研究方法分类
@login_required
def alter_method_category(request,category_id=0):
	try:
		categoryId = int(category_id)
	except:pass

	if categoryId:
		methodCategoryModel = MethodCategoryModel.objects.filter(pk = categoryId).first()
		if methodCategoryModel:
			if request.method == 'GET':
				context = {
					'id':methodCategoryModel.id,
					'category':methodCategoryModel.category
				}
				return json_result(data=context)
			else:
				category = request.POST.get('category',methodCategoryModel.category)
				isActive = request.POST.get('is_active',methodCategoryModel.is_active)
				column = request.POST.get('column',methodCategoryModel.column)

				if category:
					# #检查分类是否重复
					# repeatMethodCategoryModel = MethodCategoryModel.objects.filter(category=category).first()
					# if repeatMethodCategoryModel:
					# 	if repeatMethodCategoryModel !=methodCategoryModel:
					# 		return json_params_error(message=u'此分类已存在!')

					methodCategoryModel.category = category
					methodCategoryModel.is_active = isActive
					methodCategoryModel.column = column

					methodCategoryModel.save()
					return json_result(message=u'成功修改分类!')
				else:
					return json_params_error(message=u'请填写分类名称!')
		else:
			return json_params_error(message=u'你尝试访问一个不存在的分类!')
	else:
		return json_params_error(message=u'你尝试查看一个不存在的分类!')

#给研究方法分类上传banner图
@require_http_methods(['GET','POST'])
def add_method_category_banner(request,category_id=0):
	'''
		author:zhangx
		date:20180330
		mark:
			1、给研究方法分类增加banner图和链接,供webapp使用
	'''
	try:
		categoryId = int(category_id)
	except:
		pass

	if request.method == 'GET':
		return json_result(message=u'研究方法分类上传banner图接口!')
	else:
		link = request.POST.get('link',None)
		banner = request.POST.get('banner',None)

		if categoryId:
			methodCategoryModel = MethodCategoryModel.objects.filter(pk=categoryId).first()
			if methodCategoryModel:
				methodCategoryModel.link = link
				methodCategoryModel.banner = banner
				methodCategoryModel.save()
				return json_result(message=u'上传banner图成功!')
			else:
				return json_params_error(message=u'你尝试访问一个不存在的分类!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的分类!')

#删除研究方法分类banner和链接
def delete_method_category_banner(request,category_id=0):
	try:
		categoryId = int(category_id)
	except:
		pass
	if categoryId:
		methodCategoryModel = MethodCategoryModel.objects.filter(pk=categoryId).first()
		if methodCategoryModel:
			methodCategoryModel.banner = None
			methodCategoryModel.link = None
			methodCategoryModel.save()
			return json_result(message=u'成功删除banner图和链接!')
		else:
			return json_params_error(message=u'你尝试访问一个不存在的分类!')
	else:
		return json_params_error(message=u'你尝试查看一个不存在的分类!')

#研究方法分类列表
@login_required
def method_category_list(request,category_is_active=1):
	try:
		categoryIsActive = int(category_is_active)
	except:pass
	if categoryIsActive:
		methodCategoryModel = MethodCategoryModel.objects.filter(relevance_category=None,is_active=1).all().order_by('rank','-create_time')
	else:
		methodCategoryModel = MethodCategoryModel.objects.filter(relevance_category=None).all().order_by('rank', '-create_time')

	if methodCategoryModel:
		category_info = []
		for m in methodCategoryModel:
			relevanceCategoryModel = MethodCategoryModel.objects.filter(relevance_category=m).all()
			#如果关联的分类为真,表示有2级分类
			if relevanceCategoryModel:
				relevance_category_list = relevanceCategoryModel.values('id','category','column','is_active','create_time','rank').order_by('rank','-create_time')

				category_info.append({
					'id':m.id,
					'category':m.category,
					'relevance_category': list(relevance_category_list),
					'is_active':m.is_active,
					'create_time':m.create_time,
					'rank':m.rank,
					'banner': m.banner,
				})
			else:
				category_info.append({
					'id': m.id,
					'category': m.category,
					'relevance_category': None,
					'is_active': m.is_active,
					'create_time': m.create_time,
					'rank': m.rank,
					'banner':m.banner,
				})
		context = {
			'category_list':category_info,
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无分类!')

#添加研究方法文章标题和属性
@login_required
def add_method_article_info(request):
	'''
		author:zhangx
		date:20180123
		mark:
			1、研究方法有个专题，属于更多教程
			2、因此若将文章分类划分到更多教程中,则属于专题类文章
			3、划分到更多教程的规则是文章分类id为13(生产环境id=13)。
	'''
	if request.method == 'GET':
		return json_result(message=u'添加研究方法文章信息页面!')
	else:
		# 获取当前时间
		now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

		title = request.POST.get('title',None)
		summary = request.POST.get('summary',None)
		thumbnail = request.POST.get('thumbnail',None)
		app_thumbnail = request.POST.get('app_thumbnail',None)
		categoryId = request.POST.get('category_id',None)
		rank = request.POST.get('rank',None)
		status = request.POST.get('status',3)
		fileName = request.POST.get('file_name',None)
		createTime = request.POST.get('create_time',now_time)

		# 将createTime转换成时间格式
		try:
			tmp_create_time = time.strptime(createTime,"%Y-%m-%d %H:%M:%S") #strptime 根据指定格式将字符串解析成时间元祖
			Y,m,d,H,M,S = tmp_create_time[0:6]

			tmp_time = datetime.datetime(Y,m,d,H,M,S)

			rank = int(rank)
			status = int(status)
		except:pass


		logger.info({
			'title':title,
			'summary':summary,
			'thumbail':thumbnail,
			'app_thumbnail':app_thumbnail,
			'category_id':categoryId,
			'rank':rank,
			'status':status,
			'fileName':fileName,
			'create_time':createTime,
		})

		if rank:
			if rank not in [1,2,3]:
				return json_params_error(message=u'你尝试选择一个不存在的级别!')

		if status not in [0,1,2,3]:
			return json_params_error(message=u'你尝试选择一个不存在的状态!')

		if title:
			if categoryId:
				methodCategoryModel = MethodCategoryModel.objects.filter(pk=categoryId).first()
				if methodCategoryModel:
					methodArticleInfoModel = MethodArticleInfoModel(title=title,summary=summary,thumbnail=thumbnail,app_thumbnail=app_thumbnail,author=request.user,category=methodCategoryModel,rank=rank,status=status,file_name=fileName,create_time=tmp_time)
					methodArticleInfoModel.save()
				else:
					return json_params_error(message=u'你尝试选择一个不存在的分类!')
			else:
				return json_params_error(message=u'文章分类不能为空!')
		else:
			return json_params_error(message=u'文章标题不能为空!')

		# 如果文章状态为推荐,则需要给自定义排序字段设置默认值。把arrange属性在文章信息保存后再存储是因为防止在添加文章时候当文章状态为推荐,但是没有文章id的问题
		if methodArticleInfoModel.status == 2:
			methodArticleInfoModel.arrange = methodArticleInfoModel.id
			methodArticleInfoModel.save()
		#根据业务需求，文章发布成功后需要进入下一页面添加文章 内容,在文章内容页面需要将文章标题和属性信息展示，因此需要添加文章成功后将添加的信息返回
		if methodArticleInfoModel.thumbnail:
			thumbnail = os.path.join(settings.BASE_DIR, 'images/article_images/%s')% methodArticleInfoModel.thumbnail
		else:
			thumbnail = None

		if methodArticleInfoModel.app_thumbnail:
			app_thumbnail = os.path.join(settings.BASE_DIR, 'images/article_images/%s') % methodArticleInfoModel.app_thumbnail
		else:
			app_thumbnail = None

		if methodArticleInfoModel.category:
			category = methodArticleInfoModel.category.category
		else:
			category = None

		if methodArticleInfoModel.file_name:
			file_name = os.path.join(settings.BASE_DIR,'media/article/%s')%methodArticleInfoModel.file_name
		else:
			file_name = None

		context = {
			'id': methodArticleInfoModel.id,
			'title':methodArticleInfoModel.title,
			'summary':methodArticleInfoModel.summary,
			'thumbnail':thumbnail,
			'app_thumbnail': app_thumbnail,
			'category':category,
			'rank': methodArticleInfoModel.rank,
			'status':methodArticleInfoModel.status,
			'file_name':file_name,
			'create_time':methodArticleInfoModel.create_time,
		}
		return json_result(message=u'文章发布成功!',data=context)

#修改研究方法文章标题和属性
@login_required
def alter_method_article(request,article_id=0):
	'''
		由于文章是由版块构成,因此把文章内容由接口单独修改
	'''
	try:
		articleId = int(article_id)
	except:pass

	if articleId:
		methodArticleModel = MethodArticleInfoModel.objects.filter(pk=articleId).exclude(status=0).first()
		if methodArticleModel:

			if methodArticleModel.category:
				category = methodArticleModel.category.category
				categoryId = methodArticleModel.category.id
			else:
				category = None

			#获取文章关联的内容
			methodArticleContentModel = MethodArticleContentModel.objects.filter(article=methodArticleModel).all()
			content_list = []
			if methodArticleContentModel:
				for m in methodArticleContentModel:
					content_list.append({
						'section':m.section.section,
						'section_id':m.section.id,
						'content':m.content,
						'is_login':m.is_login,
						'rank':m.rank,
						'content_id':m.id,
					})

			if request.method == 'GET':

				context = {
					'id': methodArticleModel.id,
					'title': methodArticleModel.title,
					'summary': methodArticleModel.summary,
					'thumbnail': methodArticleModel.thumbnail,
					'app_thumbnail':methodArticleModel.app_thumbnail,
					'category': category,
					'category_id':categoryId,
					'rank': methodArticleModel.rank,
					'status': methodArticleModel.status,
					'file_name': methodArticleModel.file_name,
					'create_time': methodArticleModel.create_time,
					'content':content_list,
				}
				return json_result(data=context)
			else:
				# 获取当前时间
				now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

				title = request.POST.get('title', methodArticleModel.title)
				summary = request.POST.get('summary', methodArticleModel.summary)
				thumbnail = request.POST.get('thumbnail', methodArticleModel.thumbnail)
				app_thumbnail = request.POST.get('app_thumbnail',methodArticleModel.app_thumbnail)
				rank = request.POST.get('rank', methodArticleModel.rank)
				status = request.POST.get('status', methodArticleModel.status)
				fileName = request.POST.get('file_name', methodArticleModel.file_name)
				createTime = request.POST.get('create_time', methodArticleModel.create_time)
				categoryId = request.POST.get('category_id',methodArticleModel.category.id)

				logger.info(request.POST)

				try:
					rank = int(rank)
					status = int(status)

					tmp_create_time = time.strptime(createTime,"%Y-%m-%d %H:%M:%S")
					Y,m,d,H,M,S = tmp_create_time[0:6]
					tmp_time = datetime.datetime(Y,m,d,H,M,S)

				except:pass

				if rank:
					if rank not in [1,2,3]:
						return json_params_error(message=u'你尝试选择一个不存在的文章级别!')

				if status not in [0,1,2,3]:
					return json_params_error(message=u'你尝试选择一个不存在的文章状态!')

				if categoryId:
					methodCategoryModel = MethodCategoryModel.objects.filter(pk=categoryId).first()
					if methodCategoryModel:
						methodArticleModel.category = methodCategoryModel
					else:
						return json_params_error(message=u'你尝试选择一个不存在的分类!')
				else:
					return json_params_error(message=u'文章分类不能为空!')

				methodArticleModel.title = title
				methodArticleModel.summary = summary
				methodArticleModel.thumbnail = thumbnail
				methodArticleModel.app_thumbnail = app_thumbnail
				methodArticleModel.rank = rank
				methodArticleModel.status = status
				methodArticleModel.file_name = fileName
				methodArticleModel.create_time = tmp_time
				methodArticleModel.save()

				# 如果文章状态为推荐,则将自定义排序字段值设置为当前文章的id。否则，则将arrange置为None。
				if methodArticleModel.status == 2:
					methodArticleModel.arrange = methodArticleModel.id
				else:
					methodArticleModel.arrange = None
				methodArticleModel.save(update_fields=['arrange'])

				return json_result(message=u'修改文章属性信息成功!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的文章!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的文章!')

#删除研究方法文章
@login_required
def delete_method_article(request,article_id=0):
	try:
		articleId = int(article_id)
	except:pass
	if articleId:
		methodArticleModel = MethodArticleInfoModel.objects.filter(pk = articleId,status__in=[1,2,3]).first()
		if methodArticleModel:
			methodArticleModel.status = 0
			methodArticleModel.save(update_fields=['status'])
			return json_result(message=u'成功删除文章!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的文章!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的文章!')

#添加研究方法文章内容
@login_required
def add_method_article_content(request):
	if request.method == 'GET':
		return json_result(message=u'添加研究方法内容页面')
	else:
		articleId = request.POST.get('article_id', 0)
		content = request.POST.get('content', None)
		articleContentSectionId = request.POST.get('article_content_section_id', 0)
		rank = request.POST.get('rank', 1)
		isLogin = request.POST.get('is_login', 0)

		try:
			articleId = int(articleId)
			articleContentSectionId = int(articleContentSectionId)
			rank = int(rank)
			isLogin = int(isLogin)
		except:
			pass

		logger.info({'article_id': articleId, 'article_content_section_id': articleContentSectionId, 'rank': rank, 'content': content})

		if articleId:
			methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=articleId, status__in=[1, 2, 3]).first()
			if methodArticleInfoModel:
				if articleContentSectionId:
					methodArticleContentSectionModel = MethodArticleContentSectionModel.objects.filter(pk=articleContentSectionId).first()
					if methodArticleContentSectionModel:
						methodArticleContentModel = MethodArticleContentModel(article=methodArticleInfoModel, content=content, section=methodArticleContentSectionModel, is_login=isLogin, rank=rank)
						methodArticleContentModel.save()
						return json_result(message=u'成功添加文章版块内容!')
					else:
						return json_params_error(message=u'你尝试添加一个不存在的内容版块!')
			else:
				return json_params_error(message=u'你尝试查看一个不存在的文章!')
		else:
			return json_params_error(message=u'你尝试访问一个不存在的文章!')

#修改研究方法文章内容
@login_required
@require_http_methods(['GET','POST'])
def alter_method_article_content(request):
	if request.method == 'GET':
		return json_result(message=u'修改研究方法文章内容页面!')
	else:
		articleId = request.POST.get('article_id',0)
		contentId = request.POST.get('content_id',0)
		content = request.POST.get('content',None)
		articleContentSectionId = request.POST.get('article_content_section_id', 0)
		isLogin = request.POST.get('is_login',0)
		rank = request.POST.get('rank',0)

		try:
			articleId = int(articleId)
			contentId = int(contentId)
			articleContentSectionId = int(articleContentSectionId)
			isLogin = int(isLogin)
			rank = int(rank)
		except:pass

		if articleId and contentId:
			methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk = articleId,status__in=[1,2,3]).first()
			if methodArticleInfoModel:
				methodArticleContentModel = MethodArticleContentModel.objects.filter(pk=contentId,article=methodArticleInfoModel).first()
				if methodArticleContentModel:

					methodArticleContentSectionModel = MethodArticleContentSectionModel.objects.filter(pk=articleContentSectionId).first()
					if methodArticleContentSectionModel:

						methodArticleContentModel.content = content
						methodArticleContentModel.section = methodArticleContentSectionModel
						methodArticleContentModel.is_login = isLogin
						methodArticleContentModel.rank = rank

						methodArticleContentModel.save()
						return json_result(message=u'成功修改文章内容!')
					else:
						return json_params_error(message=u'你尝试选择一个不存在的文章内容版块')
				else:
					return json_params_error(message=u'你尝试修改一个不存在的文章内容!')
			else:
				return json_params_error(message=u'你尝试访问一个不存在的文章!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的文章内容版块!')

#删除研究方法文章内容
@login_required
@require_http_methods(['GET', 'POST'])
def delete_method_article_content(request):
	if request.method == 'GET':
		return json_result(message=u'修改研究方法文章内容页面!')
	else:
		articleId = request.POST.get('article_id', 0)
		contentId = request.POST.get('content_id', 0)

		try:
			articleId = int(articleId)
			contentId = int(contentId)
		except:
			pass

		if articleId and contentId:
			methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=articleId, status__in=[1, 2, 3]).first()
			if methodArticleInfoModel:
				methodArticleContentModel = MethodArticleContentModel.objects.filter(pk=contentId, article=methodArticleInfoModel).first()
				if methodArticleContentModel:
					methodArticleContentModel.delete()
					return json_result(message=u'成功删除文章版块!')

				else:
					return json_params_error(message=u'你尝试选择一个不存在的文章内容版块')
			else:
				return json_params_error(message=u'你尝试访问一个不存在的文章!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的文章内容版块!')

#研究方法文章版块列表
@login_required
def method_article_content_sections(request):
	methodArticleContentSectionModel = MethodArticleContentSectionModel.objects.all().values('id','section','create_time')

	context = {
		'method_article_content_sections': list(methodArticleContentSectionModel),
	}
	return json_result(data=context)

#研究方法文章列表/分类文章列表
@login_required
def method_articles(request,page=1,category_id=0):
	'''
		需求：
			1、请求的分类是1级分类，需要把1级分类下关联的2级文章都显示出来
			2、若是更多教程,则没有2级分类
	'''
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
		if methodCategoryModel:
			methodArticleInfoModel = MethodArticleInfoModel.objects.filter(
				Q(category__relevance_category=methodCategoryModel)|
			    Q(category=methodCategoryModel),
				status__in=[1,2,3]).all()
		else:
			return json_params_error(message=u'你尝试查看一个不存在的分类下的文章!')
	else:
		methodArticleInfoModel = MethodArticleInfoModel.objects.filter(status__in=[1,2,3]).all()

	if methodArticleInfoModel:
		article_list=[]
		for m in methodArticleInfoModel:
			# 分类展示的方式： parentCategory/childCategory
			if m.category:
				if m.category.relevance_category:
					parentCategory = m.category.relevance_category.category
					childCategory = m.category.category
					category = '%s/%s' % (parentCategory, childCategory)
				else:
					category = m.category.category
			else:
				category = None

			article_list.append({
				'id': m.id,
				'title': m.title,
				'category': category,
				'status': m.status,
				'arrange':m.arrange,
				'create_time':m.create_time,
			})

		articleCount = methodArticleInfoModel.count()

		pageCount = articleCount / numPage
		if articleCount % numPage > 0:
			pageCount += 1

		pages = []

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
		pages.sort()

		context = {
			'articles': article_list[start:end],
			'pages': pages,
			'current_page': currentPage,
			'page_count': pageCount,
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无文章!')

#添加研究方法内容版块
@login_required
@require_http_methods(['GET','POST'])
def add_method_article_content_section(request):
	if request.method == 'GET':
		return json_result(message=u'添加研究方法内容版块页面!')
	else:
		section = request.POST.get('section',None)
		try:
			section = str(section).replace(' ','')
		except:pass

		if section:
			repeatMethodArticleContentSectionModel = MethodArticleContentSectionModel.objects.filter(section=section).first()
			if repeatMethodArticleContentSectionModel:
				return json_params_error(message=u'此版块已存在!')
			else:
				methodArticleContentSectionModel = MethodArticleContentSectionModel(section=section)
				methodArticleContentSectionModel.save()
				return json_result(message=u'成功添加内容版块!')
		else:
			return json_params_error(message=u'请输入内容版块!')

#修改研究方法内容版块
@login_required
@require_http_methods(['GET','POST'])
def  alter_method_article_content_section(request,section_id=0):
	try:
		sectionId = int(section_id)
	except:pass

	if sectionId:
		methodArticleContentSectionModel = MethodArticleContentSectionModel.objects.filter(pk = sectionId).first()
		if methodArticleContentSectionModel:
			if request.method == 'GET':
				context = {
					'id':methodArticleContentSectionModel.id,
					'section':methodArticleContentSectionModel.section,
					'create_time':methodArticleContentSectionModel.create_time,
				}
				return json_result(data=context)
			else:
				section = request.POST.get('section',None)
				try:
					section = str(section).replace(' ', '')
				except:
					pass

				if section:
					repeatMethodArticleContentSectionModel = MethodArticleContentSectionModel.objects.filter(section=section).first()
					if repeatMethodArticleContentSectionModel:
						return json_params_error(message=u'此版块已存在!')
					else:
						methodArticleContentSectionModel.section = section
						methodArticleContentSectionModel.save()
						return json_result(message=u'成功添加内容版块!')
				else:
					return json_params_error(message=u'请输入内容版块!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的内容版块!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的内容版块!')

#自定义研究方法分类显示顺序
@require_http_methods(['GET', 'POST'])
@login_required
def alter_category_rank(request):
	'''
		实现思路：

			1、采用ajax提交，每次移动都会传入2个分类id 和修改后的顺序值,
			2、直接从数据库中检索替换
	'''
	if request.method == 'GET':
		return json_result(message=u'自定义分类显示顺序页面!')
	else:
		logger.info({'request.POST': request.POST})

		if len(request.POST):
			for k, v in request.POST.items():
				methodCategoryModel = MethodCategoryModel.objects.filter(pk=k).first()
				if methodCategoryModel:
					methodCategoryModel.rank = v
					methodCategoryModel.save()
				else:
					return json_params_error(message=u'你尝试给一个不存在的分类进行排序!')
			return json_result(message=u'修改分类排序完成!')
		else:
			return json_params_error(message=u'分类顺序暂无修改!')

#首页推荐文章列表
@login_required
def method_article_recommend_list(request):
	methodArticleRecommendModel = MethodArticleInfoModel.objects.filter(status = 2).all().order_by('arrange')
	if methodArticleRecommendModel:
		article_list = []
		for m in methodArticleRecommendModel:
			#分类展示的方式： parentCategory/childCategory
			if m.category:
				if m.category.relevance_category:
					parentCategory = m.category.relevance_category.category
					childCategory = m.category.category
					category = '%s/%s'%(parentCategory, childCategory)
				else:
					category = m.category.category
			else:
				category = None

			article_list.append({
				'id':m.id,
				'title':m.title,
				'category':category,
				'status':m.status,
				'arrange':m.arrange,
			})
		context = {
			'articles':article_list,
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无推荐文章!')

#首页推荐文章自定义排序
@login_required
@require_http_methods(['GET','POST'])
def method_article_recommend_arrange(request):

	'''
		采用ajax提交，每次文章位置发生移动,则提交给后台更新
		因此，每次会提交两个文章顺序数字进来
		数据结构：
		{
			'article_info1':arrange,
			'article_info2':arrange
		}
	'''

	if request.method == 'GET':
		return json_result(message=u'推荐文章自定义排序页面!')
	else:
		logger.info({'request.POST':request.POST})

		if len(request.POST):
			for k,v in request.POST.items():
				methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=k,status=2).first()
				if methodArticleInfoModel:
					methodArticleInfoModel.arrange = v
					methodArticleInfoModel.save()
				else:
					return json_params_error(message=u'你尝试修改一个不存在的文章!')
			return json_result(message=u'修改推荐文章自定义排序成功!')
		else:
			return json_params_error(message=u'暂无文章顺序修改!')

#取消文章推荐
@login_required
def cancel_method_article_recommend(request,article_id=0):
	'''
		mark:
			1、取消文章推荐状态的时候需要删除文章的arrange排序
	'''
	try:
		articleId = int(article_id)
	except:pass

	#由于这里是从首页文章列表中选取，因此需要带上状态为3的文章。
	if articleId:
		methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk = articleId,status__in=[1,2,3]).first()
		if methodArticleInfoModel.status == 2:
			methodArticleInfoModel.status = 1
			methodArticleInfoModel.arrange = None
			methodArticleInfoModel.save(update_fields=['status', 'arrange'])
			return json_result(message=u'取消推荐成功!')
		elif methodArticleInfoModel.status == 1:
			methodArticleInfoModel.status = 2
			methodArticleInfoModel.arrange = methodArticleInfoModel.id
			methodArticleInfoModel.save(update_fields=['status','arrange'])
			return json_result(message=u'文章推荐成功!')
		elif methodArticleInfoModel.status == 3:
			return json_result(message=u'此文章还未发布,不能推荐!')
		else:
			return json_params_error(message=u'你尝试取消一篇不存在的文章!')
	else:
		return json_params_error(message=u'你尝试查看一篇不存在的文章!')

#添加相关阅读文章
@login_required
@require_http_methods(['POST'])
def add_related_reading_method_article(request,article_id=0):
	try:
		articleId = int(article_id)
	except:pass

	if articleId:
		methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk = articleId).first()
		if methodArticleInfoModel:
			if request.method == 'POST':
				relatedReadingArticleId = request.POST.get('related_reading_article_id',0)
				try:
					relatedReadingArticleId = int(relatedReadingArticleId)
				except:pass

				if relatedReadingArticleId:
					relatedReadingArticleModel = MethodArticleInfoModel.objects.filter(pk=relatedReadingArticleId,status__in=[1,2]).first()
					if relatedReadingArticleModel:
						#判断若当前文章的相关阅读中已经存在将被添加的文章,则给出提示
						repeatRelatedReadingArticleModel = MethodArticleRelatedReadingModel.objects.filter(relevance_article=methodArticleInfoModel,related_reading_article=relatedReadingArticleModel).first()
						if repeatRelatedReadingArticleModel:
							return json_params_error(message=u'此文章已添加到当前的相关阅读中!')

						methodArticleRelatedReadingModel = MethodArticleRelatedReadingModel(relevance_article=methodArticleInfoModel,related_reading_article=relatedReadingArticleModel,arrange=relatedReadingArticleModel.id) #添加相关阅读文章的时候设置文章排序

						methodArticleRelatedReadingModel.save()
						return json_result(message=u'成功添加相关阅读文章!')
					else:
						return json_params_error(message=u'你添加的文章不存在!')
				else:
					return json_params_error(message=u'你尝试添加一个不存在的文章!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的文章!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的文章!')

#删除相关阅读文章
@login_required
@require_http_methods(['GET','POST'])
def delete_related_reading_method_article(request, article_id=0):
	if request.method == 'GET':
		return json_result(message=u'删除相关阅读文章页面!')
	else:
		relatedReadingArticleId = request.POST.get('related_reading_article_id',0)

		try:
			articleId = int(article_id)
			relatedReadingArticleId = int(relatedReadingArticleId)
		except:pass

		if articleId and relatedReadingArticleId:
			methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=articleId,status__in=[1,2]).first()
			relatedReadingArticleModel = MethodArticleInfoModel.objects.filter(pk=relatedReadingArticleId, status__in=[1,2]).first()
			if methodArticleInfoModel and relatedReadingArticleModel:
				methodArticleRelatedReadingModel = MethodArticleRelatedReadingModel.objects.filter(relevance_article=methodArticleInfoModel, related_reading_article=relatedReadingArticleModel).first()
				if methodArticleRelatedReadingModel:
					methodArticleRelatedReadingModel.delete()
					return json_result(message=u'成功删除相关阅读文章!')
				else:
					return json_params_error(message=u'此相关阅读文章已删除!')
			else:
				return json_params_error(message=u'你尝试删除一个不存在的相关阅读!')
		else:
			return json_params_error(message=u'你尝试删除一个不存在的相关文章!')

#相关阅读文章列表
@login_required
def related_reading_method_article_list(request,article_id=0):
	try:
		articleId = int(article_id)
	except:pass

	if articleId:
		#这里展示已发布、已推荐的文章关联的相关阅读文章
		methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk = articleId,status__in=[1,2]).first()
		if methodArticleInfoModel:
			#判断当前文章是否有相关阅读版块，有则展示相关阅读文章，否则不展示
			methodArticleRelatedReadingModel = MethodArticleRelatedReadingModel.objects.filter(relevance_article=methodArticleInfoModel).all().order_by('arrange')
			if methodArticleRelatedReadingModel:
				tmp_related_reading_list=[]
				for m in methodArticleRelatedReadingModel:
					if m.related_reading_article.category:
						if m.related_reading_article.category.relevance_category:
							parentCategory = m.related_reading_article.category.relevance_category.category
							childCategory = m.related_reading_article.category.category
							category = '%s/%s' % (parentCategory, childCategory)
						else:
							category = m.related_reading_article.category.category
					else:
						category = None

					tmp_related_reading_list.append({
						'id':m.related_reading_article.id,
						'title':m.related_reading_article.title,
						'category':category,
						'arrange': m.arrange,
					})
				context = {
					'articles':tmp_related_reading_list,
				}
				return json_result(data=context)
			else:
				return json_params_error(message=u'暂无相关阅读文章!')
		else:
			return json_params_error(message=u'你尝试查看一篇不存在的相关阅读文章!')
	else:
		return json_params_error(message=u'你尝试访问一篇不存在的相关阅读文章!')

#自定义相关阅读文章排序
@login_required
@require_http_methods(['GET', 'POST'])
def alter_related_reading_method_article_arrange(request,article_id=0):
	try:
		articleId = int(article_id)
	except:pass

	if articleId:
		methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=articleId, status__in=[1, 2]).first()
		if methodArticleInfoModel:
			#过滤出当前文章关联的更多阅读文章列表
			methodArticleRelatedReadingModel = MethodArticleRelatedReadingModel.objects.filter(relevance_article=methodArticleInfoModel).all()

			if methodArticleRelatedReadingModel:
				logger.info({'request.POST':request.POST})

				if len(request.POST):
					for k,v in request.POST.items():
						#查找出提交过来的关联文章是否存在，如果存在，则替换排序
						relatedReadingMethodArticleModel = MethodArticleInfoModel.objects.filter(pk=k, status__in=[1, 2]).first()

						if relatedReadingMethodArticleModel:
							#遍历相关连的阅读文章
							for m in methodArticleRelatedReadingModel:
								if m.related_reading_article == relatedReadingMethodArticleModel:
									m.arrange = v
									m.save()
						else:
							return json_params_error(message=u'你尝试修改一个不存在的文章!')

					return json_result(message=u'文章排序修改成功!')
				else:
					return json_params_error(message=u'暂无文章排序修改!')
			else:
				return json_params_error(message=u'暂无相关阅读文章!')

#上传banner图功能调用图片上传扩展接口
#上传banner图
@login_required
@require_http_methods(['GET','POST'])
def upload_method_banner(request):
	if request.method == 'GET':
		return json_result(message=u'上传banner页面!')
	else:
		name = request.POST.get('name',None)
		link = request.POST.get('link',None)
		type = request.POST.get('type',1)

		try:
			type =int(type)
		except:pass

		if name:
			bannerModel = BannerModel(name=name,link=link,type=type)
			bannerModel.save()
			return json_result(message=u'成功上传banner图片!')
		else:
			return json_params_error(message=u'请上传图片!')

#自定义banner显示顺序
@login_required
@require_http_methods(['GET','POST'])
def alter_method_banner_rank(request):
	if request.method == 'GET':
		return json_result(message=u'自定义banner显示顺序页面!')
	else:
		bannerId  = request.POST.get('banner_id',None)
		rank = request.POST.get('rank',None)
		try:
			bannerId = int(bannerId)
		except:
			pass

		if bannerId:
			bannerModel = BannerModel.objects.filter(pk =bannerId).first()
			if bannerModel:
				bannerModel.rank = rank
				bannerModel.save()
				return json_result(message=u'成功修改banner排序!')
			else:
				return json_params_error(message=u'你尝试访问一个不存在的banner图!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的banner图!')

#是否显示banner
@login_required
@require_http_methods(['GET', 'POST'])
def is_active_method_banner(request):
	if request.method == 'GET':
		return json_result(message=u'是否显示banner页面!')
	else:
		bannerId = request.POST.get('banner_id',None)
		isActive = request.POST.get('is_active',0)

		try:
			bannerId = int(bannerId)
			isActive = int(isActive)
		except:pass

		logger.info({'banner_id':bannerId,'is_active':isActive})

		if bannerId:
			bannerModel = BannerModel.objects.filter(pk=bannerId).first()
			if bannerModel:
				bannerModel.is_active = isActive
				bannerModel.save()
				if bannerModel.is_active == 1:
					return json_result(message=u'banner图已置为显示!')
				else:
					return json_result(message=u'banner图已置为不显示!')
			else:
				return json_params_error(message=u'你尝试访问一个不存在的banner图!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的banner图!')

#删除banner
@login_required
@require_http_methods(['GET', 'POST'])
def delete_method_banner(request):
	if request.method == 'GET':
		return json_result(message=u'删除banner页面!')
	else:
		bannerId = request.POST.get('banner_id', None)

		try:
			bannerId = int(bannerId)
		except:
			pass

		if bannerId:
			bannerModel = BannerModel.objects.filter(pk=bannerId).first()
			if bannerModel:
				bannerModel.delete()
				return json_result(message=u'成功删除banner!')
			else:
				return json_params_error(message=u'你尝试访问一个不存在的banner图!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的banner图!')

#banner列表
@login_required
def method_banner_list(request):
	bannerModel = BannerModel.objects.all().order_by('rank').values('id','name','link','is_active', 'rank', 'type','create_time')

	context = {
		'banners': list(bannerModel)
	}
	return json_result(data=context)

#修改banner类型
@login_required
def method_banner_type(request,id=0):

	if request.method == 'GET':
		return json_result(message=u'修改banner类型页面!')
	else:
		typeId = request.POST.get('type_id',None)

		try:
			Id = int(id)
			typeId = int(typeId)
		except:
			pass

		if typeId in [1,2]:

			bannerModel = BannerModel.objects.filter(pk=Id).first()
			if bannerModel:
				bannerModel.type = typeId
				bannerModel.save()
				return json_result(message=u'成功修改banner类型',data={'type_id':typeId})
			else:
				return json_params_error(message=u'你尝试查看一个不存在的banner!')
		else:
			return json_params_error(message=u'你尝试给banner添加一个不存在的类型!')

#搜索研究方法文章
@login_required
@require_http_methods(['GET','POST'])
def search_method_article(request,page=1,category_id=0):

	'''
		1、由于这次改版将文章标题属性和内容分开存储的特性，因此搜索的时候需要关联查询2张表
	'''
	try:
		currentPage = int(page)
		categoryId = int(category_id)
	except:
		pass

	if request.method == 'GET':
		return json_result(message=u'搜索研究方法文章页面!')
	else:
		searchWord = request.POST.get('search_word',None)

		logger.info({'search_word':searchWord})

		if searchWord:
			try:
				searchWord = str(searchWord).replace(' ','')
			except:pass

			numPage = int(configs.PC_FRONT_NUM_PAGE)
			start = (currentPage - 1) * numPage
			end = start + numPage

			if categoryId:
				methodCategoryModel = MethodCategoryModel.objects.filter(pk=categoryId, is_active=1).first()
				#这里要注意过滤分类的时候提交的是1级分类, 目前的数据结构是 1级分类下关联的有子分类
				#遍历出这个1级分类下关联的子分类,将父分类和子分类全部添加到临时列表
				category_list = [methodCategoryModel]
				relevanceCategoryModel = MethodCategoryModel.objects.filter(relevance_category=methodCategoryModel).all()
				for r in relevanceCategoryModel:
					category_list.append(r)

				if methodCategoryModel:
					# 先过滤出符合条件的文章信息,然后在这些文章中检索出和关键词相匹配的文章
					tmp_articleModel = MethodArticleInfoModel.objects.filter(Q(title__icontains=searchWord) | Q(summary__icontains=searchWord), status__in=[1, 2, 3],category__in=category_list).all()
				else:
					return json_params_error(message=u'你尝试查看一个不存在的分类下的文章!')
			else:
				#indexModel = MethodArticleInfoModel.objects.filter(status__in=[1,2,3]).all()
				tmp_articleModel = MethodArticleInfoModel.objects.filter(Q(title__icontains=searchWord) | Q(summary__icontains=searchWord),status__in=[1, 2, 3]).all()

			articleModel = []
			for t in tmp_articleModel:
				if t not in articleModel:
					articleModel.append(t)
		else:
			return json_params_error(message=u'请输入要搜索的关键词!')

	if len(articleModel) > 0:
		articles = []
		for m in articleModel:
			# 分类展示的方式： parentCategory/childCategory
			if m.category:
				if m.category.relevance_category:
					parentCategory = m.category.relevance_category.category
					childCategory = m.category.category
					category = '%s/%s' % (parentCategory, childCategory)
				else:
					category = m.category.category
			else:
				category = None

			articles.append({
				'id': m.id,
				'title': m.title,
				'category': category,
				'status': m.status,
				'arrange': m.arrange,
				'create_time':m.create_time,
			})

		articleCount = len(articles)

		pageCount = articleCount / numPage
		if articleCount % numPage > 0:
			pageCount += 1

		pages = []

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
			else:
				pages.append(tmpPage)
				tmpPage += 1
		pages.sort()

		context = {
			'articles': articles[start:end],
			'pages': pages,
			'current_page': currentPage,
			'page_count': pageCount,
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无相关文章!')

'''
	author: zhangx
	date: 20180118
	mark:
		1、研究方法专题版块
'''

#添加专题
@login_required
@require_http_methods(['GET','POST'])
def add_method_article_topic(request):
	if request.method == 'GET':
		return json_result(message=u'添加专题页面!')
	else:

		now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

		title = request.POST.get('title',None)
		summary = request.POST.get('summary',None)
		status = request.POST.get('status',1)
		arrange = request.POST.get('arrange',None)
		createTime = request.POST.get('create_time',now_time)
		thumbnail = request.POST.get('thumbnail',None)
		app_thumbnail = request.POST.get('app_thumbnail',None)

		try:
			tmp_create_time = time.strptime(createTime,"%Y-%m-%d %H:%M:%S")
			Y,m,d,H,M,S = tmp_create_time[0:6]
			tmp_time = datetime.datetime(Y,m,d,H,M,S)

			status = int(status)
		except:pass

		if status not in [0,1,2]:
			return json_params_error(message=u'你尝试选择一种不存在的状态!')

		if title:
			methodArticleTopicModel = MethodArticleTopicModel(title=title,summary=summary,status=status,arrange=arrange,create_time=createTime,thumbnail=thumbnail,app_thumbnail=app_thumbnail)
			methodArticleTopicModel.save()
			return json_result(message=u'添加专题成功!',data={'topic_id':methodArticleTopicModel.id})
		else:
			return json_params_error(message=u'专题标题不能为空!')

#修改专题
@login_required
@require_http_methods(['GET','POST'])
def alter_method_article_topic(request,topic_id=0):
	try:
		topicId = int(topic_id)
	except:pass

	if topicId:
		methodArticleTopicModel = MethodArticleTopicModel.objects.filter(status__in=[1,2],pk=topicId).first()
		if methodArticleTopicModel:
			if request.method == 'GET':
				context = {
					'title':methodArticleTopicModel.title,
					'summary':methodArticleTopicModel.summary,
					'status':methodArticleTopicModel.status,
					'create_time':methodArticleTopicModel.create_time,
					'thumbnail':methodArticleTopicModel.thumbnail,
					'app_thumbnail':methodArticleTopicModel.app_thumbnail,
					'arrange':methodArticleTopicModel.arrange,
				}
				return json_result(data=context)
			else:

				title = request.POST.get('title',methodArticleTopicModel.title)
				summary = request.POST.get('summary',methodArticleTopicModel.summary)
				status = request.POST.get('status',methodArticleTopicModel.status)
				arrange = request.POST.get('arrange',methodArticleTopicModel.arrange)
				createTime = request.POST.get('create_time',methodArticleTopicModel.create_time)
				thumbnail = request.POST.get('thumbnail',methodArticleTopicModel.thumbnail)
				app_thumbnail = request.POST.get('app_thumbnail', methodArticleTopicModel.app_thumbnail)

				logger.info({'title': title, 'summary': summary, 'status': status, 'thumbnail': thumbnail,'app_thumbnail': app_thumbnail})

				try:
					tmp_create_time = time.strptime(createTime,'%Y-%m-%d %H:%M:%S')
					Y,m,d,H,M,S = tmp_create_time[0:6]
					tmp_time = datetime.datetime(Y,m,d,H,M,S)

					status = int(status)
				except:pass

				if status not in[0,1,2]:
					return json_params_error(message=u'你尝试选择一个不存在的状态!')

				methodArticleTopicModel.title = title
				methodArticleTopicModel.summary = summary
				methodArticleTopicModel.status = status
				methodArticleTopicModel.arrange = arrange
				methodArticleTopicModel.create_time = createTime
				methodArticleTopicModel.thumbnail = thumbnail
				methodArticleTopicModel.app_thumbnail = app_thumbnail
				methodArticleTopicModel.save()
				return json_result(message=u'修改专题信息成功!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的专题信息!')

#删除专题
@login_required
@require_http_methods(['GET','POST'])
def delete_method_article_topic(request):
	if request.method == 'GET':
		return json_result(message=u'删除专题页面!')
	else:
		topicId = request.POST.get('topic_id',0)
		try:
			topicId = int(topicId)
		except:pass

		if topicId:
			methodArticleTopicModel = MethodArticleTopicModel.objects.filter(pk=topicId).first()
			if methodArticleTopicModel:
				# 删除专题时需要将专题相关的文章关联关系删除，再删除专题!
				topicRelatedMethodArticleModel = TopicRelatedMethodArticleModel.objects.filter(topic=methodArticleTopicModel).all()
				topicRelatedMethodArticleModel.delete()
				#再删除专题
				methodArticleTopicModel.delete()
				return json_result(message=u'删除专题成功!')
			else:
				return json_params_error(message=u'你尝试查看一个不存在的专题!')
		else:
			return json_params_error(message=u'你尝试访问一个不存在的专题!')

#专题列表
@login_required
def method_article_topic_list(request,page=1):
	try:
		currentPage = int(page)
	except:pass

	numPage = int(configs.PC_FRONT_NUM_PAGE)
	start = (currentPage -1) *numPage
	end = start +numPage

	methodArticleTopicModel = MethodArticleTopicModel.objects.annotate(topic_count = Count('topicrelatedmethodarticlemodel')).all().order_by('arrange')

	if methodArticleTopicModel:
		articleCount = methodArticleTopicModel.count()

		pageCount = articleCount / numPage

		if articleCount % numPage:
			pageCount +=1

		methodArticleTopicModel = methodArticleTopicModel[start:end]

		topic_list =[]
		for m in methodArticleTopicModel:
			if m.status ==1:
				status = u'隐藏'
			else:
				status = u'显示'

			topic_list.append({
				'id':m.id,
				'title': m.title,
				'arrange':m.arrange,
				'topic_count':m.topic_count,
				'status':status,
				'create_time':m.create_time,
			})

		context ={
			'current_page':currentPage,
			'page_count':pageCount,
			'topic_list':topic_list,
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无专题!')

#给专题添加相关文章
@login_required
@require_http_methods(['GET', 'POST'])
def add_topic_related_method_article(request):
	if request.method == 'GET':
		return json_result(message=u'给专题添加相关文章页面!')
	else:
		topicId = request.POST.get('topic_id',0)
		articleId = request.POST.get('article_id',0)

		try:
			topicId = int(topicId)
			articleId = int(articleId)
		except:pass

		logger.info({'topicId': topicId,'articleId': articleId})

		if topicId or articleId:
			methodArticleTopicModel = MethodArticleTopicModel.objects.filter(pk = topicId).first()
			methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=articleId,status__in=[1,2,3]).first()

			logger.info({'topic_id': methodArticleTopicModel.id,'article_id': methodArticleInfoModel.id})

			if methodArticleTopicModel and methodArticleInfoModel:
				topicRelatedMethodArticleModel = TopicRelatedMethodArticleModel(topic=methodArticleTopicModel,article=methodArticleInfoModel)

				# 给专题中每篇相关文章增加默认排序
				topicCount = TopicRelatedMethodArticleModel.objects.filter(topic=methodArticleTopicModel).count()
				topicRelatedMethodArticleModel.arrange = topicCount + 1

				topicRelatedMethodArticleModel.save()

				return json_result(message=u'添加专题文章成功!')
			else:
				return json_params_error(message=u'你尝试查看一个不存在的专题或文章!')
		else:
			return json_params_error(message=u'你尝试访问一个不存在的专题或文章!')

#删除专题中相关文章
@login_required
@require_http_methods(['GET', 'POST'])
def delete_topic_related_method_article(request):
	if request.method == 'GET':
		return json_result(message=u'删除专题相关文章页面!')
	else:
		topicId = request.POST.get('topic_id', 0)
		articleId = request.POST.get('article_id', 0)

		try:
			topicId = int(topicId)
			articleId = int(articleId)
		except:
			pass

		if topicId or articleId:
			methodArticleTopicModel = MethodArticleTopicModel.objects.filter(pk=topicId).first()
			methodArticleInfoModel = MethodArticleInfoModel.objects.filter(pk=articleId, status__in=[1, 2, 3]).first()
			if methodArticleTopicModel and methodArticleInfoModel:
				topicRelatedMethodArticleModel = TopicRelatedMethodArticleModel.objects.filter(topic=methodArticleTopicModel,article=methodArticleInfoModel)
				topicRelatedMethodArticleModel.delete()
				return json_result(message=u'删除专题文章成功!')
			else:
				return json_params_error(message=u'你尝试查看一个不存在的专题或文章!')
		else:
			return json_params_error(message=u'你尝试访问一个不存在的专题或文章!')

#专题相关文章自定义排序
@login_required
@require_http_methods(['GET','POST'])
def alter_method_article_arrange(request,topic_id=0):
	try:
		topicId = int(topic_id)
	except:pass

	if topicId:
		methodArticleTopicModel = MethodArticleTopicModel.objects.filter(status__in=[1, 2], pk=topicId).first()
		if methodArticleTopicModel:
			if request.method == 'GET':
				return json_result(message=u'专题相关文章自定义排序!')
			else:
				if len(request.POST):
					for k,v in request.POST.items():
						try:
							k = int(k)
							v = int(v)
						except:pass

						topicRelatedMethodArticleModel = TopicRelatedMethodArticleModel.objects.filter(topic=methodArticleTopicModel,article__id = k).first()
						if topicRelatedMethodArticleModel:
							topicRelatedMethodArticleModel.arrange = v
							topicRelatedMethodArticleModel.save()
						else:
							return json_params_error(message=u'你尝试修改一个不存在的相关文章!')
					return json_result(message=u'修改专题相关文章自定义排序成功!')
				else:
					return json_params_error(message=u'暂无文章排序修改!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的专题!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的专题!')

#专题相关文章列表
@login_required
def topic_related_method_article_list(request,topic_id=0):
	try:
		topicId = int(topic_id)
	except:pass

	if topicId:
		methodArticleTopicModel = MethodArticleTopicModel.objects.filter(pk=topicId).first()
		if methodArticleTopicModel:
			topicRelatedMethodArticleModel = TopicRelatedMethodArticleModel.objects.filter(topic=methodArticleTopicModel).order_by('arrange')
			if topicRelatedMethodArticleModel:
				topic_article_list=[]
				for t in topicRelatedMethodArticleModel:
					topic_article_list.append({
						'id':t.article.id,
						'title':t.article.title,
						'category':t.article.category.category,
						'arrange':t.arrange,
					})

				context ={
					'topic_related_method_article_list':topic_article_list,
				}
				return json_result(data=context)
			else:
				return json_params_error(message=u'暂无相关文章!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的专题文章列表!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的专题文章列表!')

#专题搜索
@require_http_methods(['GET','POST'])
@login_required
def search_topic_related_method_article(request,page=1):
	try:
		currentPage = int(page)
	except:
		pass

	numPage = int(configs.PC_FRONT_NUM_PAGE)
	start = (currentPage - 1) * numPage
	end = start + numPage

	if request.method == 'POST':
		searchKeyWords = request.POST.get('search_key_words', None)

		methodArticleTopicModel = MethodArticleTopicModel.objects.filter(Q(title=searchKeyWords)|Q(summary=searchKeyWords)).annotate(topic_count=Count('topicrelatedmethodarticlemodel')).all()

		if methodArticleTopicModel:
			articleCount = methodArticleTopicModel.count()

			pageCount = articleCount / numPage

			if articleCount % numPage:
				pageCount += 1

			methodArticleTopicModel = methodArticleTopicModel[start:end]

			topic_list = []
			for m in methodArticleTopicModel:
				if m.status == 1:
					status = u'隐藏'
				else:
					status = u'显示'

				topic_list.append({
					'id': m.id,
					'title': m.title,
					'arrange': m.arrange,
					'topic_count': m.topic_count,
					'status': status,
					'create_time': m.create_time,
				})

			context = {
				'current_page': currentPage,
				'page_count': pageCount,
				'topic_list': topic_list,
			}
			return json_result(data=context)
		else:
			return json_params_error(message=u'暂无专题!')

'''
	author :zhangx
	date :20180313
	mark :
		1、新增提问关键词检索功能(主要检索研究方法文章)
'''
#创建搜索关键词分组
@require_http_methods(['GET','POST'])
@login_required
def add_key_word_group(request):
	if request.method == 'GET':
		return json_result(message=u'添加关键词分组和文章页面!')
	else:
		groupName = request.POST.get('group_name',None)
		try:
			groupName = str(groupName).strip()
		except:pass

		logging.info({'group_name':groupName})

		if groupName:
			#查询分组名称是否存在
			keyWordGroupModel = KeyWordGroupModel.objects.filter(group_name=groupName).first()

			if keyWordGroupModel:
				return json_params_error(message=u'您添加的关键词分组已存在!')

			addKeyWordGroupModel = KeyWordGroupModel(group_name=groupName)
			addKeyWordGroupModel.save()
			return json_result(message=u'添加关键词分组数据成功!',data={'group_id':addKeyWordGroupModel.id})
		else:
			return json_params_error(message=u'关键词分组名称不能为空!')

#修改关键词分组名称
@require_http_methods(['GET','POST'])
@login_required
def alter_key_word_group_name(request,group_id=0):
	try:
		groupId = int(group_id)
	except:pass
	keyWordGroupModel = KeyWordGroupModel.objects.filter(pk = groupId).first()
	if keyWordGroupModel:
		if request.method == 'GET':
			#将关键词列表返回
			keyWordModel = KeyWordModel.objects.filter(group_name=keyWordGroupModel).values('id','key_word')
			#将关联文章返回
			keyWordRelevanceArticleModel = KeyWordRelevanceArticleModel.objects.filter(group_name=keyWordGroupModel).all()
			articleList = []
			if keyWordRelevanceArticleModel:
				for k in keyWordRelevanceArticleModel:

					if k.type == 1:
						methodArticleInfoModel = MethodArticleInfoModel.objects.filter(status__in=[1, 2], pk=k.article).first()
						if methodArticleInfoModel:
							articleList.append({
								'id': methodArticleInfoModel.id,
								'title': methodArticleInfoModel.title,
								'category':methodArticleInfoModel.category.category,
								'rank': methodArticleInfoModel.rank,
								'type': k.type,
							})
					else:
						methodArticleTopicModel = MethodArticleTopicModel.objects.filter(status__in=[2], pk=k.article).first()
						if methodArticleTopicModel:
							articleList.append({
								'id': methodArticleTopicModel.id,
								'title': methodArticleTopicModel.title,
								'category':u'专题',
								'rank': None,
								'type': k.type,
							})
			context = {
				'id':keyWordGroupModel.id,
				'group_name':keyWordGroupModel.group_name,
				'key_word': list(keyWordModel),
				'relevance_articles':articleList,
			}
			return json_result(message=u'修改关键词分组名称页面!',data=context)
		else:
			groupName = request.POST.get('group_name',keyWordGroupModel.group_name)

			try:
				groupName = str(groupName).strip()
			except:pass

			if groupName:
				# 查询分组名称是否存在
				repeatKeyWordGroupModel = KeyWordGroupModel.objects.filter(group_name=groupName).first()
				if repeatKeyWordGroupModel:
					if repeatKeyWordGroupModel.id !=keyWordGroupModel.id:
						return json_params_error(message=u'您添加的关键词分组已存在!')
				keyWordGroupModel.group_name = groupName
				keyWordGroupModel.save()
				return json_result(message=u'修改分组名称成功!')
			else:
				return json_params_error(message=u'关键词分组名称不能为空!')
	else:
		return json_params_error(message=u'你尝试查看一个不存在的分组信息!')

#添加关键词
@require_http_methods(['GET','POST'])
@login_required
def add_key_word(request,group_id=0):

	if request.method == 'GET':
		return json_result(message=u'添加关键词页面!')
	else:
		keyWord = request.POST.get('key_word',None)
		try:
			groupId = int(group_id)
			keyWord = str(keyWord).strip()
		except:pass

		keyWordGroupModel = KeyWordGroupModel.objects.filter(pk=groupId).first()
		if keyWordGroupModel:
			addKeyWordModel = KeyWordModel(group_name=keyWordGroupModel,key_word=keyWord)
			addKeyWordModel.save()
			return json_result(message=u'添加关键词成功!',data={'key_word_id':addKeyWordModel.id,'key_word':addKeyWordModel.key_word})
		else:
			return json_params_error(message=u'你尝试查看一个不存在的分组信息!')

#删除关键词
@login_required
def delete_key_word(request,key_word_id=0):

	try:
		keyWordId = int(key_word_id)
	except:pass

	keyWordModel = KeyWordModel.objects.filter(pk = keyWordId).first()
	if keyWordModel:
		keyWordModel.delete()
		return json_result(message=u'成功删除关键词!')
	else:
		return json_params_error(message=u'你尝试删除一个不存在的关键词!')

#给分组添加关联文章
@require_http_methods(['GET','POST'])
@login_required
def add_key_word_group_relevance_article(request,group_id=0):
	if request.method == 'GET':
		return json_result(message=u'给分组添加文章页面')
	else:
		articleId = request.POST.get('article_id',None)
		typeId = request.POST.get('type_id',None)
		try:
			groupId = int(group_id)
			articleId = int(articleId)
			typeId = int(typeId)
		except:pass

		if groupId:
			keyWordGroupModel = KeyWordGroupModel.objects.filter(pk = groupId).first()
			if keyWordGroupModel:
				#判断提交过来的数据的类型，若typeId=1 表示是研究方法文章 ，否则为专题合集。
				if typeId == 1:
					methodArticleInfoModel = MethodArticleInfoModel.objects.filter(status__in=[1, 2], pk=articleId).first()
					if not methodArticleInfoModel:
						return json_params_error(message=u'你尝试添加一个不存在的文章!')
				else:
					methodArticleTopicModel = MethodArticleTopicModel.objects.filter(status__in=[2], pk=articleId).first()
					if not methodArticleTopicModel:
						return json_params_error(message=u'你尝试添加一个不存在的专题合集!')

				keyWordRelevanceArticleModel = KeyWordRelevanceArticleModel(group_name=keyWordGroupModel, article=articleId, type=typeId)
				keyWordRelevanceArticleModel.save()
				return json_result(message=u'添加关联文章成功!')
			else:
				return json_params_error(message=u'你尝试访问一个不存在的关键次分组信息!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的关键词分组信息!')

#删除分组下的关联文章
@require_http_methods(['GET','POST'])
@login_required
def delete_key_word_group_relevance_article(request,group_id=0):

	if request.method == 'GET':
		return json_result(message=u'删除分组下的关联文章页面')
	else:
		articleId = request.POST.get('article_id', None)
		typeId = request.POST.get('type_id', None)
		try:
			groupId = int(group_id)
			articleId = int(articleId)
			typeId = int(typeId)
		except:
			pass

		if groupId:
			keyWordGroupModel = KeyWordGroupModel.objects.filter(pk=groupId).first()
			if keyWordGroupModel:

				keyWordRelevanceArticleModel = KeyWordRelevanceArticleModel.objects.filter(group_name=keyWordGroupModel, article=articleId,type=typeId).first()
				if keyWordRelevanceArticleModel:
					keyWordRelevanceArticleModel.delete()
					return json_result(message=u'成功删除关联文章!')

			else:
				return json_params_error(message=u'你尝试查看一个不存在的分组信息!')
		else:
			return json_params_error(message=u'你尝试访问一个不存在的分组信息!')

#删除关键词分组数据
@require_http_methods(['GET','POST'])
@login_required
def delete_key_word_group(request,group_id=0):
	if request.method == 'GET':
		return json_result(message=u'删除关键词分组页面')
	else:
		try:
			groupId = int(group_id)
		except:
			pass
		keyWordGroupModel = KeyWordGroupModel.objects.filter(pk=groupId).first()
		if keyWordGroupModel:
			#需要同时删除3张表的数据
			keyWordModel = KeyWordModel.objects.filter(group_name=keyWordGroupModel).all()
			keyWordRelevanceArticleModel = KeyWordRelevanceArticleModel.objects.filter(group_name=keyWordGroupModel).all()

			if keyWordModel:
				keyWordModel.delete()

			if keyWordRelevanceArticleModel:
				keyWordRelevanceArticleModel.delete()

			keyWordGroupModel.delete()

			return json_result(message=u'成功删除关键词分组信息!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的分组信息!')

#关键词分组数据列表
@login_required
def key_word_groups(request,page=1):
	try:
		currentPage = int(page)
	except:pass

	numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
	start = (currentPage - 1) * numPage
	end = start + numPage

	keyWordGroupModel = KeyWordGroupModel.objects.all()

	keyWordGroupCount = keyWordGroupModel.count()

	pageCount = keyWordGroupCount / numPage

	if keyWordGroupCount %numPage>0:
		pageCount +=1

	keyWordGroupModel = list(keyWordGroupModel)[start:end]
	keyWordGroupsList=[]
	for k in keyWordGroupModel:
		keyWordList=[]
		keyWordModel = KeyWordModel.objects.filter(group_name=k).all()
		for kw in keyWordModel:
			keyWordList.append(kw.key_word)

		keyWordGroupsList.append({
			'group_id':k.id,
			'group_name':k.group_name,
			'key_word_list':keyWordList,
		})
	context = {
		'current_page':currentPage,
		'page_count':pageCount,
		'key_word_groups':keyWordGroupsList,
	}
	return json_result(data=context)

#搜索关键词文章列表
@require_http_methods(['GET','POST'])
@login_required
def search_key_word_articles(request):
	if request.method == 'GET':
		return json_result(message=u'搜索关键词文章页面!')
	else:
		searchKeyWord = request.POST.get('search_key_word',None)

		if searchKeyWord:
			articleList=[]

			#由于需要同时列出研究方法和专题，因此需要检索2张表
			methodArticleInfoModel =MethodArticleInfoModel.objects.filter(status__in=[1,2],title__icontains=searchKeyWord).all()
			if methodArticleInfoModel:
				for m in methodArticleInfoModel:
					#如果分类id=13，则为专题合集的文章
					if m.category:
						category = m.category.category
						categoryId = m.category.id
					else:
						category = None
						categoryId = None

					articleList.append({
						'id':m.id,
						'title':m.title,
						'category':category,
						'category_id':categoryId,
						'rank':m.rank,
						'create_time':m.create_time,
						'type':1,
					})
			#再检索专题合集
			methodArticleTopicModel = MethodArticleTopicModel.objects.filter(status__in=[2],title__icontains=searchKeyWord).all()
			if methodArticleTopicModel:
				for m in methodArticleTopicModel:
					articleList.append({
						'id':m.id,
						'title':m.title,
						'category':u'专题',
						'rank':None,
						'create_time':m.create_time,
						'type':2,
					})

			#将汇总的检索结果按照时间倒序
			articles = sorted(articleList,key=lambda x:x['create_time'],reverse=True)
			context ={
				'articles': articles,
			}
			return json_result(data=context)
		else:
			return json_params_error(message=u'关键词不能为空!')

#搜索关键词
@require_http_methods(['GET','POST'])
@login_required
def search_key_word(request,page=1):
	try:
		currentPage = int(page)
	except:
		pass

	if request.method == 'GET':
		return json_result(message=u'关键词搜索页面!')
	else:
		searchKeyWord = request.POST.get('search_key_word', None)

		if searchKeyWord:

			numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
			start = (currentPage - 1) * numPage
			end = start + numPage

			#检索关键词表，返回有效的关键词分组列表
			keyWordGroupModel = KeyWordGroupModel.objects.filter(keywordmodel__key_word__icontains=searchKeyWord).all()

			keyWordGroupCount = keyWordGroupModel.count()

			pageCount = keyWordGroupCount / numPage

			if keyWordGroupCount % numPage > 0:
				pageCount += 1

			keyWordGroupModel = list(keyWordGroupModel)[start:end]
			keyWordGroupsList = []
			for k in keyWordGroupModel:
				keyWordList = []
				keyWordModel = KeyWordModel.objects.filter(group_name=k).all()
				for kw in keyWordModel:
					keyWordList.append(kw.key_word)

				keyWordGroupsList.append({
					'group_id': k.id,
					'group_name': k.group_name,
					'key_word_list': keyWordList,
				})
			context = {
				'current_page': currentPage,
				'page_count': pageCount,
				'key_word_groups': keyWordGroupsList,
			}
			return json_result(data=context)

		else:
			return json_params_error(message=u'关键词不能为空!')

'''
	author:zhangx
	date: 20180201
	mark:
		1、研究进展版块

'''

#添加研究进展分类
@login_required
@require_http_methods(['GET','POST'])
def add_news_category(request):
	if request.method == 'GET':
		return json_result(message=u'添加研究进展分类页面!')
	else:
		category = request.POST.get('category', None)

		if category:

			addNewsCategoryModel = NewsCategoryModel(category=category)
			addNewsCategoryModel.save()
			return json_result(message=u'成功添加分类!')
		else:
			return json_params_error(message=u'请填写分类名称!')

#修改研究进展分类
@login_required
@require_http_methods(['GET','POST'])
def alter_news_category(request,category_id):
	try:
		categoryId = int(category_id)
	except:pass

	if categoryId:
		newsCategoryModel = NewsCategoryModel.objects.filter(pk = categoryId).first()
		if newsCategoryModel:
			if request.method == 'GET':
				context = {
					'id':newsCategoryModel.id,
					'category':newsCategoryModel.category,
				}
				return json_result(data=context)
			else:
				category = request.POST.get('category', None)
				try:
					category = str(category).strip()
				except:pass

				if category:
					newsCategoryModel.category = category
					newsCategoryModel.save()

					return json_result(message=u'成功添加分类!')
				else:
					return json_params_error(message=u'请填写分类名称!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的分类!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的分类!')

#研究进展分类列表
@login_required
def news_category_list(request):
	newsCategoryListModel = NewsCategoryModel.objects.all().values('id','category','create_time')

	context = {
		'news_category_list':list(newsCategoryListModel)
	}
	return json_result(data=context)

#添加研究进展文章
@login_required
@require_http_methods(['GET','POST'])
def add_news(request):
	if request.method == 'GET':
		return json_result(message=u'添加研究进展内容页面!')
	else:
		# 获取当前时间
		now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

		title = request.POST.get('title', None)
		summary = request.POST.get('summary', None)
		thumbnail = request.POST.get('thumbnail', None)
		app_thumbnail = request.POST.get('thumbnail',None)
		categoryId = request.POST.get('category_id', None)
		content = request.POST.get('content',None)
		status = request.POST.get('status',1)
		fileName = request.POST.get('file_name',None)
		createTime = request.POST.get('create_time', now_time)

		# 将createTime转换成时间格式
		try:
			tmp_create_time = time.strptime(createTime, "%Y-%m-%d %H:%M:%S")  # strptime 根据指定格式将字符串解析成时间元祖
			Y, m, d, H, M, S = tmp_create_time[0:6]
			tmp_time = datetime.datetime(Y, m, d, H, M, S)
		except:
			pass

		logger.info({
			'title': title,
			'summary': summary,
			'thumbail': thumbnail,
			'category_id': categoryId,
			'status':status,
			'fileName': fileName,
			'create_time': createTime,
		})

		if title:
			if categoryId:
				newsCategoryModel = NewsCategoryModel.objects.filter(pk=categoryId).first()
			else:
				newsCategoryModel = None

			newsModel = NewsModel(title=title, summary=summary, thumbnail=thumbnail, app_thumbnail =app_thumbnail,category=newsCategoryModel, content=content,status=status, file_name=fileName, create_time=tmp_time,author=request.user)
			newsModel.save()

			context = {
				'id': newsModel.id,
			}
			return json_result(message=u'添加新闻成功!',data=context)

		else:
			return json_params_error(message=u'文章标题不能为空!')


#修改研究进展文章
@login_required
@require_http_methods(['GET','POST'])
def alter_news(request,news_id=0):
	try:
		newsId = int(news_id)
	except:pass

	if newsId:
		newsModel = NewsModel.objects.filter(pk = newsId,status__in=[1,2,3]).first()
		if newsModel:
			if request.method == 'GET':
				if newsModel.category:
					category = newsModel.category.id
				else:
					category = None

				context = {
					'id': newsModel.id,
					'title': newsModel.title,
					'summary': newsModel.summary,
					'thumbnail': newsModel.thumbnail,
					'app_thumbnail':newsModel.app_thumbnail,
					'category': category ,
					'status': newsModel.status,
					'file_name': newsModel.file_name,
					'create_time': newsModel.create_time,
					'content':newsModel.content,
				}
				return json_result(data=context)
			else:
				# 获取当前时间
				now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

				title = request.POST.get('title', newsModel.title)
				summary = request.POST.get('summary', newsModel.summary)
				thumbnail = request.POST.get('thumbnail', newsModel.thumbnail)
				app_thumbnail = request.POST.get('app_thumbnail',newsModel.app_thumbnail)
				categoryId = request.POST.get('category_id', None)
				content = request.POST.get('content', newsModel.content)
				status = request.POST.get('status', newsModel.status)
				fileName = request.POST.get('file_name', newsModel.file_name)
				createTime = request.POST.get('create_time', newsModel.create_time)

				# 将createTime转换成时间格式
				try:
					createTime = str(createTime)
					if createTime:
						tmp_create_time = time.strptime(createTime, "%Y-%m-%d %H:%M:%S")
						Y, m, d, H, M, S = tmp_create_time[0:6]
						tmp_time = datetime.datetime(Y, m, d, H, M, S)
					else:
						tmp_time = now_time
				except:
					pass

				logger.info({
					'title': title,
					'summary': summary,
					'thumbail': thumbnail,
					'category_id': categoryId,
					'status': status,
					'fileName': fileName,
					'create_time': createTime,
					'content':content,
				})

				if title:
					if categoryId:
						newsCategoryModel = NewsCategoryModel.objects.filter(pk=categoryId).first()
						newsModel.category = newsCategoryModel
					else:
						newsModel.category =None

					newsModel.title = title
					newsModel.summary = summary
					newsModel.thumbnail = thumbnail
					newsModel.app_thumbnail = app_thumbnail
					newsModel.content = content
					newsModel.status = status
					newsModel.file_name = fileName
					newsModel.create_time = tmp_time

					newsModel.save()
					return json_result(message=u'修改新闻成功!')
				else:
					return json_params_error(message=u'文章标题不能为空!')
		else:
			return json_params_error(message=u'你尝试查看一篇不存在的新闻!')
	else:
		return json_params_error(message=u'你尝试访问一篇不存在的新闻!')

#删除研究进展文章
@login_required
def delete_news(request,news_id=0):
	try:
		newsId = int(news_id)
	except:
		pass

	if newsId:
		newsModel = NewsModel.objects.filter(pk=newsId, status__in=[1, 2, 3]).first()
		if newsModel:
			newsModel.status = 0
			newsModel.save()
			return json_result(message=u'删除新闻成功!')
		else:
			return json_params_error(message=u'你尝试查看一篇不存在的新闻!')
	else:
		return json_params_error(message=u'你尝试访问一篇不存在的新闻!')

#研究进展文章列表
@login_required
def news(request,page=1,category_id=0):
	try:
		currentPage = int(page)
		categoryId = int(category_id)
	except:pass

	numPage = int(configs.PC_FRONT_NUM_PAGE)
	start = (currentPage -1)*numPage
	end = start +numPage

	if categoryId:
		newsCategoryModel = NewsCategoryModel.objects.filter(pk=categoryId).first()
		if newsCategoryModel:
			newsModel = NewsModel.objects.filter(status__in=[1,2,3],category=newsCategoryModel).all()
		else:
			newsModel = NewsModel.objects.filter(status__in=[1,2,3]).all()
	else:
		newsModel = NewsModel.objects.filter(status__in=[1,2,3]).all()

	if newsModel:

		newsCount = newsModel.count()

		pageCount = newsCount /numPage
		if newsCount % numPage>0:
			pageCount +=1

		news_list= []
		for n in newsModel:
			if n.category:
				category = n.category.category
			else:
				category = None
			news_list.append({
				'id': n.id,
				'title': n.title,
				'category': category,
				'create_time': n.create_time,
			})

		context= {
			'current_page':currentPage,
			'page_count':pageCount,
			'news':news_list[start:end],
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无研究进展列表!')

#添加热门文章
@login_required
def add_hold_news(request,news_id=0,type_id=1):
	'''
		mark:
			typeId 用来区分热门文章推送到左侧大banner还是右侧列表
			typeId : 1= 推荐到右侧列表  2=推荐到banner
	'''
	try:
		newsId = int(news_id)
		typeId = int(type_id)
	except:pass

	if newsId:
		if typeId in [1,2]:
			newsModel = NewsModel.objects.filter(pk = newsId,status__in=[1,2]).first()
			if newsModel:
				holdNewsModel = HoldNewsModel(news=newsModel,type=typeId)
				holdNewsModel.save()
				return json_result(message=u'成功添加热门文章!')
			else:
				return json_params_error(message=u'你尝试查看一篇不存在的文章!')
		else:
			return json_params_error(message=u'你尝试选择一个不存在的类型!')
	else:
		return json_params_error(message=u'你尝试访问一篇不存在的文章!')

#删除热门文章
@login_required
def delete_hold_news(request,news_id=0,type_id=1):
	try:
		newsId = int(news_id)
		typeId = int(type_id)
	except:
		pass

	if newsId:
		newsModel = NewsModel.objects.filter(pk=newsId).first()
		if newsModel:
			holdNewsModel = HoldNewsModel.objects.filter(news=newsModel,type=typeId).first()
			if holdNewsModel:
				holdNewsModel.delete()
				return json_result(message=u'文章取消推荐成功!')
			else:
				return json_params_error(message=u'此文章不是热门文章!')
		else:
			return json_params_error(message=u'你尝试选择一个不存在的文章!')
	else:
		return json_params_error(message=u'你尝试访问一篇不存在的文章!')

#研究进展热门文章列表
@login_required
def hold_news(request,type_id=0):
	try:
		typeId = int(type_id)
	except:pass

	if typeId in [1,2]:
		holdNewsModel = HoldNewsModel.objects.filter(type=typeId).all()
	else:
		holdNewsModel = HoldNewsModel.objects.all()

	if holdNewsModel:
		hold_news_list=[]
		for h in holdNewsModel:
			if h.news.category:
				category = h.news.category.category
			else:
				category = None

			hold_news_list.append({
				'id':h.news.id,
				'title':h.news.title,
				'type':h.type,
				'category':category,
			})
		context ={
			'hold_news':hold_news_list,
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无热门文章!')

#添加研究进展相关阅读
@login_required
def add_news_related_reading_articles(request,news_id=0,article_id=0,type_id=1):
	'''
		mark:
		    研究进展的相关阅读是关联研究方法和研究进展两站表
		    由于文章id可能重复，因此通过typeId 来区分不同表
	'''
	try:
		newsId = int(news_id)
		articleId = int(article_id)
		typeId = int(type_id)
	except:
		pass

	if newsId and articleId and typeId:
		newsModel = NewsModel.objects.filter(pk=newsId).first()
		if newsModel:
			# 根据typeId在对应的表中搜索是否有相关的文章,如果有则保存。
			if typeId == 1:
				articleModel = MethodArticleInfoModel.objects.filter(status__in=[1, 2], pk=articleId).first()
			elif typeId == 2:
				articleModel = NewsModel.objects.filter(status__in=[1,2],pk=articleId).first()
			else:
				return json_params_error(message=u'你尝试选择一种不存在的文章类型!')

			#如果检索出的文章存在,则保存
			if articleModel:
				newsRelatedReadingModel = NewsRelatedReadingModel(related_news=newsModel, related_reading_article=articleId, type=typeId)
				newsRelatedReadingModel.save()
				return json_result(message=u'成功添加相关阅读!')
		else:
			return json_params_error(message=u'你尝试关联一篇不存在的文章!')
	else:
		return json_params_error(message=u'文章id或类型不能为空!')

#删除研究进展相关阅读
@login_required
def delete_news_related_reading(request,news_related_reading_id=0):
	try:
		newsRelatedReadingId = int(news_related_reading_id)
	except:
		pass

	if newsRelatedReadingId:
		newsRelatedReadingModel = NewsRelatedReadingModel.objects.filter(pk=newsRelatedReadingId).first()
		if newsRelatedReadingModel:
			newsRelatedReadingModel.delete()
			return json_result(message=u'成功删除相关阅读文章!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的文章列表!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的文章列表!')

#研究进展相关阅读文章列表
@login_required
def news_related_reading_article_list(request,news_id=0):
	try:
		newsId = int(news_id)
	except:
		pass

	if newsId:
		newsModel = NewsModel.objects.filter(status__in=[1,2],pk=newsId).first()
		if newsModel:
			newsRelatedReadingModel = NewsRelatedReadingModel.objects.filter(related_news=newsModel).all()

			if newsRelatedReadingModel:
				article_list=[]
				for r in newsRelatedReadingModel:
					if r.type == 1:
						related_article = MethodArticleInfoModel.objects.get(pk=r.related_reading_article).title
					else:
						related_article = NewsModel.objects.get(pk = r.related_reading_article).title
					article_list.append({
						'id':r.id,
						'article_id':r.related_reading_article, #用于后台数据关联(搜索出来的数据和相关阅读文章数据关联)
						'related_article':related_article,
						'type':r.type,
					})

				context = {
					'news_realted_reading': article_list,
				}
				return json_result(data=context)
			else:
				return json_params_error(message=u'暂无相关阅读文章!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的文章!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的文章!')

#搜索研究进展文章
@login_required
@require_http_methods(['GET','POST'])
def search_news(request,page=1):
	try:
		currentPage = int(page)
	except:
		pass

	numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
	start = (currentPage - 1) * numPage
	end = start + numPage

	if request.method == 'GET':
		return json_result(message=u'研究进展的搜索页面!')
	else:
		searchKeyWords = request.POST.get('search_key_words', None)

		if searchKeyWords:
			newsModel = NewsModel.objects.filter(status__in=[1, 2], title__icontains=searchKeyWords).all()

			newsCount = newsModel.count()
			# 求总页数
			pageCount = newsCount / numPage
			if newsCount % numPage:
				pageCount += 1

			newsModel = list(newsModel)[start:end]

			news_list = []
			for n in newsModel:
				if n.category:
					category = n.category.category
				else:
					category = None

				news_list.append({
					'id':n.id,
					'title':n.title,
					'category':category,
					'create_time':n.create_time,
				})

			context = {
				'news': news_list,
				'current_page': currentPage,
				'page_count': pageCount,
			}
			return json_result(data=context)
		else:
			return json_params_error(message=u'请输入搜索的关键词!')

#搜索研究方法和研究进展文章
@login_required
@require_http_methods(['GET','POST'])
def search_methods_and_news_articles(request,page=1):
	'''
		mark:
			由于搜索是将研究方法和研究进展两张表混合搜索
			因此需要区分搜索结果数据的来源，已做不同详情页面跳转
			给数据新增类型type : 1=研究方法 2=研究进展
	'''
	try:
		currentPage = int(page)
	except:pass

	numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
	start = (currentPage -1) *numPage
	end = start +numPage

	if request.method == 'GET':
		return json_result(message=u'研究进展的搜索页面!')
	else:
		searchKeyWords = request.POST.get('search_key_words',None)

		if searchKeyWords:
			articles_list = []

			methodModel = MethodArticleInfoModel.objects.filter(status__in=[1,2],title__icontains=searchKeyWords).all()
			if methodModel:
				for m in methodModel:
					articles_list.append({
						'id': m.id,
						'title': m.title,
						'create_time': m.create_time,
						'type': 1,  # 给研究方法模型添加数据来源类型
					})

			newsModel = NewsModel.objects.filter(status__in=[1,2],title__icontains=searchKeyWords).all()
			if newsModel:
				for n in newsModel:
					articles_list.append({
						'id': n.id,
						'title': n.title,
						'create_time': n.create_time,
						'type': 2,
					})

			# 按照文章的创建时间排序
			articles = sorted(articles_list, key=lambda x: (x['create_time']), reverse=True)

			articlesCount = len(articles)

			#计算总页数
			pageCount = articlesCount / numPage
			if articlesCount % numPage:
				pageCount +=1

			context = {
				'articleModel': articles[start:end],
				'current_page':currentPage,
				'page_count':pageCount,
			}
			return json_result(data=context)
		else:
			return json_params_error(message=u'请输入搜索的关键词!')

#研究进展评论列表
@login_required
def news_comments(request,page=1):
	try:
		currentPage = int(page)
	except:pass

	numPage = int(configs.NUM_PAGE)
	start = (currentPage -1 )*numPage
	end = start +numPage

	commentsModel = NewsCommentModel.objects.filter(status=1).all()
	if commentsModel:
		commentsCount = commentsModel.count()

		pageCount = commentsCount /numPage
		if commentsCount % numPage >0:
			pageCount +=1

		commentsModel = list(commentsModel)[start:end]
		comments_list=[]
		for c in commentsModel:
			comments_list.append({
				'id':c.id,
				'username':c.author.username,
				'comment':c.comment,
				'create_time':c.create_time,
			})
		context ={
			'comments':comments_list,
			'page_count':pageCount,
			'current_page':currentPage,
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无任何评论!')

#删除研究进展评论
def delete_news_comment(request):
	commentId = request.POST.get('comment_id',None)

	try:
		commentId = int(commentId)
	except:pass

	if commentId:
		commentModel = NewsCommentModel.objects.filter(pk=commentId).first()
		if commentModel:
			commentModel.delete()
			return json_result(message=u'成功删除评论!')
		else:
			return json_params_error(message=u'你尝试删除一个不存在的评论!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的评论!')

'''
	author:zhangx
	date:20180426
	mark:
		1、新增视频管理模块
'''
#添加视频课程
@login_required
@require_http_methods(['GET', 'POST'])
def add_course(request):
	if request.method == 'GET':
		return json_result(message=u'添加课程页面!')
	else:
		course = request.POST.get('course',None)
		courseIntro = request.POST.get('course_intro',None)
		teachIntro = request.POST.get('teach_intro',None)
		thumbnail = request.POST.get('thumbnail',None)
		price = request.POST.get('price',None)

		logger.info({
			'course': course,
			'courseIntro': courseIntro,
			'teachIntro': teachIntro,
			'thumbnail': thumbnail,
			'price': price,
		})

		if not course:
			return json_params_error(message=u'课程名称不能为空!')

		try:
			course = str(course).strip()
		except:
			pass

		#把课程名称保存到MethodCategoryModel中,设置type=2
		courseModel = MethodCategoryModel(category=course,type=2)
		courseModel.save()

		courseInfoModel = CourseModel(course=courseModel,course_intro=courseIntro,teach_intro=teachIntro,thumbnail=thumbnail,price=price)
		courseInfoModel.save()

		context={
			'course_id': courseInfoModel.id,
		}
		return json_result(message=u'成功添加课程信息!',data=context)


#修改课程信息
@login_required
@require_http_methods(['GET', 'POST'])
def alter_course(request,course_id=0):
	try:
		courseId = int(course_id)
	except:pass

	if courseId:
		courseModel = CourseModel.objects.filter(pk=courseId).first()
		if courseModel:
			if request.method == 'GET':
				context = {
					'id':courseModel.id,
					'course':courseModel.course.category,
					'course_intro':courseModel.course_intro,
					'teach_intro':courseModel.teach_intro,
					'thumbnail':courseModel.thumbnail,
					'price':courseModel.price,
				}
				return json_result(data=context)
			else:
				course = request.POST.get('course', courseModel.course.category)
				courseIntro = request.POST.get('course_intro', courseModel.course_intro)
				teachIntro = request.POST.get('teach_intro', courseModel.teach_intro)
				thumbnail = request.POST.get('thumbnail', courseModel.thumbnail)
				price = request.POST.get('price',courseModel.price,)

				try:
					course = str(course).strip()
				except:
					pass

				if not course:
					return json_params_error(message=u'课程名称不能为空!')

				#课程名字在methodCategoryModel中保存
				methodCategoryModel = courseModel.course
				methodCategoryModel.category = course
				methodCategoryModel.save(update_fields = ['category'])

				courseModel.course_intro = courseIntro
				courseModel.teach_intro = teachIntro
				courseModel.thumbnail = thumbnail
				courseModel.price = price
				courseModel.save()

				return json_result(message=u'成功修改课程信息!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的课程!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的课程!')

#课程列表
def course_list(request):
	courseModel = CourseModel.objects.all().order_by('-create_time')
	if courseModel:
		courseList=[]
		for c in courseModel:
			courseList.append({
				'id':c.id,
				'course_id':c.course.id,
				'course':c.course.category,
				'thumbnail':c.thumbnail,
			})

		context = {
			'course_list': courseList,
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无课程!')

#课程章节列表
def course_section(request):
	courseSectionModel = MethodCategoryModel.objects.filter(type=2,is_active=1,relevance_category__isnull=False ).values('id','category')

	context = {
		'course_list': list(courseSectionModel)
	}
	return json_result(data=context)

#章节关联课时视频列表
@login_required
def course_video(request,course_id=0):
	try:
		courseId = int(course_id)
	except:pass
	if not courseId:
		return json_params_error(message=u'请选择课程章节!')

	courseModel = MethodCategoryModel.objects.filter(pk=courseId,type=2,is_active=1).first()
	if not courseModel:
		return json_params_error(message=u'你尝试查看一个不存在的课程章节!')

	videoModel = VideoModel.objects.filter(status__in=[1,2],course=courseModel).all()
	if videoModel:
		tmp_video=[]
		for v in videoModel:
			tmp_video.append({
				'video_id': v.id,
				'title': v.title,
			})
		return  json_result(data=tmp_video)
	else:
		return json_params_error(message=u'此课程下暂无关联的课时!')

#添加视频信息
@login_required
@require_http_methods(['GET', 'POST'])
def add_video(request):
	if request.method == 'GET':
		return json_result(u'添加视频页面!')
	else:

		now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

		title = request.POST.get('title',None)
		courseMain = request.POST.get('course_main',None)
		summary = request.POST.get('summary',None)
		courseId = request.POST.get('course_id',None)
		polyvId = request.POST.get('polyv_id',None)
		status = request.POST.get('status',2)
		isPay = request.POST.get('is_pay',0)
		videoTime = request.POST.get('video_time',None)
		createTime = request.POST.get('create_time', now_time)
		thumbnail = request.POST.get('thumbnail',None)
		videoRelatedData = request.POST.getlist('video_related_data',None)
		teacherIntroduction = request.POST.get('teacher_introduction','')


		logger.info({
			'title':title,
			'video_related_data':videoRelatedData,
		})
		try:
			tmp_create_time = time.strptime(createTime, "%Y-%m-%d %H:%M:%S")
			Y, m, d, H, M, S = tmp_create_time[0:6]
			tmp_time = datetime.datetime(Y, m, d, H, M, S)
		except:
			pass
		if not title:
			return json_params_error(message=u'请填写视频标题!')

		course=None
		if courseId:
			courseModel = MethodCategoryModel.objects.filter(pk=courseId,is_active=1,type=2,relevance_category__isnull=False).first()
			if courseModel:
				course = courseModel
			else:
				return json_params_error(message=u'你尝试选择一个不存在的分类!')

		videoModel = VideoModel(author=request.user,title=title,summary=summary,course=course,course_main=courseMain,polyv_vid=polyvId,status=status,is_pay=isPay,video_time=videoTime,thumbnail=thumbnail,create_time=tmp_time,teacher_introduction=teacherIntroduction)
		# videoModel = VideoModel(title=title, summary=summary, course=course, course_main=courseMain, polyv_vid=polyvId, status=status, is_pay=isPay, video_time=videoTime, thumbnail=thumbnail, create_time=tmp_time)
		videoModel.save()

		if videoRelatedData:
			for v in videoRelatedData:
				v = str(v).strip()
				if v:
					videoRelatedDataModel = VideoRelatedDataModel(video=videoModel,file_name=v)
					videoRelatedDataModel.save()
		context ={
			'video_id':videoModel.id,
		}
		return json_result(message=u'添加视频信息成功!',data=context)

#修改视频信息
@login_required
@require_http_methods(['GET', 'POST'])
def alter_video(request,video_id=0):
	try:
		videoId = int(video_id)
	except:pass

	if videoId:
		videoModel = VideoModel.objects.filter(pk = videoId,status__in=[1,2]).first()
		# 获取视频关联的相关资料
		videoRelatedDataModel = VideoRelatedDataModel.objects.filter(video=videoModel)

		if videoModel:
			if request.method == 'GET':

				context = {
					'video_id':videoModel.id,
					'title':videoModel.title,
					'course':videoModel.course.category,
					'course_id':videoModel.course.id,
					'course_main':videoModel.course_main,
					'summary':videoModel.summary,
					'polyv_vid':videoModel.polyv_vid,
					'status':videoModel.status,
					'is_pay':videoModel.is_pay,
					'video_time':videoModel.video_time,
					'thumbnail':videoModel.thumbnail,
					'create_time':videoModel.create_time,
					'video_related_data':list(videoRelatedDataModel.values('id', 'file_name')),
					'teacher_introduction':videoModel.teacher_introduction,
				}
				return json_result(data=context)
			else:

				tmp_video_data=[]
				if videoRelatedDataModel:
					for v in videoRelatedDataModel:
						tmp_video_data.append(v.file_name)

				title = request.POST.get('title', videoModel.title)
				courseMain = request.POST.get('course_main', videoModel.course_main)
				summary = request.POST.get('summary', videoModel.summary)
				courseId = request.POST.get('course_id', videoModel.course.id)
				polyvId = request.POST.get('polyv_id', videoModel.polyv_vid)
				status = request.POST.get('status', videoModel.status)
				isPay = request.POST.get('is_pay', videoModel.is_pay)
				videoTime = request.POST.get('video_time', videoModel.video_time)
				thumbnail = request.POST.get('thumbnail',videoModel.thumbnail)
				createTime = request.POST.get('create_time', videoModel.create_time)
				videoRelatedData = request.POST.getlist('video_realted_data', tmp_video_data)
				teacherIntroduction = request.POST.get('teacher_introduction',videoModel.teacher_introduction)

				now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

				logger.info({
					'title':title,
					'courseMain': courseMain,
					'summary':summary,
					'courseId':courseId,
					'polyvId':polyvId,
					'status':status,
					'isPay':isPay,
					'videoTime':videoTime,
					'thumbnail':thumbnail,
					'createTime':createTime,
					'videoRelatedData':videoRelatedData,
					'teacherIntroduction':teacherIntroduction,
				})

				tmp_time = now_time
				if createTime:
					try:
						tmp_create_time = time.strptime(createTime, "%Y-%m-%d %H:%M:%S")
						Y, m, d, H, M, S = tmp_create_time[0:6]
						tmp_time = datetime.datetime(Y, m, d, H, M, S)
					except:pass

				if not title:
					return json_params_error(message=u'请填写视频标题!')

				course = None
				if courseId:
					courseModel = MethodCategoryModel.objects.filter(pk=courseId, is_active=1, type=2, relevance_category__isnull=False).first()
					if courseModel:
						course = courseModel
					else:
						return json_params_error(message=u'你尝试选择一个不存在的分类!')

				videoModel.title = title
				videoModel.course_main = courseMain
				videoModel.summary = summary
				videoModel.course = course
				videoModel.polyv_vid = polyvId
				videoModel.status = status
				videoModel.is_pay = isPay
				videoModel.thumbnail = thumbnail
				videoModel.video_time = videoTime
				videoModel.create_time = tmp_time
				videoModel.teacher_introduction = teacherIntroduction
				videoModel.save()

				if videoRelatedData:

					for v in videoRelatedData:
						v = str(v).strip()
						if v:
							videoRelatedDataModel = VideoRelatedDataModel.objects.filter(video=videoModel,file_name=v).first()
							if not videoRelatedDataModel:
								tmpVideoDataModel = VideoRelatedDataModel(video=videoModel,file_name=v)
								tmpVideoDataModel.save()

				return json_result(message=u'成功修改视频信息!')
		else:
			return json_params_error(message=u'你尝试查看一个不存在的视频!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的视频!')

#删除视频
@login_required
def delete_video(request,video_id=0):
	try:
		videoId = int(video_id)
	except:
		pass

	if videoId:
		videoModel = VideoModel.objects.filter(pk=videoId,status__in=[1,2]).first()
		if videoModel:
			videoModel.status = 0
			videoModel.save()
			return json_result(message=u'成功删除视频!')
		else:
			return json_params_error(message=u'你尝试删除一个不存在的视频!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的视频!')


#删除视频相关资料
@login_required
def delete_video_related_data(request,video_data_id=0):
	try:
		videoDataId = int(video_data_id)
	except:pass

	if videoDataId:
		videoRelatedDataModel = VideoRelatedDataModel.objects.filter(pk = videoDataId).first()
		if videoRelatedDataModel:
			videoRelatedDataModel.delete()
			return json_result(message=u'成功删除视频资料!')
		else:
			return json_params_error(message=u'你尝试删除一个不存在的视频资料!')
	else:
		return json_params_error(message=u'你尝试删除一个不存在的视频资料!')

#视频评论列表
@login_required
def video_comments(request, page=1):
	try:
		currentPage = int(page)
	except:
		pass

	numPage = int(configs.PC_ADMIN_ARTICLE_NUM_PAGE)
	start = (currentPage - 1) * numPage
	end = start + numPage

	commentsModel = VideoCommentModel.objects.all()
	if commentsModel:
		commentsCount = commentsModel.count()

		pageCount = commentsCount / numPage
		if commentsCount % numPage > 0:
			pageCount += 1

		commentsModel = list(commentsModel)[start:end]
		comments_list = []
		for c in commentsModel:
			comments_list.append({
				'id': c.id,
				'username': c.username.username,
				'comment': c.comment,
				'create_time': c.create_time,
			})
		context = {
			'comments': comments_list,
			'page_count': pageCount,
			'current_page': currentPage,
		}
		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无任何评论!')


#删除视频评论
@login_required
def delete_video_comment(request,comment_id=0):

	try:
		commentId = int(comment_id)
	except:
		pass

	if commentId:
		commentModel = VideoCommentModel.objects.filter(pk=commentId).first()
		if commentModel:
			childCommentModel = VideoCommentModel.objects.filter(relevance_comment=commentModel).all()
			if childCommentModel:
				childCommentModel.delete()
			commentModel.delete()
			return json_result(message=u'成功删除评论!')
		else:
			return json_params_error(message=u'你尝试删除一个不存在的评论!')
	else:
		return json_params_error(message=u'你尝试访问一个不存在的评论!')

#搜索视频评论
@login_required
@require_http_methods(['GET','POST'])
def search_video_comment(request,page=1):
	try:
		currentPage = int(page)
	except:
		pass

	numPage = int(configs.NUM_PAGE)
	start = (currentPage - 1) * numPage
	end = start + numPage

	if request.method == 'GET':
		return json_result(message=u'搜索视频评论页面!')
	else:
		comment  =  request.POST.get('comment',None)

		commentsModel = VideoCommentModel.objects.filter(comment__icontains=comment).all()
		if commentsModel:
			commentsCount = commentsModel.count()

			pageCount = commentsCount / numPage
			if commentsCount % numPage > 0:
				pageCount += 1

			commentsModel = list(commentsModel)[start:end]
			comments_list = []
			for c in commentsModel:
				comments_list.append({
					'id': c.id,
					'username': c.username.username,
					'comment': c.comment,
					'create_time': c.create_time,
				})
			context = {
				'comments': comments_list,
				'page_count': pageCount,
				'current_page': currentPage,
			}
			return json_result(data=context)
		else:
			return json_params_error(message=u'暂无任何评论!')

#交易订单列表
@login_required
def order_list(request,page=1):

	try:
		currentPage = int(page)
	except:pass

	ordersModel = UserBuyOrderModel.objects.all()

	#订单已支付总金额
	amountCount = 0
	amountModel = ordersModel.filter(status=2).all()

	if amountModel:
		for a in amountModel:
			amountCount += a.price

	if ordersModel:
		orderCount = ordersModel.count()

		numPage = int(configs.NUM_PAGE)
		start = (currentPage -1) *numPage
		end = start +numPage

		pageCount = orderCount /numPage
		if orderCount % numPage >0:
			pageCount +=1

		tmp_order_list = []
		for r in ordersModel:
			#获取课程名称
			course = r.content_object.category

			tmp_order_list.append({
				'order_id':r.order_id,
				'course':course,
				'username':r.username.username,
				'price':r.price,
				'type':r.type,
				'relevance_order':r.relevance_order,
				'status':r.status,
			})

		context ={
			'order_list':tmp_order_list[start:end],
			'page_count':pageCount,
			'current_page':currentPage,
			'amount':amountCount,
		}

		return json_result(data=context)
	else:
		return json_params_error(message=u'暂无订单!')

#订单查询
@login_required
def search_order(request,page=1):
	if request.method == 'GET':
		return json_result(message=u'订单查询页面!')
	else:
		startTime = request.POST.get('start_time',None)
		endTime = request.POST.get('end_time',None)
		status = request.POST.get('status',None)
		course = request.POST.get('course',None)

		logger.info({
			'startTime':startTime,
			'endTime':endTime,
			'status':status,
		})

		if (startTime and not endTime) or (not startTime and endTime):
			return json_params_error(message=u'开始/结束时间不能为空')

		tmp_start_time = None
		tmp_end_time = None

		try:
			tmp_s_time = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")  # strptime 根据指定格式将字符串解析成时间元祖
			Y, m, d, H, M, S = tmp_s_time[0:6]

			tmp_start_time = datetime.datetime(Y, m, d, H, M, S)

		except:
			pass

		try:
			tmp_e_time = time.strptime(endTime, "%Y-%m-%d %H:%M:%S")  # strptime 根据指定格式将字符串解析成时间元祖
			Y, m, d, H, M, S = tmp_e_time[0:6]

			tmp_end_time = datetime.datetime(Y, m, d, H, M, S)
		except:
			pass

		#如果课程为真,则查询课程模型
		if not course:
			return json_params_error(message=u'请选择课程!')
		else:
			try:
				course = int(course)
			except:pass

			courseModel = MethodCategoryModel.objects.filter(is_active=1,pk=course).first()
			if not courseModel:
				return json_params_error(message=u'你尝试查看一个不存在的课程!')

		try:
			status = str(status)
		except:pass

		if status in ['0','1','2']:
			try:
				status = int(status)
			except:pass

			ordersModel = UserBuyOrderModel.objects.filter(
				Q(create_time__gte=tmp_start_time) &
			    Q(create_time__lte=tmp_end_time) &
			    Q(status=int(status))
			).all()

		else:
			ordersModel = UserBuyOrderModel.objects.filter(
				Q(create_time__gte=tmp_start_time) &
				Q(create_time__lte=tmp_end_time)
			).all()

		tmp_model = []
		if not ordersModel:
			return json_params_error(message=u'暂无相关订单!')
		else:
			for r in ordersModel:
				if r.content_object == courseModel:
					tmp_model.append(r)
		try:
			currentPage = int(page)
		except:
			pass

		orderCount = len(tmp_model)

		numPage = int(configs.NUM_PAGE)
		start = (currentPage - 1) * numPage
		end = start + numPage

		pageCount = orderCount / numPage
		if orderCount % numPage > 0:
			pageCount += 1

		tmp_order_list = []
		amountCount =0
		for r in tmp_model:
			# 获取课程名称
			course = r.content_object.category

			if r.status ==2:
				amountCount += r.price

			tmp_order_list.append({
				'order_id': r.order_id,
				'course': course,
				'username': r.username.username,
				'price': r.price,
				'type': r.type,
				'relevance_order': r.relevance_order,
				'status': r.status,
			})

		context = {
			'order_list': tmp_order_list[start:end],
			'page_count': pageCount,
			'current_page': currentPage,
			'amount':amountCount,
		}

		return json_result(data=context)

# 支付宝订单状态校验
@login_required
def supervisor_alipay_order_status(request, order_id=0):
	return api.front.views.alipay_order_status(request,order_id=order_id)

#用户意见反馈列表
@login_required
def user_feed_back(request,page=1):
	try:
		currentPage = int(page)
	except:pass

	numPage = int(configs.NUM_PAGE)
	start = (currentPage -1)*numPage
	end = start +numPage

	userFeedBack = UserFeedBack.objects.all().values('id','content','image','iphone','username__username','create_time')

	userFeedBackCount = userFeedBack.count()

	pageCount = userFeedBackCount / numPage
	if userFeedBackCount % numPage > 0 :
		pageCount +=1

	userFeedBack = list(userFeedBack)

	context = {
		'user_feed_back_list':userFeedBack,
		'current_page':currentPage,
		'page_count':pageCount,
	}
	return json_result(data=context)

#反馈详情
@login_required
def user_feed_back_detail(request,id=0):
	try:
		Id = int(id)
	except:pass

	if Id:
		userFeedBackDetail = UserFeedBack.objects.filter(pk=Id).first()
		if userFeedBackDetail:
			context = {
				'id': userFeedBackDetail.id,
				'username': userFeedBackDetail.username.username,
				'content': userFeedBackDetail.content,
				'image': userFeedBackDetail.image,
				'iphone': userFeedBackDetail.iphone,
				'create_time': userFeedBackDetail.create_time,
			}
		return json_result(data=context)
	else:
		return json_params_error(message=u'你尝试查看一个不存在的反馈!')

# 获取勋章列表
@login_required
@require_http_methods(['GET'])
def get_medal(request):
	
	medals = medalModel.objects.all()

	if not medals:
		return json_result(message=u'请求成功',data = [])

	medals = list(medals.values())
	
	return json_result(message=u'请求成功',data = medals)

#添加勋章
@login_required
@require_http_methods(['POST'])
def add_medal(request):
	name = request.POST.get('name', None)
	uid = request.POST.get('uid', None)
	pic_url = request.POST.get('pic_url', None)
	
	if not name :
		return  json_params_error(message=u'勋章name缺失')
	if not uid :
		return  json_params_error(message=u'勋章uid缺失')
	if not pic_url :
		return  json_params_error(message=u'勋章pic_url缺失')

	is_valid = request.POST.get('is_valid', None)
	medal_type = request.POST.get('medal_type',0)
	description = request.POST.get('description','')
	try:
		if(is_valid == '0'):
			is_valid = False
		else:
			is_valid = True
		medal_type = int(medal_type)
	except :pass

	medal = medalModel(name = name,uid = uid,is_valid = is_valid,medal_type = medal_type,pic_url = pic_url,description = description)
	medal.save()

	return json_result(message=u'勋章添加成功')

#删除勋章
@login_required
@require_http_methods(['POST'])
def delete_medal(request):

	uid = request.POST.get('uid', None)

	medal = medalModel.objects.filter(uid = uid)

	if not medal:
		return json_params_error(message=u'要删除的勋章不存在')
	
	medal.delete()

	return json_result(message=u'删除勋章成功')

#获取留言列表
@login_required
@require_http_methods(['GET'])
def get_activity_comments(request,topic_type = 'twoYear', page = 1,pagesize = 5,show_which = '0'):
	if show_which == '0':
		comments = specialTopicCommentModel.objects.filter(is_publish = False)
	elif show_which == '1':
		comments = specialTopicCommentModel.objects.filter(is_publish = True)
	else:
		comments = specialTopicCommentModel.objects.all()
	comments_list = list(comments.values())
	# 挂载user信息
	for i,comment in enumerate(comments):
		comments_list[i]['user'] = {}
		comments_list[i]['user']['username'] = comment.user.username
		comments_list[i]['user']['avatar'] = comment.user.avatar
		try:
			reply = comments[i].specialtopiccommentreplymodel
		except:
			continue
		comments_list[i]['reply'] = {}
		comments_list[i]['reply']['content'] = reply.reply_content
		comments_list[i]['reply']['user_name'] = reply.reply_user
		
   	paginator = Paginator(comments_list, pagesize)
	try:
		comments_list = paginator.page(page)
	except PageNotAnInteger:
        # 如果page不是整数，则展示第1页
		comments_list = paginator.page(1)
	except EmptyPage:
        # 如果page超过范围，则展示最后一页
		comments_list = paginator.page(paginator.num_pages)
		page = int(paginator.num_pages)
		
	context = {
		'page':page,
		'pagesize':pagesize,
		'comments':list(comments_list.object_list),
		'page_count':paginator.num_pages
	}
	
	return json_result(message=u'请求成功',data = context)

# 修改留言展示状态(获得医咖会的朋友勋章)
@login_required
@require_http_methods(['GET'])
def change_activity_comment_state(request,comment_id = 0,state = '0'):
	try:
		comment = specialTopicCommentModel.objects.get(pk = comment_id)
	except:
		return json_params_error(message=u'留言不存在')
		
	if state == '0':
		comment.is_publish = False
		comment.save()
		# 不收回勋章
		return json_result(message=u'修改成功')
	elif state == '1':
		comment.is_publish = True
		comment.save()
		try:
			userMedalModel(user = comment.user,medal = medalModel.objects.get(uid = 'positive_man')).save()
		except:
			return json_result(message=u'用户已获得过勋章')
		return json_result(message=u'修改成功')
	else:
		return json_params_error(message=u'state参数不合法')
	
# 获取sci成员信息
@login_required
@require_http_methods(['GET'])
def get_sci_member(request,anniversary_times = 2):

	medal = medalModel.objects.get(uid = 'sci_god')
	#过滤掉被剥夺勋章的用户
	sci_user_list = userMedalModel.objects.filter(medal = medal,is_disabled = False).values_list('user_id',flat=True)
	sci_users_data = list(anniversaryModel.objects.filter(user__in = sci_user_list,anniversary_times = int(anniversary_times)).values())

	for i,sci_user_data in  enumerate(sci_users_data):
		sci_users_data[i]['data'] = json.loads(sci_user_data['data'])
		user = FrontUserModel.objects.get(pk = sci_user_data['user_id'])
		sci_users_data[i]['user'] = {}
		sci_users_data[i]['user']['email'] = user.email
		sci_users_data[i]['user']['avatar'] = user.avatar
		sci_users_data[i]['user']['gender'] = u'男' if user.gender == 0 else u'女'
		sci_users_data[i]['user']['username'] = user.username

	context = sci_users_data


	return json_result(message=u'请求成功',data = context)

# 获取医咖会朋友信息
@login_required
@require_http_methods(['GET'])
def get_friend_member(request,anniversary_times = 2):

	medal = medalModel.objects.get(uid = 'yizhu_friend')
	sci_medal = medalModel.objects.get(uid = 'sci_god')
	user_list = userMedalModel.objects.filter(medal = medal).values_list('user_id',flat=True)
	friends = anniversaryModel.objects.filter(user__in = user_list,anniversary_times = int(anniversary_times))
	friends_list = list(friends.values())
	friends_list_show = []
	for friend in friends_list:
		friend['data'] = json.loads(friend['data'])
		if friend['data']['is_writer'] == 1 or friend['data']['is_liaison'] == 1:
			friend['user'] = {}
			user = FrontUserModel.objects.get(pk = friend['user_id'])
			user_sci = user.usermedalmodel_set.filter(medal = sci_medal,is_disabled = False).first()
			if not user_sci:
				friend['data']['sci'] = {}
			else:
				friend['data']['sci'] = model_to_dict(user_sci)
			friend['user']['username'] = user.username
			friend['user']['email'] = user.email
			friend['user']['avatar'] = user.avatar
			friend['user']['gender'] = u'男' if user.gender == 0 else u'女'
			friends_list_show.append(friend)

	context = friends_list_show

	return json_result(message=u'请求成功',data = context)

# 剥夺用户勋章
@login_required
@require_http_methods(['GET'])

def disable_user_medal(request,medal_type,user_id):

	if medal_type == 'sci':
		medal = medalModel.objects.get(uid = 'sci_god')
		user_medal = userMedalModel.objects.filter(medal = medal,user = int(user_id))
		if not user_medal:
			return json_params_error(message = u'用户没有SCI勋章')
		user_medal.update(is_disabled = True)
		return json_result(message=u'sci勋章剥夺成功')
	elif medal_type == 'all':
		user_medals = userMedalModel.objects.filter(user = int(user_id))
		if not user_medals:
			return json_params_error(message = u'用户没有勋章')
		user_medals.update(is_disabled = True)
		return json_result(message=u'全部勋章剥夺成功')
	else:
		return json_params_error(message=u'medal_type只能为sci或all')

# 恢复用户勋章
@login_required
@require_http_methods(['GET'])

def restore_user_medal(request,medal_type,user_id):

	if medal_type == 'sci':
		medal = medalModel.objects.get(uid = 'sci_god')
		user_medal = userMedalModel.objects.filter(medal = medal,user = int(user_id))
		if not user_medal:
			return json_params_error(message = u'用户未获得过SCI勋章')
		user_medal.update(is_disabled = False)
		return json_result(message=u'sci勋章恢复成功')
	elif medal_type == 'all':
		user_medals = userMedalModel.objects.filter(user = int(user_id))
		if not user_medals:
			return json_params_error(message = u'用户未获得过任何勋章')
		user_medals.update(is_disabled = False)
		return json_result(message=u'全部勋章恢复成功')
	else:
		return json_params_error(message=u'medal_type只能为sci或all')

# 留言回复
@login_required
@require_http_methods(['POST'])

def reply_user_comment(request):
	comment_id = request.POST.get('comment_id', None)
	content = request.POST.get('content', None)
	reply_user = request.POST.get('reply_user', None)

	if not comment_id :
		return json_params_error(message = u'comment_id缺失')
	if not content :
		return json_params_error(message = u'content缺失')
	if not reply_user :
		return json_params_error(message = u'reply_user缺失')

	comment = specialTopicCommentModel.objects.get(pk = int(comment_id))
	used_comment_reply = specialTopicCommentReplyModel.objects.filter(comment = comment).first()
	if not used_comment_reply:
		comment_reply = specialTopicCommentReplyModel(comment = comment,reply_content = content, reply_user = reply_user)
		comment_reply.save()
		return json_result(message=u'留言回复成功')
	used_comment_reply.reply_content = content
	used_comment_reply.reply_user = reply_user
	used_comment_reply.save()
	return json_result(message=u'留言更新成功')

#获取用户勋章信息
@login_required
@require_http_methods(['POST'])
def get_user_medal(request):
	user_id = request.POST.get('user_id', None)
	if (not user_id) or user_id == '':
		return json_params_error(message = u'user_id缺失')
	user_medals = userMedalModel.objects.filter(user = int(user_id))
	
	user_medals_list = list(user_medals.values())

	for index,user_medal in enumerate(user_medals):
		try :
			medal = user_medal.medal
		except:
			continue
		user_medals_list[index]['medal_name'] = medal.name

	context = user_medals_list

	return json_result(message=u'请求成功',data = context)






