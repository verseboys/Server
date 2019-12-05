# coding:utf-8

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

import hashers
import random
import uuid

import configs


# 前台用户模型
class FrontUserModel(AbstractBaseUser):
    """
    更新说明(2019.06.10)：
    将用户 Model 改为继承 AbstractBaseUser，该父 Model 提供了两个字段，
    * password（max_length 为 128）
    * last_login
    这个更新将导致该 Model 的两个变动：
    * password 的 max_length 由原来的 200 变为 128
    * 新增 last_login
    此外，我们还需要增加 USERNAME_FIELD 属性或实现 get_username() 方法，
    这里我们选择增加 USERNAME_FIELD 属性（有更好的工具兼容性）。
    更新说明（2019.06.17）
    增加email_need_validate，新注册用户标示为True，验证邮箱后标识为False，
    已注册的邮箱可以手工标识为True，登录时需要跳转到邮箱验证页面。
    """
    USERNAME_FIELD = 'username'

    gender_type = (
        (0, u'男'), (1, u'女'), (2, u'保密')
    )
    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(unique=True, null=True)
    #联系邮箱
    contact_email = models.EmailField(max_length=200, null=True)
    # phone 为用于登录的手机号，允许为空
    phone = models.CharField(unique=True, max_length=11, null=True)
    # mobile 为联系电话，用于发送通知信息
    mobile = models.CharField(null=True, max_length=50)
    gender = models.IntegerField(choices=gender_type, default=2)
    avatar = models.URLField(null=True)
    corporation = models.CharField(u'所在公司', null=True, max_length=200)  # 所在公司
    profession = models.ForeignKey('ProfessionalSectionsModel', null=True)  # 专业科室
    jobtitle = models.ForeignKey('JobTitleModel', null=True)  # 职称
    create_time = models.DateTimeField(auto_now_add=True)
    signature = models.TextField(null=True)  # 签名
    last_logout_date = models.DateTimeField(auto_now=True, null=True)
    is_active = models.IntegerField(u'是否锁定', default=1)
    uuid = models.UUIDField(default=uuid.uuid4)
    email_validated = models.BooleanField(default=False)
    # 邮箱是否需要验证，默认无需，可手动修改为需要验证。
    email_need_validate = models.BooleanField(default=False)
    phone_validated = models.BooleanField(default=False)
    full_name = models.CharField(max_length=191, default='')

    class Meta:
        db_table = 'y_users'

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            hash_password = hashers.make_password(kwargs['password'])
            kwargs['password'] = hash_password
        super(FrontUserModel, self).__init__(*args, **kwargs)

    def check_password(self, raw_password):
        """
        2019.06.11 更新说明，将该函数改为调用 Django 自带的 check_password

        Django 的密码支持多种 hash 算法，具体实现在 contrib/auth/hashers.py 中，
        其中与 md5 相关的有两种方式：
        * unsalted_md5，即直接 md5(raw_password)
        * md5，md5(salt + raw_password)，salt 会保存在密码哈希中

        其中，unsalted_md5 的哈希内容为裸的 32 字符长度的字符串，md5 的格式为:
            md5$__salt__$__hash__

        例如，假设密码为 123456，salt 为 abcdef，则哈希为：
            md5$abcdef$3c655e2f47c23bbd565448c992529891

        医咖会中原来密码的hash方式实际上是（salted）md5，但是 salt 是写死的，
        因此安全性与 unsalted_md5 一样（不能对抗彩虹表）。因此我们需要升级
        数据库中的 hash，改为使用 pbkdf2_sha256 。当使用 Django 自带的 check_password
        时，如果校验成功，Django 会自动升级 hash。

        为了正常使用 Django 的 check_password，我们需要将 self.password
        改为 md5 的格式。注，实际上原来代码中使用的是 md5(raw + salt)，而非
        md5(salt + raw)，因此我们复制了 Django hashers 中的 MD5PasswordHasher，
        改成了 MediecoMD5PasswordHasher，所以我们实际修改后的格式是
            medieco_md5$__salt__$__hash__

        关于 Django 自动升级 hash 的逻辑补充说明：
        Django 的 check_password 中，会检查设置中默认的 hash 方法（在 settings.py
        中设置，默认为 pbkdf2_sha256），以及当前密码使用的 hash 方法，如果密码
        校验成功（意味着我们有用户密码原文）、且当前 hash 和应用设置的 hash 不同，
        Django 就会重新计算哈希并保存到数据库中。因此，任何用户只要登录之后，其密码
        哈希就会被自动升级。

        另一种升级的方式是，不依赖于用户的操作，我们可以直接用现在的哈希作为原文，
        使用更安全的 hash 算法计算，存入数据库，在 check_password 时，先用用户提供
        的原文进行校验，如果不成功，就再用 md5(salt+raw) 去校验，如果成功就放行。
        我们此次更新暂时不采用这个方法。
        """
        if len(self.password) == 32 and '$' not in self.password:
            self.password = 'medieco_md5$%s$%s' % (configs.PASSWORD_SALT, self.password)
        return super(FrontUserModel, self).check_password(raw_password)

    def set_password(self, raw_password):
        """
        2019.06.11 更新说明，将该函数改为 Django 自带的 set_password。

        没有直接删除该函数，而是通过 super 调用父类（AbstractBaseUser）的函数，
        主要是为了便于以后了解到这个修改。
        """
        super(FrontUserModel, self).set_password(raw_password)

    def update_password(self, raw_password):
        """
        set_password 是为了保证和django行为一致，那么单独定义本方法进行db的持久化save操作。
        """
        self.set_password(raw_password)
        self.save(update_fields=['password'])

    def create_user_by_email(self,email_need_validate=True):
        self.username = self._generate_random_username()
        self.email_validated = not email_need_validate
        self.email_need_validate = email_need_validate
        self.avatar = 'yika_admin.png'
        self.save()

    def update_phone(self,new_phone):
        self.phone=new_phone
        self.phone_validated = True
        self.save(update_fields=['phone','phone_validated'])

    def update_email(self, new_email):
        self.email = new_email
        self.email_need_validate = False
        self.email_validated = True
        self.save(update_fields=['email', 'email_need_validate', 'email_validated'])

    def create_user_by_phone(self):
        self.username = self._generate_random_username()
        self.phone_validated = True
        self.avatar = 'yika_admin.png'
        self.save()

    def _generate_random_username(self):
        seed = "1234567890abcdefghijklmnopqrstuvwxyz"
        sa = []
        for i in range(7):
            sa.append(random.choice(seed))
        salt = ''.join(sa)
        return 'medi_' + salt

    def set_email_validated(self):
        self.email_validated = True
        self.email_need_validate = False
        self.save(update_fields=['email_validated','email_need_validate'])

    def serialize(self, to_dict=True):
        # TODO implement it seriously
        return dict(
            username=self.username,
            email=self.email,
            mobile=self.mobile,
            gender=self.gender,
            is_active=self.is_active,
            uuid=self.uuid,
        )


