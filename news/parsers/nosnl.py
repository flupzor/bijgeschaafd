from pyquery import PyQuery as pq

from baseparser import BaseParser

from .utils import html_to_text


class NOSNLParser(BaseParser):
    short_name = 'nos.nl'
    full_name = 'NOS.nl'

    domains = ['www.nos.nl']

    feeder_base = 'http://www.nos.nl'
    feeder_pat = '^http://www.nos.nl/artikel/'
    feeder_pages = ['http://www.nos.nl/', ]

    def _parse(self, html):
        d = pq(html)

        self.title = d.find('article h1.article__title').text()
        self.body = html_to_text(d.find('article .article_body'))
        self.date = d.find('time').attr('datetime')
        self.byline = ''

