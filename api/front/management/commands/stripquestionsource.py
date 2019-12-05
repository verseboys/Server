# coding: utf-8
from django.core.management.base import BaseCommand, CommandError

import re

from questionsandanswersmodel.models import QuestionsModel

ptn = re.compile(u"<p class='text-rig font-15'>——来自文章:.*</a></p>")

class Command(BaseCommand):
	def handle(self, *args, **options):
		questions = QuestionsModel.objects.filter(relevance_method_article__isnull=False)
		count = 0
		for q in questions:
			q.content = ptn.sub('', q.content)
			q.save(update_fields=['content'])
			count += 1

		self.stdout.write(self.style.HTTP_SUCCESS('processes %s items' % count))