# 专业科室模型
class ProfessionalSectionsModel(models.Model):
    department_name = models.CharField('科室名称', max_length=20)
    section_grade = models.IntegerField('科室等级', default=1)
    professional_section = models.ForeignKey('ProfessionalSectionsModel', max_length=50, default=1, null=True)

    class Meta:
        db_table = 'y_professional_sections'

    def serialize(self, to_dict=True):
        return dict(
            id=self.id,
            department_name=self.department_name,
            section_grade=self.section_grade,
        )

# 职称模型
class JobTitleModel(models.Model):
    job_name = models.CharField('职称名字', max_length=20, null=True)
    job_grade = models.IntegerField('职称等级')
    job_title = models.ForeignKey('JobTitleModel', max_length=50, null=True)

    class Meta:
        db_table = 'y_job_title'

    def serialize(self, to_dict=True):
        return dict(
            id=self.id,
            job_name=self.job_name,
            job_grade=self.job_grade,
        )

# 用户收藏记录模型
class UserFavoritesModel(models.Model):
    username = models.ForeignKey('FrontUserModel')
    favorite_category = models.ForeignKey('questionsandanswersmodel.UserCollectCategoryModel', null=True)  # 所属收藏夹的分类
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'y_user_favorites'


# 用户购买记录
class UserBuyOrderModel(models.Model):
    status = (
        (0, '已失效'),
        (1, '未支付'),
        (2, '已支付'),
    )
    type = (
        (1, '支付宝'),
        (2, '微信')
    )
    username = models.ForeignKey('FrontUserModel')
    order_id = models.CharField(max_length=200)  # 订单id
    relevance_order = models.CharField(max_length=200, null=True)  # 关联订单id
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True)  # 金额
    summary = models.TextField()  # 说明
    status = models.IntegerField(choices=status, default=1, null=True)  # 订单状态
    type = models.IntegerField(choices=type, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'y_user_buy_order'


# 用户点赞模型
class UserPraiseModel(models.Model):
    username = models.ForeignKey('FrontUserModel')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'y_user_praise'
