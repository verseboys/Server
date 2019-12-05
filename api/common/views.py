#coding:utf-8

from extends.buildjson import json_params_error,json_result
import datetime,time
import logging
from questionsandanswersmodel.models import QuestionsModel,AnswersModel,AttentionQuestionModel,PraiseAnswerModel,CollectAnswerModel,MyMessagesModel,UserCollectCategoryModel
from frontmodel import configs
from frontmodel.models import FrontUserModel,UserFavoritesModel,UserPraiseModel
from videomodel.models import VideoModel,VideoCommentModel

logger = logging.getLogger(__name__)

# 计算评论时间周期
'''
	# 根据需求，评论的时间需要按照：
		1、小于10分钟,显示为：刚刚
		2、大于10分钟小于1小时为：*分钟前
		3、大于1小时小于24小时为：*小时之前
		4、大于1天小于1个月为：*天前
		5、大于1个月小于1年为：*月前
		6、大于1年为：*年前
'''

def comment_time_period(create_time):
	if create_time:

		now = datetime.datetime.now()
		# 转换成秒数计算相差
		seconds = (now - create_time).total_seconds()

		# 如果秒数小于10分钟，则返回刚刚
		if seconds:
			if seconds <= 60 * 10:
				return u'刚刚'
			elif seconds > 60 * 10 and seconds <= 60 * 60:
				minute = seconds / 60
				return u'%s分钟前' % int(minute)
			elif seconds > 60 * 60 and seconds <= 60 * 60 * 24:
				hours = seconds / (60 * 60)
				return u'%s小时之前' % int(hours)
			elif seconds > 60 * 60 * 24 and seconds <= 60 * 60 * 24 * 30:
				day = seconds / (60 * 60 * 24)
				return u'%s天前' % int(day)
			# elif seconds > 60 * 60 * 24 * 30 and seconds <= 60 * 60 * 24 * 365:
			# 	month = seconds / (60 * 60 * 24 * 30)
			# 	return u'%s月前' % int(month)
			else:
				#year = seconds / (60 * 60 * 24 * 365)
				#return u'%s年前' % int(year)
				# str_time =time.strptime(create_time, "%Y-%m-%d %H:%M:%S")
				# 转换为其他字符串格式:
				return create_time.strftime("%Y-%m-%d")
		else:
			return json_params_error(message=u'时间格式错误!')
	else:
		return json_params_error(message=u'时间格式错误!')

