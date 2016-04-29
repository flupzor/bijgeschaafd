from pyquery import PyQuery as pq

from baseparser import BaseParser

from news.parsers.exceptions import NotInteresting


class BaseMockParser(BaseParser):
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


class MockParser(BaseMockParser):
    short_name = 'mock.nl'
    full_name = 'Mock'

    article_list = 'http://www.mock.nl/'
    url_filter = '^http://www.mock.nl/\w+/'
    url_exclude = []

    @classmethod
    def request_urls(cls):
        return [
            'http://www.mock.nl/mock_article1.html',
            'http://www.mock.nl/mock_article2.html',
        ]


class SimilarMockParser(BaseMockParser):
    short_name = 'similarmock.nl'
    full_name = 'SimilarMock'

    article_list = 'http://www.similarmock.nl/'
    url_filter = '^http://www.similarmock.nl/\w+/'
    url_exclude = []

    @classmethod
    def request_urls(cls):
        return [
            'http://www.similarmock.nl/mock_article1.html',
            'http://www.similarmock.nl/mock_article2.html',
        ]
