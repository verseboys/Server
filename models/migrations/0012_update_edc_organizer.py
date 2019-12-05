# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0011_import_initial_network_data')
    ]

    operations = [
            migrations.RunSQL(["update y_edc_organizers set organizer_name='中国宋庆龄基金会 · 呼吸疾病临床研究公益基金' where id=2;"]),
        ]
