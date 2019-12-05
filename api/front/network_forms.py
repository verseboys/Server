#coding:utf-8

from __future__ import unicode_literals

from django import forms

from models.edc import EdcStudy

class ApplicationForm(forms.Form):
    # NOTE see django doc: https://docs.djangoproject.com/en/1.10/ref/forms/fields/#modelchoicefield
    # Django will load all projects from db, and check choices in memory.
    # If EdcStudy has more than 100 items, this should be impractical.
    edc_study_ids = forms.ModelMultipleChoiceField(
            queryset=EdcStudy.objects.all(),
            to_field_name='study_id',
            error_messages={
                'required': '请至少选择一个项目',
                'list': 'edc_study_ids 字段不是合法的数组',
                'invalid_choice': '项目 %(value)s 不存在',
                'invalid_pk_value': '%(pk)s 不是合法的项目 id，请提供项目 id',
            })
    site = forms.CharField(required=True, error_messages={'required': '工作单位不能为空'})
    address = forms.CharField(required=True, error_messages={'required': '工作地址不能为空'})

    # NOTE leader、researchers、datamanager 我们单独处理，不在这个 form 中处理
    def clean_edc_study_ids(self):
        edc_study_ids = self.cleaned_data['edc_study_ids']
        if len(edc_study_ids) == 0:
            raise form.ValidationError('请选择至少一个项目')

        return edc_study_ids

class ApplicationMemberForm(forms.Form):
    name = forms.CharField(required=True, error_messages={'required': '姓名不能为空'})
    email = forms.EmailField(required=True, error_messages={
        'required': '邮箱不能为空',
        'invalid': '请输入正确的邮箱',
        })
    # TODO 这里并没有严格的校验手机号
    phone = forms.RegexField(required=True, regex=r'1\d{8}', error_messages={
        'required': '手机号不能为空',
        'invalid': '请输入正确的手机号',
        })
    department = forms.CharField(required=True, error_messages={'required': '科室不能为空'})
    title = forms.CharField(required=True, error_messages={'required': '职称不能为空'})
