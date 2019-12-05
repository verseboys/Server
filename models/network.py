# coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# 文档：https://confluence.natureself.site/pages/viewpage.action?pageId=25624953
# notice文档：https://confluence.natureself.site/pages/viewpage.action?pageId=26775262

# 医咖会科研网络
class Network(models.Model):
    class Meta:
        db_table = 'y_network'

    name = models.CharField(max_length=191, unique=True)
    description = models.TextField(blank=True)
    studies = models.ManyToManyField('EdcStudy', related_name='networks')
    train_description = models.TextField(blank=True)


class NetworkApplication(models.Model):
    class Meta:
        db_table = 'y_network_application'
        unique_together = (
            ('network', 'user'),
        )

    network = models.ForeignKey('Network')
    studies = models.ManyToManyField('EdcStudy', related_name='network_applications')
    user = models.ForeignKey('frontmodel.FrontUserModel', related_name='network_applications')
    address = models.CharField(max_length=191)
    site = models.CharField(max_length=191)
    status = models.IntegerField(choices={
        (0, '未审核'),
        (1, '已审核'),
    }, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def has_has_applied_and_member(request):
        # 判断当前登录用户是否提交过申请，根据情况决定如何渲染“申请加入”的按钮
        if not hasattr(request, 'front_user'):
            application = None
            member = None
        else:
            try:
                application = NetworkApplication.objects.get(user=request.front_user)
            except NetworkApplication.DoesNotExist:
                application = None
            # 查看用户是否已加入该网络，在 NetworkMember 中查找邮箱与当前登录用户相同、并且状态为已激活的，
            # 如果 member 为空，表示用户未加入该网络。
            # 注意：根据之前实现的业务逻辑，可能存在多个 member 的邮箱相同，因此这里不能用 get()，可能会抛出 MultipleObjectsReturned 异常
            member = NetworkMember.objects.filter(email=request.front_user.email, status=2).first()

        has_applied = bool(application)
        return has_applied, member

    @property
    def leader(self):
        try:
            return self.members.get(duty='项目负责人')
        except:
            return None

    @property
    def researchers(self):
        # NOTE, filter() returns a queryset, we should return a list of object here
        return self.members.filter(duty='研究者')

    @property
    def datamanager(self):
        try:
            return self.members.get(duty='数据管理员')
        except:
            return None

    # 用于在渲染申请表单的数据，这里返回一个字典，在 template 的 context 中可以序列化为 json
    def to_form_dict(self):
        form = {}
        form['edc_study_ids'] = [study.study_id for study in self.studies.all()]
        form['site'] = self.site
        form['status'] = self.status
        form['address'] = self.address
        form['leader'] = self.leader.to_dict() if self.leader else None
        form['researchers'] = [r.to_dict() for r in self.researchers]
        form['datamanager'] = self.datamanager.to_dict() if self.datamanager else None
        return form


# 研究人员
class NetworkMember(models.Model):
    class Meta:
        db_table = 'y_network_member'

    network = models.ForeignKey('Network')
    application = models.ForeignKey('NetworkApplication', related_name='members')
    name = models.CharField(max_length=191)
    phone = models.CharField(max_length=32)
    email = models.EmailField()
    # 职称
    title = models.CharField(max_length=191)
    # 科室
    department = models.CharField(max_length=191)
    # 研究职责，取值：项目负责人、研究者、数据管理员、other（自定义）
    duty = models.CharField(max_length=191)
    # EDC 用户ID，如果为0，表示未在 EDC 中注册
    edc_user_id = models.IntegerField(default=0)
    # 医咖会用户id，如果为0，表示未创建
    medieco_user_id = models.IntegerField(default=0)
    # 研究人员验证进度  0未处理 1：未邮箱验证  2：邮箱已激活
    status = models.IntegerField(default=0)

    @property
    def registered_in_edc(self):
        return self.edc_user_id != 0

    def to_dict(self):
        return dict(
            name=self.name,
            phone=self.phone,
            email=self.email,
            title=self.title,
            department=self.department,
            duty=self.duty,
            status=self.status,
        )


class NetworkMemberB4Account(models.Model):
    class Meta:
        db_table = 'y_network_member_before_account'

    member = models.ForeignKey('NetworkMember')
    # 生成初始密码，这里保存初始密码的明文
    password_raw = models.CharField(max_length=191)

    # 用户激活用的 code，32字节字符串，建议用 uuid4 直接生成，例如 uuid.uuid4().get_hex()
    code = models.CharField(max_length=32, unique=True)
    # 用户没有访问过时，used_at 是 null
    used_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def used(self):
        return self.used_at != None


class NetworkCourse(models.Model):
    class Meta:
        db_table = 'y_network_course'

    network = models.ForeignKey('Network', related_name='courses')
    name = models.CharField(max_length=191)
    type = models.IntegerField(choices={
        (0, '基本课程'),
        (1, '补充课程'),
    }, default=0)
    icon_ss_key = models.CharField(max_length=191, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices={
        ('draft', '草稿'),
        ('plan', '待发布'),
        ('publish', '已发布'),
    }, default='draft', max_length=10)
    published_at = models.DateTimeField(null=True)
    videos = models.ManyToManyField('videomodel.VideoModel', through='NetworkCourseVideo')
    participants = models.ManyToManyField('frontmodel.FrontUserModel', through='NetworkCourseTrainProgress')
    medal = models.ForeignKey('anniversary.medalModel', null=True)
    data_collection = models.BooleanField(default=False)
    serial_state = models.CharField(choices=(('loading','连载中'),('finished','已完结')),max_length=10,default='loading')
    public_scope = models.IntegerField(default=0)
    order = models.IntegerField(default=1)


    @property
    def published(self):
        return self.status == 'publish'

    @property
    def pic_url(self):
        return settings.STORAGE_SERVICE_FILE_URL.format(self.icon_ss_key)


class NetworkCourseVideo(models.Model):
    class Meta:
        db_table = 'y_network_course_videos'

    course = models.ForeignKey('NetworkCourse')
    video = models.ForeignKey('videomodel.VideoModel')
    order = models.IntegerField()


class NetworkCourseTrainProgress(models.Model):
    class Meta:
        db_table = 'y_network_course_train_progress'
        unique_together = (
            ('participant', 'course'),
        )

    participant = models.ForeignKey('frontmodel.FrontUserModel')
    course = models.ForeignKey(NetworkCourse)
    begin_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField(null=True)


class NetworkCourseTrainLog(models.Model):
    class Meta:
        db_table = 'y_network_course_train_logs'
        unique_together = (
            ('participant', 'video'),
        )

    participant = models.ForeignKey('frontmodel.FrontUserModel')
    video = models.ForeignKey('NetworkCourseVideo')


# 下方两个model基于member的科室和职称无法映射而设，悲催
class NetworkMemberDepartmentProfession(models.Model):
    class Meta:
        db_table = 'y_network_memeber_department_profession'
        unique_together = (
            ('department', 'profession')
        )

    department = models.CharField(max_length=191, unique=True)
    profession = models.ForeignKey('frontmodel.ProfessionalSectionsModel')


class NetworkMemberTitleJobTitle(models.Model):
    class Meta:
        db_table = 'y_network_member_title_jobtitle'
        unique_together = (
            ('title', 'job_title')
        )

    title = models.CharField(max_length=191, unique=True)
    job_title = models.ForeignKey('frontmodel.JobTitleModel')


# 医咖会-通知公告文章
class NetworkNotice(models.Model):
    class Meta:
        db_table = 'y_network_notices'

    title = models.CharField(max_length=191)
    content = models.TextField()
    # 手写的时间，所以定义为字符
    published_at = models.DateTimeField()
    publish_user = models.ForeignKey(User, related_name='network_notices')
    status = models.IntegerField(choices={
        (0, '草稿'),
        (1, '已发布'),
    }, default=0)
    scope = models.IntegerField(choices={
        (0, '公开'),
        (1, '科研网络'),
    }, default=0)
    top = models.BooleanField(default=False)
    network = models.ForeignKey('Network', related_name='network_notices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_count = models.IntegerField(default=0)
    tags = models.ManyToManyField('NetworkTag', db_table='y_network_notice_tag', related_name='notices')


# # 医咖会-通知公告文章统计
class NetworkNoticeStat(models.Model):
    class Meta:
        db_table = 'y_network_notice_stat'

    user = models.ForeignKey('frontmodel.FrontUserModel', null=True)
    action = models.CharField(choices={
        ('read', '阅读'),
        ('share', '分享'),
    }, max_length=20, default='read')
    notice = models.ForeignKey('NetworkNotice')
    created_at = models.DateTimeField(auto_now_add=True)


class NetworkNoticeAttachment(models.Model):
    class Meta:
        db_table = 'y_network_notice_attachment'
        unique_together = (
            ('notice', 'file_key'),
        )

    notice = models.ForeignKey('NetworkNotice')
    # ss 文件服务返回的 key
    file_key = models.CharField(max_length=50)
    # 虽然 ss 服务会存储file_name 这里做个冗余，方便前端使用
    file_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def file_url(self):
        return settings.STORAGE_SERVICE_FILE_URL.format(self.file_key)


class NetworkTag(models.Model):
    class Meta:
        db_table = 'y_network_tags'

    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
