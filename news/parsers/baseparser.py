import hashlib
from datetime import timedelta
import logging
import re
import socket
import sys
import time

from pyquery import PyQuery as pq
from django.db import transaction
from django.utils import timezone
from raven.contrib.django.raven_compat.models import client

from news.models import RequestLog, Article, Version
from news.parsers.exceptions import NotInteresting
from news.utils import get_diff_info, is_boring, canonicalize, http_get

from urlparse import urljoin, urlsplit, urlunsplit

logger = logging.getLogger(__name__)


class BaseParser(object):
    short_name = None
    full_name = None

    article_list = None
    url_filter = None
    url_exclude = []

    @classmethod
    def request_urls(cls):
        html, _ = http_get(cls.article_list)
        d = pq(html)

        urls = [a.get('href', '') for a in d.find('a')]

        doc_scheme, doc_netloc, doc_path, _, _ = urlsplit(cls.article_list)

        absolute_urls = []
        for url in urls:
            scheme, netloc, path, query, _ = urlsplit(url)

            # If this is a relative URL construct an absolute one.
            if scheme == '' and netloc == '':
                scheme, netloc, path = \
                     doc_scheme, doc_netloc, urljoin(doc_path, path)

            # We forget the fragment, to normalize the url.
            absolute_urls.append(urlunsplit((scheme, netloc, path, query, '')))

        filtered_urls = [url for url in absolute_urls if re.search(cls.url_filter, url)]

        for exclude in cls.url_exclude:
            filtered_urls = [url for url in filtered_urls if not re.search(exclude, url)]

        return set(filtered_urls)

    @classmethod
    def get_update_delay(cls, time_since_update):
        if time_since_update < timedelta(hours=3):
            return timedelta(minutes=15)
        elif time_since_update < timedelta(days=1):
            return timedelta(hours=1)
        elif time_since_update < timedelta(days=7):
            return timedelta(hours=3)
        elif time_since_update < timedelta(days=30):
            return timedelta(days=3)
        elif time_since_update < timedelta(days=360):
            return timedelta(days=30)
        else:
            return None

    @classmethod
    def get_or_instantiate_articles(cls):
        for url in cls.request_urls():
            try:
                article = Article.objects.get(url=url)

                assert article.source == cls.short_name, "The same URL is used for two different sources"
            except Article.DoesNotExist:
                article = Article(
                    url=url,
                    source=cls.short_name
                )

            yield article

    @classmethod
    def parse_new_version(cls, url, content):
        raise NotImplementedError()

    @classmethod
    def request_new_version(cls, article, content):
        current_time = timezone.now()

        parsed_data = cls.parse_new_version(article.url, content)

        to_store = unicode(
            canonicalize(u'\n'.join((parsed_data.get('date', ''), parsed_data.get('title', ''), '', parsed_data.get('content', ''),)))
        ).encode('utf-8')


        to_store_sha1 = hashlib.sha1(to_store).hexdigest()
        boring = parsed_data.get('boring', False)

        diff_info = None

        try:
            latest_version = article.version_set.latest()
        except Version.DoesNotExist:
            latest_version = None

        if latest_version:
            latest_version_content = latest_version.content.encode('utf-8')

            if latest_version_content == to_store:
                raise NotInteresting()

            if article.version_set.filter(
                    content_sha1=to_store_sha1).count() >= 2:
                raise NotInteresting()

            if is_boring(latest_version_content, to_store):
                raise NotInteresting()

            diff_info = get_diff_info(latest_version_content, to_store)

        version = Version(
            boring=boring,
            title=parsed_data.get('title'),
            byline='',
            date=current_time,
            content=to_store,
            content_sha1=to_store_sha1,
        )
        version.diff_info = diff_info
        article.last_update = current_time
        article.last_check = current_time

        return article, version

    @classmethod
    def _create_new_version(cls, article):
        current_time = timezone.now()

        content, request_info = http_get(article.url)

        try:
            _new_article, _new_version = cls.request_new_version(article, content)
        except NotInteresting:
            if article.pk:
                article.last_check = current_time
                article.save()
        else:
            with transaction.atomic():
                _new_article.save()
                _new_version.article = _new_article
                _new_version.save()


        requestlog = RequestLog.objects.create(
            date=timezone.now(),
            source=article.source,
            url=article.url,
            server_address="{addr}:{port}".format(addr=request_info['addr'], port=request_info['port'])
        )

    @classmethod
    def create_new_version(cls, article):
        try:
            cls._create_new_version(article)
        except Exception:
            client.captureException()

    @classmethod
    def update(cls):
        for new_article in cls.get_or_instantiate_articles():
            cls.create_new_version(new_article)

        for article in Article.objects.filter(source=cls.short_name):
            if article.needs_update:
                cls.create_new_version(article)
