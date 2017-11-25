import hashlib
import logging
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from elasticsearch import Elasticsearch, helpers
from news.models import Article, Version
from news.parsers import all_parsers, load_article
from news.utils import get_diff_info, is_boring

logger = logging.getLogger('scraper')



class Command(BaseCommand):
    help = "Index all articles into elasticsearch"

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Very naive implementation of an indexer. This will probably be better implemented
        using walking over batches of versions (saving memory). Also creating the indexes
        should probably be somewhat configurable.
        """
        versions_to_index = Version.objects.all()
        # TODO: If you would run a second indexer it would have to wait until the first
        # indexer has finished. Which is fine for now.
        versions = versions_to_index.select_for_update().order_by('-date').values(
            'pk', 'title', 'content', 'date'
        )

        actions = [{
            '_index': 'bijgeschaafd',
            '_type': 'document',
            '_id': version['pk'],
            '_source': {
                "title": version['title'],
                "body": version['content'],
                "date": version['date']
            }
        } for version in versions]

        client = Elasticsearch()
        helpers.bulk(client, actions)

        Version.objects.filter(pk__in=[version['pk'] for version in versions]).update(indexed=True)
