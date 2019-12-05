# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0018_auto_20181201_1425'),
    ]

    operations = [
        migrations.RunSQL(["ALTER TABLE y_network_course MODIFY COLUMN created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"]),

        migrations.RunSQL(["ALTER TABLE y_network_course MODIFY COLUMN updated_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);"]),
    ]
