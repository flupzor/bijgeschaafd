from baseparser import BaseParser
from pyquery import PyQuery as pq

from ..dateparsers import NosNLDateParser
from .utils import html_to_text


class NOSNLParser(BaseParser):
    short_name = 'nos.nl'
    full_name = 'NOS.nl'

    article_list = 'http://www.nos.nl'
    url_filter = '^http://www.nos.nl/artikel/'
    url_exclude = []

    dateparser = NosNLDateParser

    @classmethod
    def parse_new_version(cls, url, html):
        d = pq(html)

        title = d.find('article h1.article__title').text()
        content = html_to_text(d.find('article .article_body'))

        # TODO: I'm doubtful if this css selector is correct all the time.
        date = cls.dateparser.process(d.find('time').attr('datetime'))

        return {
            'title': title,
            'content': content,
            'date': date,
        }
