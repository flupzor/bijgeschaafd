import json
import re
from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

from news.parsers import get_parser
from news.parsers.exceptions import ParserDoesNotExist


def ancient():
    return datetime(1901, 1, 1, tzinfo=timezone.get_current_timezone())


class Article(models.Model):
    class Meta:
        db_table = 'Articles'

    url = models.CharField(max_length=255, blank=False, unique=True,
                           db_index=True)
    initial_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(default=ancient)
    last_check = models.DateTimeField(default=ancient)

    source = models.CharField(max_length=255, blank=False, db_index=True)

    def filename(self):
        return self.url[len('http://'):].rstrip('/')

    def publication(self):
        try:
            parser = get_parser(self.source)
        except ParserDoesNotExist:
            return ''

        return parser.full_name

    def versions(self):
        return self.version_set.filter(boring=False).order_by('date')

    def latest_version(self):
        return self.versions().latest()

    def first_version(self):
        return self.versions()[0]

    def minutes_since_update(self):
        delta = timezone.now() - max(self.last_update, self.initial_date)
        return delta.seconds // 60 + 24*60*delta.days

    def minutes_since_check(self):
        delta = timezone.now() - self.last_check
        return delta.seconds // 60 + 24*60*delta.days


class Version(models.Model):
    article = models.ForeignKey('Article', null=False)
    title = models.CharField(max_length=255, blank=False)
    byline = models.CharField(max_length=255, blank=False)
    date = models.DateTimeField(blank=False)
    boring = models.BooleanField(blank=False, default=False)
    diff_json = models.CharField(max_length=255, null=True)

    content_sha1 = models.CharField(max_length=40, null=True, db_index=True)
    content = models.TextField(default="")

    class Meta:
        db_table = 'version'
        get_latest_by = 'date'
        ordering = ['-date', ]

    def text(self):
        return self.content

    def get_diff_info(self):
        if self.diff_json is None:
            return {}
        return json.loads(self.diff_json)

    def set_diff_info(self, val=None):
        if val is None:
            self.diff_json = None
        else:
            self.diff_json = json.dumps(val)
    diff_info = property(get_diff_info, set_diff_info)
