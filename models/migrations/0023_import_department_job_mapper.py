# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0022_auto_20181208_2029'),
    ]

    operations = [
        #29-中医内科
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('中医康复科','29');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('中医科','29');"),

        #临床医学-全科
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('全科','27');"),

        #临床医学-内科-呼吸科
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸一科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('老年呼吸科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸与危重症','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('肺功能室','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸二科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸1科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('中医肺病科一部','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('肺病科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸与危重症医学科四部','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('干部呼吸科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('附属医院呼吸内科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸与危重症中心二病区','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('肺科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('蒙医呼吸内科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('放射科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('蒙医呼吸科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸内科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸与危重症医学科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('肺病科（呼吸科）','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('RICU','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('dsdds','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸与危重症学科','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸病学研究室','80');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('呼吸内科一区','80');"),
        
        #临床医学-内科-普通内科
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('内五科','87');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('内三科','87');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('内二科2组','87');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('内科','87');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('内二科','87');"),

        #临床医学 - 内科 - 消化科
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('脾胃科','79');"),

        #临床医学-内科-老年病科
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('老年病科','86');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('老年医学科','86');"),

        #临床医学-外科-泌尿外科
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('泌尿科','97');"),

        #临床医学-急诊科
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('急诊科','20');"),

        #临床医学-检验科
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('特检科','24');"),

        #临床医学-重症医学科
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('重症医学科','21');"),

        #基础医学-解剖学与组织胚胎学
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('解剖学教研室','58');"),

        #药学 - 中药学
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('药理系中药药理实验室','52');"),

        #药学 - 临床药学
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('附属医院药剂科','53');"),
        migrations.RunSQL("INSERT INTO y_network_memeber_department_profession (department, profession_id) VALUES ('药学部','53');"),
        #other 75 医学相关-其他

        #中级职称-主治医师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('中级','14');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('主治中医师','14');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('住院中医师','14');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('主治医师','14');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('主治医生','14');"),

        #中级职称-主管护师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('主管护师','17');"),

        #中级职称 - 主管药师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('主管药师','16');"),

        #中级职称-讲师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('讲师','19');"),

        #初级职称以下-医学生
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('硕士生','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('在读硕士研究生','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('博士生','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('硕士研究生在读','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('硕士研究生','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('全科研究生在读','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('在读研究生','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('呼吸内科专业研究生','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('学生','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('研究生在读','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('研究生','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('博士研究生','6');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('医学生','6');"),

        #初级职称-住院医师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('规培医师','8');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('住院医师','8');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('住院医','8');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('初级医师','8');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('住院医生','8');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('医师','8');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('初级','8');"),

        #初级职称-助教
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('助教','12');"),

        #初级职称-技师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('技师','11');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('工程师','11');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('初级技师','11');"),

        #初级职称-护师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('护师','10');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('护士','10');"),

        #初级职称-药师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('药师','9');"),

        #副高级职称-副主任医师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('副高级','21');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('副主任医师/副教授','21');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('副主任中医师','21');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('副主任医师','21');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('副主任','21');"),

        #副高级职称-副主任技师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('副主任技师','24');"),

        #副高级职称-副主任护师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('副主任护师','23');"),

        #副高级职称-副主任药师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('副主任药师','22');"),

        #副高级职称-副教授
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('副教授','25');"),

        #副高级职称-副研究员
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('副研究员','26');"),

        #高级职称-主任医师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('教授/主任医师','27');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('主任中医师','27');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('主任医师','27');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('主任医师、教授','27');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('科主任','27');"),

        #高级职称-主任护师
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('主任护师','29');"),

        #高级职称-教授
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('教授','31');"),
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('高级','31');"),

        #高级职称-研究员
        migrations.RunSQL("INSERT INTO y_network_member_title_jobtitle (title, job_title_id) VALUES ('高级实验师','32');"),
        #DEFAULT 7 初级职称以下-未晋升初级职称
    ]