#问答问题详情
def question_detail(request,question_id=0,answer_id=0,parent_page=1,child_page=1):
	try:
		questionId = int(question_id)
		answerId = int(answer_id) #当前问题下的那个回答，用来实现评论翻页
		currentParentPage = int(parent_page) #1级评论当前页
		currentChildPage = int(child_page) #2级评论当前页
	except:pass

	logger.info({'question_id':question_id,'answer_id':answerId,'parent_page':currentParentPage,'child_page':currentChildPage})

	if questionId:
		questionModel = QuestionsModel.objects.filter(is_removed=0,pk=questionId).first()
		if questionModel:
			#统计阅读数
			questionModel.read_count()

			#20171212 进入问题详情时,若当前用户在登录状态下,则需要查看当前问题在消息列表中是否存在,如果存在需要将此问题置为已读状态
			if hasattr(request,'front_user'):
				if questionModel.author == request.front_user:
					myMessagesModel = MyMessagesModel.objects.filter(question=questionModel).all()
					if myMessagesModel:
						myMessagesModel.update(is_read=1)

			#如果问题存在,则查询问题是否存在分类
			if questionModel.category:
				question_category = questionModel.category.category
				question_category_id = questionModel.category.id
			else:
				question_category = None
				question_category_id =None

			#返回当前问题的关注数量
			attentionCount = AttentionQuestionModel.objects.filter(attention_question=questionModel).count()

			#如果当前用户已关注此问题，需要显示已关注
			if hasattr(request,'front_user'):
				isAttentionModel = AttentionQuestionModel.objects.filter(username=request.front_user,attention_question=questionModel).first()
				if isAttentionModel:
					is_attention = 1
				else:
					is_attention = 0
			else:
				is_attention = 0

			#返回问题的必备属性
			article = questionModel.relevance_method_article
			context = {
				'article': article,
				'article_url': article.url if article else '',
				'question_id':questionModel.id,
				'content':questionModel.content,
				'question_author':questionModel.author.username,
				'question_author_avatar':questionModel.author.avatar,
				'question_create_time':comment_time_period(questionModel.create_time),
				'question_category':question_category,
				'question_category_id':question_category_id,
				'current_parent_page': currentParentPage,
				'attention_count':attentionCount,
				'is_attention':is_attention,
			}

			#找出该问题的所有1级回答
			answersModel = AnswersModel.objects.filter(is_removed=0,questions=questionModel,relevance_answer=None).all()

			if answersModel:

				#给1级评论增加翻页
				#每页显示条数
				parentNumPage = int(configs.PC_FRONT_COMMENT_NUM_PAGE)
				parentStart = (currentParentPage-1)* parentNumPage
				parentEnd = parentStart + parentNumPage


				#计算评论总数
				answersCount = answersModel.count()

				#计算总页数
				parentPageCount = answersCount / parentNumPage
				if answersCount % parentNumPage > 0:
					parentPageCount +=1

				parentPages = []

				# 如果当前页码小于5,那么 pages将[1,2,3,4]填充进去
				# 如果当前页码大于5,那么 需要显示当前页码的左边2个，右边2个页码
				# 当页码为倒数第2页的时候,需要往前查找3页，往后查找1页
				# 如果当前页码是尾页，那么需要往前显示4个页码

				if currentParentPage < 5:
					tmpParentPage = currentParentPage - 1
					while tmpParentPage >= 1:
						if tmpParentPage % 5 == 0:
							break
						else:
							parentPages.append(tmpParentPage)
							tmpParentPage -= 1

					tmpParentPage = currentParentPage
					while tmpParentPage <= parentPageCount:
						if tmpParentPage % 5 == 0:
							parentPages.append(tmpParentPage)
							break
						else:
							parentPages.append(tmpParentPage)
							tmpParentPage += 1

				elif currentParentPage + 1 < parentPageCount:
					# 往前查找2次
					tmpParentPage = currentParentPage - 1
					t = 1
					while t < 3:
						if tmpParentPage > 1:
							parentPages.append(tmpParentPage)
							tmpParentPage -= 1
							t += 1
						else:
							break

					# 往后查找3次
					tmpParentPage = currentParentPage
					t = 1
					while t < 4:
						if tmpParentPage < parentPageCount:
							parentPages.append(tmpParentPage)
							tmpParentPage += 1
							t += 1
						else:
							parentPages.append(tmpParentPage)
							break

				elif currentParentPage + 1 == parentPageCount:
					# 这个判断用来解决当前页码为倒数第2页的时候,只显示4页的bug
					# 往前查找3次
					tmpParentPage = currentParentPage - 1
					t = 1
					while t < 4:
						if tmpParentPage > 1:
							parentPages.append(tmpParentPage)
							tmpParentPage -= 1
							t += 1
						else:
							break

					# 往后查找2次
					tmpParentPage = currentParentPage
					t = 1
					while t < 3:
						if tmpParentPage < parentPageCount:
							parentPages.append(tmpParentPage)
							tmpParentPage += 1
							t += 1
						else:
							parentPages.append(tmpParentPage)
							break
				else:
					tmpParentPage = currentParentPage
					t = 1
					# 往前查找5次
					while t < 6:
						parentPages.append(tmpParentPage)
						tmpParentPage -= 1
						t += 1

				parentPages.sort()

				answersModel = answersModel[parentStart:parentEnd]

				#如果评论存在,则继续查找每个1级评论是否有关联的2级评论
				tmpAnswers = []
				for a in answersModel:

					#获取当前1级回答的点赞数
					praiseAnswerCount = PraiseAnswerModel.objects.filter(praise_answer=a).count()

					#如果当前用户已点赞，需要显示黄色小手
					if hasattr(request,'front_user'):
						isPraiseModel = PraiseAnswerModel.objects.filter(username=request.front_user,praise_answer=a).first()
						if isPraiseModel:
							is_praise = 1
						else:
							is_praise = 0
					else:
						is_praise = 0

					#获取当前1级回答的收藏数
					collectAnswerCount = CollectAnswerModel.objects.filter(collect_answer=a).count()
					#如果当前用户收藏此回答,需要显示已收藏
					if hasattr(request,'front_user'):
						isCollectModel = CollectAnswerModel.objects.filter(username=request.front_user,collect_answer=a).first()
						if isCollectModel:
							is_collect = 1
						else:
							is_collect = 0
					else:
						is_collect = 0

					# 如果当前1级评论下有关联的2级评论，则把关联的2级评论全部取出来
					childAnswersModel = AnswersModel.objects.filter(is_removed=0, questions=questionModel,relevance_answer=a).all()

					if childAnswersModel:
						# 计算当前评论下2级评论的数量，超过3条则需要增加翻页按钮
						childNumPage = int(configs.ANSWER_NUM_PAGE)
						childStart = (currentChildPage - 1) * childNumPage
						childEnd = childStart + childNumPage
						# 计算2级评论总数
						childAnswersCount = childAnswersModel.count()

						# 计算总页数
						childPageCount = childAnswersCount / childNumPage
						if childAnswersCount % childNumPage > 0:
							childPageCount += 1

						pages = []

						# 先往前面找
						tmpPage = currentChildPage - 1
						while tmpPage >= 1:
							if tmpPage % 5 == 0:
								break
							else:
								pages.append(tmpPage)
								tmpPage -=1
						# 再往后面找
						tmpPage = currentChildPage
						while tmpPage <= childPageCount:
							if tmpPage % 5 == 0:
								pages.append(tmpPage)
								break
							else:
								pages.append(tmpPage)
								tmpPage += 1

						pages.sort()

						#如果当前传入的answerId为真，那么表示当前这个回答的2级评论有翻页操作，那么这个回答的2级评论需要展示currentChildPage页的数据。即:替换answerId回答的2级评论数据
						if answerId:
							answerIdModel = AnswersModel.objects.filter(pk=answerId,is_removed=0,questions=questionModel).first()
							if answerIdModel:
								if a == answerIdModel:
									childAnswersModel = childAnswersModel[childStart:childEnd] #如果遇到1级评论等于传入的answerId,那么这个1级评论下的2级评论才用切片展示currentChildPage页的数据
								else:
									childAnswersModel = childAnswersModel[:childNumPage]  #没有翻页的2级评论，默认展示配置的3条数据
						else:
							childAnswersModel = childAnswersModel[:childNumPage]  # 没有翻页的2级评论，默认展示配置的3条数据

						tmpChildAnswers = []
						for c in childAnswersModel:

							#如果当前2级评论有回复属性,则展示被回复者的姓名和id
							if c.relay_to:
								relay_to = c.relay_to.username
								relay_to_user_id = c.relay_to.id
							else:
								relay_to = None
								relay_to_user_id = None

							tmpChildAnswers.append({
								'answer_id':c.id,
								'current_answer_id':answerId,
								'user_id':c.author.id,
								'answer_username':c.author.username,
								'answer_user_avatar': c.author.avatar,
								'comment':c.comment,
								'relay_to':relay_to,
								'relay_to_user_id':relay_to_user_id,
								'create_time':comment_time_period(c.create_time),
							})

						#将2级评论合并到当前1级评论上
						tmpAnswers.append({
							'answer_id': a.id,
							'current_answer_id': answerId,
							'user_id': a.author.id,
							'answer_username': a.author.username,
							'answer_user_avatar':a.author.avatar,
							'comment': a.comment,
							'create_time': comment_time_period(a.create_time),
							'child_answers': tmpChildAnswers,
							'child_answers_count': childAnswersCount,
							'child_page_count': childPageCount,
							'current_child_page': currentChildPage,
							'pages': pages,
							'praise_answer_count':praiseAnswerCount,
							'collect_answer_count':collectAnswerCount,
							'is_praise':is_praise,
							'is_collect':is_collect,
						})

					else:
						#如果当前评论没有关联的2级评论,则直接返回1级评论信息
						# 将所有1级评论汇总
						tmpAnswers.append({
							'answer_id': a.id,
							'current_answer_id': answerId,
							'user_id': a.author.id,
							'answer_username': a.author.username,
							'answer_user_avatar':a.author.avatar,
							'comment': a.comment,
							'create_time': comment_time_period(a.create_time),
							'child_answers': None,
							'praise_answer_count': praiseAnswerCount,
							'collect_answer_count': collectAnswerCount,
							'is_praise': is_praise,
							'is_collect': is_collect,
						})

				context['answers'] = tmpAnswers
				context['parent_page_count'] = parentPageCount
				context['parent_pages'] = parentPages

				return context
			else:
				#没有评论 则返回None
				context['answers'] = None
				return context
		else:
			return {'message': u'你尝试查看一个不存在的问题!'}
	else:
		return {'message': u'你尝试访问一个不存在的问题!'}

