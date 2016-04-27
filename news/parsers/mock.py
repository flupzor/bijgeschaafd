from pyquery import PyQuery as pq

from django.utils import timezone
from baseparser import BaseParser

from news.parsers.exceptions import NotInteresting


class MockParser(BaseParser):
    short_name = 'mock.nl'
    full_name = 'Mock'

    article_list = 'http://www.mock.nl/'
    url_filter = '^http://www.mock.nl/\w+/'
    url_exclude = []

    @classmethod
    def parse_new_version(cls, url, html):
        d = pq(html)

        title = d.find('#title').text()
        content = d.find('#content').text()

        if len(d.find('#boring')) > 0:
            raise NotInteresting()

        return {
            'title': title,
            'content': content,
            'date': None
        }

    @classmethod
    def request_urls(cls):
        return [
            'http://www.mock.nl/mock_article1.html',
            'http://www.mock.nl/mock_article2.html',
        ]
