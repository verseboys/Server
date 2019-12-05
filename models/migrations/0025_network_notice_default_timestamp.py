# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('models', '0024_auto_20190119_1150'),
    ]

    operations = [
        migrations.RunSQL([
            "ALTER TABLE y_network_notices MODIFY COLUMN created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"
        ]),
        migrations.RunSQL([
            "ALTER TABLE y_network_notices MODIFY COLUMN updated_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);"
        ]),
        migrations.RunSQL([
            "ALTER TABLE y_network_notice_stat MODIFY COLUMN created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"
        ]),
        migrations.RunSQL([
            "ALTER TABLE y_network_notice_attachment MODIFY COLUMN created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"
        ]),
        migrations.RunSQL([
            "ALTER TABLE y_network_tags MODIFY COLUMN created_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"
        ]),
        migrations.RunSQL([
            "ALTER TABLE y_network_tags MODIFY COLUMN updated_at datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);"
        ]),
    ]
