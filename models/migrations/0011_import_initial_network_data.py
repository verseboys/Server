# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0010_network_networkapplication_networkmember')
    ]

    operations = [
            migrations.RunSQL(["INSERT INTO y_network(id, name, description) VALUES (1, '慢阻肺临床研究专项', '%s');" %
                """慢阻肺是最常见的慢性呼吸系统疾病，在我国，慢阻肺具有高患病率、高致残率、高病死率和高疾病负担的“四高”特点，已成为我国最为突出的公共卫生与医疗问题之一。

结合慢阻肺面临的问题，真实世界研究在慢阻肺中的价值，中国宋庆龄基金会呼吸疾病临床研究公益基金设立了“慢阻肺临床研究专项”（简称“慢阻肺专项”），用于支持慢阻肺防治技术的临床研究项目。计划开展慢阻肺危险因素、病因、发病机制研究，慢阻肺急性加重预警与救治体系构建研究，慢阻肺规范诊治和长期管理研究等三项重点任务。

通过“慢阻肺专项”，将构建面向真实世界研究的慢阻肺精准医学大数据平台。把临床数据、生物信息和统计、实验室和分子检测数据、大数据和人工智能技术、云计算等多个学科领域融合在一起，从数据中获取洞察，助推临床和科研，为慢阻肺临床实践提供智慧、精准的决策支持。
                """
                ]),
            ]
