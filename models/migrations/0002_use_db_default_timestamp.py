# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(["ALTER TABLE y_edc_illnesses MODIFY COLUMN create_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"]),
        migrations.RunSQL(["ALTER TABLE y_edc_organizers MODIFY COLUMN create_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"]),
        migrations.RunSQL(["ALTER TABLE y_edc_platforms MODIFY COLUMN create_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"]),
        migrations.RunSQL(["ALTER TABLE y_edc_study_sites MODIFY COLUMN create_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"]),
        migrations.RunSQL(["ALTER TABLE y_edc_studies MODIFY COLUMN create_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"]),
        migrations.RunSQL(["ALTER TABLE y_edc_study_sites MODIFY COLUMN create_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)"]),

        migrations.RunSQL(["ALTER TABLE y_edc_illnesses MODIFY COLUMN update_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);"]),
        migrations.RunSQL(["ALTER TABLE y_edc_organizers MODIFY COLUMN update_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);"]),
        migrations.RunSQL(["ALTER TABLE y_edc_platforms MODIFY COLUMN update_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);"]),
        migrations.RunSQL(["ALTER TABLE y_edc_studies MODIFY COLUMN update_time datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);"]),
    ]
