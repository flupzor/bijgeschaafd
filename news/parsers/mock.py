from django.utils import timezone
from baseparser import BaseParser

from news.parsers.exceptions import NotInteresting


class MockParser(BaseParser):
    short_name = 'mock.nl'
    full_name = 'Mock'

    article_list = 'http://www.mock.nl/'
    url_filter = '^http://www.mock.nl/\w+/'
    url_exclude = []

    version_counter = {}

    updates = True

    set_to_boring = False

    @classmethod
    def _http_get(cls, url):
        return '', {'addr': None, 'port': None}

    @classmethod
    def parse_new_version(cls, url, html):
        cls.version_counter.setdefault(url, 0)

        if cls.updates:
            MockParser.version_counter[url] += 1

        current_article = cls.version_counter[url]

        title = u'\u1d90rticle {} {}'.format(url, current_article)
        date = timezone.now().date()
        content = u'Body \u1d00 {} {}'.format(url, current_article)
        if cls.set_to_boring:
            raise NotInteresting()

        return {
            'title': title,
            'date': date,
            'content': content,
        }

    @classmethod
    def request_urls(cls):
        return [
            'http://www.mock.nl/mock_article1.html',
            'http://www.mock.nl/mock_article2.html',
        ]