#问答发表评论
def add_answer(request):
	if request.method == 'GET':
		return json_result(message=u'这是问答发表评论页面!')
	else:
		questionId = request.POST.get('question_id',0)
		relevanceAnswer = request.POST.get('relevance_answer',0)
		relayTo = request.POST.get('relay_to',0)
		comment = request.POST.get('comment',None)


		try:

			comment = str(comment).strip()
			relevanceAnswer = int(relevanceAnswer)
			relayTo =int(relayTo)
		except:pass

		logger.info({'question_id': questionId, 'relevance_answer': relevanceAnswer, 'relay_to': relayTo, 'comment': comment})

		if questionId:
			questionModel = QuestionsModel.objects.filter(pk = questionId,is_removed=0).first()

			if questionModel:
				if comment:
					if relevanceAnswer:
						#如果关联的回答id为真，则为2级评论
						answerModel = AnswersModel.objects.filter(pk = relevanceAnswer,questions=questionModel,is_removed=0).first()
						if answerModel:
							#2级评论还需要区分:对父评论回复时，不需要显示 回复者
							if relayTo:
								frontUserModel = FrontUserModel.objects.filter(pk=relayTo,is_active=1).first()

								if frontUserModel:
									# 若修改userid，导致不是当前问题下的用户，需要特殊处理
									tmpAnswerUserModel = AnswersModel.objects.filter(author=frontUserModel, questions=questionModel, is_removed=0).first()

									if tmpAnswerUserModel:
										relevanceAnswerModel = AnswersModel(author=request.front_user, questions=questionModel, comment=comment, relevance_answer=answerModel, relay_to=frontUserModel)
										relevanceAnswerModel.save()

										# 更新问题模型中的最后评论时间
										questionModel.last_answer_time = datetime.datetime.now()
										questionModel.save(update_fields=['last_answer_time'])

										#给回复者发通知


										return json_result(message=u'回复评论成功!')
									else:
										return json_params_error(message=u'你回复的回答不存在或已删除!')
								else:
									return json_params_error(message=u'不能回复给不存在的人!')
							else:
								tmpChildAnswerModel = AnswersModel(author=request.front_user, questions=questionModel, comment=comment, relevance_answer=answerModel)
								tmpChildAnswerModel.save()

								questionModel.last_answer_time = datetime.datetime.now()
								questionModel.save(update_fields=['last_answer_time'])
								return json_result(message=u'回复评论成功!')
						else:
							return json_params_error(message=u'你尝试回复一个不存在的评论!')
					else:
						parentAnswerModel = AnswersModel(author=request.front_user, questions=questionModel, comment=comment)
						parentAnswerModel.save()
						questionModel.last_answer_time = datetime.datetime.now()
						questionModel.save(update_fields=['last_answer_time'])

						#20171212 当问题有1级回复时,给发表问题者发送通知
						myMessagesModel = MyMessagesModel(replay_name=request.front_user,replay_answer=parentAnswerModel,question=questionModel)
						myMessagesModel.save()

						return json_result(message=u'回复评论成功!')
				else:
					return json_params_error(message=u'评论内容不能为空!')
			else:
				return json_params_error(message=u'你尝试回答一个不存在的问题!')
		else:
			return json_params_error(message=u'你尝试访问一个不存在的问题!')


