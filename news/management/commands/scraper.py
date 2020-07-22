import hashlib
import logging
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils import timezone

from news.models import Article, Version
from news.parsers import all_parsers, load_article
from news.utils import get_diff_info, is_boring

logger = logging.getLogger('scraper')


class Command(BaseCommand):
    help = "Scrape articles which need updating."

    def handle(self, *args, **options):
        for parser in all_parsers():
            parser.update()
