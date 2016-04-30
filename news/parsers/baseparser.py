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
from Levenshtein import ratio as levenshtein_ratio
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
        logger.debug(
            "Retrieving the article list for source: %s from: %s",
            cls.short_name, cls.article_list
        )

        html, _ = cls._http_get(cls.article_list)
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

        url_filter_list = cls.url_filter
        if not (type(cls.url_filter) is list or type(cls.url_filter) is tuple):
            url_filter_list = [cls.url_filter, ]

        filtered_urls = []
        for url_filter in url_filter_list:
            filtered_urls += [url for url in absolute_urls
                              if re.search(url_filter, url)]

        for exclude in cls.url_exclude:
            filtered_urls = [url for url in filtered_urls
                             if not re.search(exclude, url)]

        return set(filtered_urls)

    @classmethod
    def get_update_delay(cls, time_since_update):
        if time_since_update < timedelta(hours=3):
            return timedelta(minutes=15)
        elif time_since_update < timedelta(days=1):
            return timedelta(hours=1)
        elif time_since_update < timedelta(days=10):
            return timedelta(hours=3)
        else:
            return None

    @classmethod
    def get_or_instantiate_articles(cls):
        for url in cls.request_urls():
            try:
                article = Article.objects.get(url=url)

                assert article.source == cls.short_name, "The same URL is used for two different sources"
            except Article.DoesNotExist:
                print 'NEW ARTICLE: {} for {}'.format(url, cls.short_name)
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
            canonicalize(parsed_data.get('content', ''))).encode('utf-8')
        to_store_sha1 = hashlib.sha1(to_store).hexdigest()

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

        version = Version.new(
            title=parsed_data.get('title'),
            modified_date_in_article=parsed_data.get('date'),
            byline='',
            date=current_time,
            content=to_store,
            content_sha1=to_store_sha1,
        )
        version.diff_info = diff_info
        article.last_update = current_time
        article.last_check = current_time

        print 'request_new_version {}'.format(article.url)

        return article, version

    @classmethod
    def _http_get(cls, url):
        """
        Convenience method for mocking.
        """
        return http_get(url)

    @classmethod
    def _create_new_version(cls, article):
        current_time = timezone.now()

        logger.debug("Retrieving article: %s", article.url)
        content, request_info = cls._http_get(article.url)

        try:
            _new_article, _new_version = cls.request_new_version(article, content)
        except NotInteresting:
            print 'notintersting {}'.format(article.url)
            if article.pk:
                article.last_check = current_time
                article.save()

            _new_article, _new_version = None, None
        else:
            print 'saving: {}'.format(article.url)
            with transaction.atomic():
                _new_article.save()
                _new_version.article = _new_article
                _new_version.save()

        requestlog = RequestLog.objects.create(
            date=timezone.now(),
            source=article.source,
            url=article.url,
            version=_new_version,
            server_address="{addr}:{port}".format(addr=request_info['addr'], port=request_info['port'])
        )

        return _new_version

    @classmethod
    def create_new_version(cls, article):
        try:
            return cls._create_new_version(article)
        except Exception:
            client.captureException(extra={
                'article_url': article.url,
            })

            return None

    @classmethod
    def compare_articles(cls, a1, a2):
        if a1.content == a2.content:
            return 1.0

        # TODO: For some reason these numbers are returned
        # as a long integer. While a BigIntegerField should
        # always fit into a normal Integer.
        return levenshtein_ratio(
            [int(x) for x in a1.content_words_hashed],
            [int(x) for x in a2.content_words_hashed])

    @classmethod
    def find_similar_articles(cls, new_articles):
        current_time = timezone.now()
        yesterday = current_time - timedelta(days=1)

        articles = Article.objects.filter(
            initial_date__gte=yesterday,
        )

        logger.debug("Comparing against %d articles", articles.count())

        for new_article in new_articles:
            for article in articles:
                # We don't care if websites copy from themselves.
                if new_article.source == article.source:
                    continue

                try:
                    new_version = new_article.version_set.earliest('date')
                    version = article.version_set.earliest('date')
                except Version.DoesNotExist:
                    continue

                ratio = cls.compare_articles(new_version, version)
                if ratio > 0.6:
                    logger.debug("Found one that is intersting. %d -> %d", new_article.pk, article.pk)
                    new_article.add_similar_article(article, ratio)

    @classmethod
    def update(cls):
        new_articles = []

        print '{}->update'.format(cls.__name__)

        # Scrape the frontpage and download the articles found.
        for unsaved_new_article in cls.get_or_instantiate_articles():
            new_version = cls.create_new_version(unsaved_new_article)
            if new_version:
                new_article = new_version.article
                new_articles.append(new_article)

        cls.find_similar_articles(new_articles)

        # Look for existing articles that need an update, an download them
        # if they do.
        for article in Article.objects.filter(source=cls.short_name):
            if article.needs_update:
                cls.create_new_version(article)
