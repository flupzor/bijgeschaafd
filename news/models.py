import json
import re
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from news.parsers import get_parser
from news.parsers.exceptions import ParserDoesNotExist
from news.utils import hash_djb2


class Article(models.Model):
    class Meta:
        db_table = 'Articles'

    url = models.CharField(max_length=255, blank=False, unique=True,
                           db_index=True)
    initial_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField()
    last_check = models.DateTimeField()

    source = models.CharField(max_length=255, blank=False, db_index=True)

    _latest_date = models.DateTimeField(blank=True, null=True)
    _sum_versions = models.IntegerField(default=0)

    # What i've implemented is a undirected weighted graph. Since the edges
    # are undirected the ordering of source and destination doesn't matter.
    # This means: SimilarArticle(from, to, weight) == SimilarArticle(to, from,
    # weight)

    # Which means we have to decide which of the two we want to store. I've
    # decided to store the the article with the lowest id as the source and
    # the article with the highest id as the destination.

    def add_similar_article(self, article, ratio):

        from_article = min(self, article, key=lambda a: a.id)
        to_article = max(self, article, key=lambda a: a.id)

        if from_article == to_article:
            raise Exception("It's not possible to create a similarity relation"
                            "to from and to the same Article. An Article is"
                            "always 100% similar to itself.")

        # XXX: This should throw an Exception when a relation already exists.

        return SimilarArticle.objects.get_or_create(
            from_article=from_article, to_article=to_article,
            ratio=ratio)


    def filename(self):
        return self.url[len('http://'):].rstrip('/')

    def publication(self):
        try:
            parser = get_parser(self.source)
        except ParserDoesNotExist:
            return ''

        return parser.full_name

    def versions(self):
        return self.version_set.all().order_by('date')

    def latest_version(self):
        return self.versions().latest()

    def first_version(self):
        return self.versions()[0]

    @property
    def needs_update(self):
        parser = get_parser(self.source)
        update_delay = parser.get_update_delay(self.time_since_update)

        if update_delay:
            return self.time_since_check - update_delay > timedelta()

        return False

    @property
    def time_since_update(self):
        return timezone.now() - max(self.last_update, self.initial_date)

    @property
    def time_since_check(self):
        return timezone.now() - self.last_check


class SimilarArticle(models.Model):
    from_article = models.ForeignKey(Article, related_name='from_article')
    to_article = models.ForeignKey(Article, related_name='to_article')

    ratio = models.FloatField()

    def __str__(self):
        return "{0} to {1} weight: {2}".format(self.from_article, self.to_article, self.ratio);


class Version(models.Model):
    article = models.ForeignKey('Article', null=False)
    title = models.CharField(max_length=255, blank=False)
    byline = models.CharField(max_length=255, blank=False)
    date = models.DateTimeField(blank=False)
    diff_json = models.CharField(max_length=255, null=True)

    modified_date_in_article = models.DateTimeField(blank=True, null=True, default=None)

    content_sha1 = models.CharField(max_length=40, null=True, db_index=True)
    content = models.TextField(default="")
    content_words_hashed = ArrayField(models.BigIntegerField(), null=True)

    class Meta:
        db_table = 'version'
        get_latest_by = 'date'
        ordering = ['-date', ]

    def save(self, *args, **kwargs):
        super(Version, self).save(*args, **kwargs)

        try:
            latest_date = \
                self.article.version_set.latest('date').date
        except Version.DoesNotExist:
            latest_date = None

        self.article._latest_date = latest_date
        self.article._sum_versions = self.article.version_set.count()
        self.article.save()

    @classmethod
    def new(cls, **kwargs):
        content = kwargs.get('content')

        if content:
            kwargs['content_words_hashed'] = \
                [hash_djb2(word) for word in content.split(' ')]

        return Version(**kwargs)


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


class RequestLog(models.Model):
    date = models.DateTimeField(blank=False)
    source = models.CharField(max_length=255, blank=False, db_index=True)

    url = models.CharField(max_length=255, blank=False, db_index=True)
    server_address = models.CharField(max_length=255, blank=False, db_index=True)

    version = models.ForeignKey('Version', null=True)