# 收藏方法/取消收藏(可收藏视频、研究方法，研究进展等一切)
def favorites(request, id=0, collect_category_id=0, type_id=0):
	try:
		Id = int(id)
		collectCategoryId = int(collect_category_id)
	except:
		pass

	typeId =type_id
	model_type = configs.model_type

	if not Id:
		return json_params_error(message=u'这是一片未知的荒原!')

	if not typeId:
		return json_params_error(message=u'请选择收藏类型!')

	collectCategoryModel = None
	# 判断收藏分类是否存在
	if collectCategoryId:
		userCollectCategoryModel = UserCollectCategoryModel.objects.filter(author=request.front_user, pk=collectCategoryId).first()
		if userCollectCategoryModel:
			collectCategoryModel = userCollectCategoryModel

	# 判断此类型是否存在

	if model_type[typeId]:
		typeId = int(typeId)
		if typeId == 1:
			favoritesModel = MethodArticleInfoModel.objects.filter(status__in=[1, 2], pk=Id).first()
			if not favoritesModel:
				return json_params_error(message=u'你尝试查看一篇不存在的文章!')
		elif typeId == 2:
			favoritesModel = NewsModel.objects.filter(status__in=[1, 2], pk=Id).first()
			if not favoritesModel:
				return json_params_error(message=u'你尝试查看一篇不存在的新闻!')
		elif typeId == 3:
			favoritesModel = VideoModel.objects.filter(status=1, pk=Id).first()
			if not favoritesModel:
				return json_params_error(message=u'你尝试查看一节不存在的课程!')
		else:
			return json_params_error(message=u'请更新模型!')

		# 判断用户收藏列表中是否存在此收藏
		userFavoritesModel = UserFavoritesModel.objects.filter(username=request.front_user, favorite_category=collectCategoryModel).all()

		if userFavoritesModel:
			for u in userFavoritesModel:
				if u.content_object == favoritesModel:
					u.delete()
					context = {
						'is_collect': 0,
					}
					return json_result(message=u'已取消收藏!', data=context)

		userFavoritesModel = UserFavoritesModel(username=request.front_user, favorite_category=collectCategoryModel, content_object=favoritesModel)
		userFavoritesModel.save()
		context = {
			'is_collect': 1,
		}
		return json_result(message=u'收藏成功!', data=context)
	else:
		return json_params_error(message=u'你尝试收藏一个不存在的类型!')


