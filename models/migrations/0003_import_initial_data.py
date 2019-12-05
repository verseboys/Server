# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_use_db_default_timestamp'),
    ]

    operations = [
        migrations.RunSQL(["INSERT INTO y_edc_illnesses(id, illness_name) VALUES (1, '慢阻肺');"]),
        migrations.RunSQL(["INSERT INTO y_edc_illnesses(id, illness_name) VALUES (2, '哮喘');"]),
        migrations.RunSQL(["INSERT INTO y_edc_illnesses(id, illness_name) VALUES (3, '肺炎');"]),

        migrations.RunSQL(["INSERT INTO y_edc_platforms(id, platform_name,url,icon_url) VALUES (1, '医维云科研大数据平台','www.einmatrix.com','https://www.einmatrix.com/app/static/assets/evalogos.png');"]),

        migrations.RunSQL(["INSERT INTO y_edc_organizers(id, organizer_name) VALUES (1, '中华医学会呼吸分会基层呼吸防治联盟');"]),
        migrations.RunSQL(["INSERT INTO y_edc_organizers(id, organizer_name) VALUES (2, '宋庆龄基金会呼吸疾病临床研究公益基金会');"]),
    ]
