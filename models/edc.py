#coding:utf-8
from __future__ import unicode_literals

from django.db import models

class EdcIllness(models.Model):
    class Meta:
        db_table='y_edc_illnesses'

    illness_name = models.CharField(max_length=191, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class EdcOrganizer(models.Model):
    class Meta:
        db_table='y_edc_organizers'

    organizer_name = models.CharField(max_length=191, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class EdcPlatform(models.Model):
    class Meta:
        db_table='y_edc_platforms'

    platform_name = models.CharField(max_length=191, unique=True)
    url = models.TextField(blank=True)
    icon_url = models.CharField(max_length=191, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class EdcStudy(models.Model):
    class Meta:
        db_table='y_edc_studies'

    study_id = models.IntegerField(unique=True)
    name = models.TextField(blank=False)
    state = models.TextField(blank=False)
    type = models.TextField(blank=False)
    is_top = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    level_type = models.IntegerField(choices={
        (0, '院级'),
        (1, '市级'),
        (2, '省部级'),
        (3, '国家级'),
    }, default=0)
    declare_type = models.IntegerField(choices={
        (0, '自主申报'),
        (1, '定向委托'),
    }, default=0)
    is_data_share = models.BooleanField(default=False)
    bg_oss_key=models.TextField(blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True)
    finish_date = models.DateField(null=True)
    edc_platform = models.ForeignKey('EdcPlatform', null=True)
    study_website = models.CharField(max_length=191)
    apply_term = models.TextField(blank=True)
    apply_way = models.TextField(blank=True)
    apply_due_date = models.DateField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    illnesses = models.ManyToManyField('EdcIllness', through='EdcStudyIllness')
    organizers = models.ManyToManyField('EdcOrganizer', through='EdcStudyOrganizer')

    def role_count(self):
        return ','.join(i.id for i in self.edcstudyrole_set.all())

    def __unicode__(self):
        return self.name

    @property
    def state_display(self):
        states = {
            'INIT': '新建立',
            'ONGOING': '进行中',
            'LOCKED': '已锁定',
            'COMPLETE': '已完成',
            }
        return states[self.state]

    @property
    def level_type_display(self):
        level_types = {
            0: '',
            1: '院级',
            2: '市级',
            3: '省部级',
            4: '国家级',
            }
        return level_types[self.level_type]

    @property
    def declare_type_display(self):
        declare_types = {
            1: '',
            2: '自主申报',
            3: '定向委托',
            }
        return declare_types[self.declare_type]

    @property
    def is_data_share_display(self):
        data_share = {
            True: '是',
            False: '否',
            }
        return data_share[self.is_data_share]

    def to_dict(self):
        return dict(
                study_id = self.study_id,
                name = self.name,
                )

class EdcStudyIllness(models.Model):
    class Meta:
        db_table='y_edc_study_illness'

    edc_study = models.ForeignKey('EdcStudy')
    illness = models.ForeignKey('EdcIllness')

class EdcStudyOrganizer(models.Model):
    class Meta:
        db_table='y_edc_study_organizer'

    edc_study = models.ForeignKey('EdcStudy')
    organizer = models.ForeignKey('EdcOrganizer')

class EdcStudyRole(models.Model):
    class Meta:
        db_table='y_edc_study_roles'

    edc_study = models.ForeignKey('EdcStudy')
    user_id = models.IntegerField()
    name = models.TextField()
    department = models.TextField()
    site = models.TextField()
    title = models.TextField()

    type = models.TextField(choices={
        ('pi', 'PI'),
        ('researcher', '研究者'),
        ('expertComm', '专家委员会'),
    },default='researcher')
    display_order = models.IntegerField(default=0)
    email = models.TextField(blank=True)

class EdcStudySite(models.Model):
    class Meta:
        db_table='y_edc_study_sites'

    edc_study = models.ForeignKey('EdcStudy')
    site_id = models.IntegerField()
    org_id = models.IntegerField(default=0)
    org_name = models.CharField(max_length=191,blank=True)
    is_top = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    icon_url = models.CharField(max_length=191, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