#点赞方法
def user_praise(request,id=0,type_id=0):
	try:
		Id = int(id)
	except:pass

	model_type = configs.model_type

	if not Id:
		return json_params_error(message=u'这是一片未知的荒原!')

	if not type_id:
		return json_params_error(message=u'请选择点赞类型!')

	if model_type[type_id]:
		typeId = int(type_id)
		if typeId == 1:
			praiseModel = MethodArticleInfoModel.objects.filter(status__in=[1, 2], pk=Id).first()
			if not praiseModel:
				return json_params_error(message=u'你尝试查看一篇不存在的文章!')
		elif typeId == 2:
			praiseModel = NewsModel.objects.filter(status__in=[1, 2], pk=Id).first()
			if not praiseModel:
				return json_params_error(message=u'你尝试查看一篇不存在的新闻!')
		elif typeId == 3 :
			praiseModel = VideoModel.objects.filter(status=1, pk=Id).first()
			if not praiseModel:
				return json_params_error(message=u'你尝试查看一节不存在的课程!')
		elif typeId == 6:
			praiseModel = VideoCommentModel.objects.filter(pk=Id).first()
			if not praiseModel:
				return json_params_error(message=u'你尝试查看一条不存在的评论!')
		else:
			return json_params_error(message=u'请更新模型!')
		#判断用户是否已点赞
		userPraiseModel = UserPraiseModel.objects.filter(username=request.front_user)

		if userPraiseModel:
			for u in userPraiseModel:
				if praiseModel == u.content_object:
					u.delete()
					context = {
						'is_praise':0,
					}
					return json_result(message=u'已取消赞点!',data=context)

		addPraiseModel = UserPraiseModel(username=request.front_user,content_object= praiseModel)
		addPraiseModel.save()
		context = {
			'is_praise':1,
		}
		return json_result(message=u'已点赞!', data=context)
	else:
		return json_params_error(message=u'你尝试点赞一个不存在的类型!')




