# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0008_contentrecommend'),
    ]

    operations = [
        migrations.RunSQL(["ALTER TABLE y_content_recommend MODIFY COLUMN create_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"]),
        migrations.RunSQL(["ALTER TABLE y_content_recommend MODIFY COLUMN content_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"]),
        migrations.RunSQL(["ALTER TABLE y_content_recommend MODIFY COLUMN update_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);"]),
    ]
