from pyquery import PyQuery as pq

from baseparser import BaseParser

from .utils import html_to_text
from ..dateparsers import MetroDateParser


class MetroParser(BaseParser):
    short_name = 'metronieuws.nl'
    full_name = 'Metro'

    article_list = 'http://www.metronieuws.nl/'
    url_filter = '^http://www.metronieuws.nl/\w+/\w+/\d+/\d+/\w+'
    url_exclude = [
        '^http://www.metronieuws.nl/xl/',
        '^http://www.metronieuws.nl/lifestyle/',
    ]
    dateparser = MetroDateParser

    @classmethod
    def parse_new_version(cls, url, html):
        d = pq(html)

        def exclude_cb(element, parent, level):
            css_class = element.get('class', None)
            css_id = element.get('id', None)

            data_provider = element.get('data-provider')

            if data_provider == 'leesook':
                return True

            return False

        rows = d.find("#content .row")

        title = d.find("#content .row").eq(0).find('h1').text()
        content = html_to_text(rows.eq(1).find('.field'), exclude_fn=exclude_cb)
        date = cls.dateparser.process(
            d.find('span[property="dc:date dc:created"]').text())

        return {
            'title': title,
            'content': content,
            'date': date,
        }
