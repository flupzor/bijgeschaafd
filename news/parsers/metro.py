from pyquery import PyQuery as pq

from baseparser import BaseParser

from .utils import html_to_text


class MetroParser(BaseParser):
    domains = ['www.metronieuws.nl/']

    feeder_base = 'http://www.metronieuws.nl/'
    feeder_pat = '^http://www.metronieuws.nl/\w+/\w+/\d+/\d+/\w+'
    feeder_pages = ['http://www.metronieuws.nl/', ]

    def _parse(self, html):
        d = pq(html)

        self.title = d.find("#content .row").eq(0).find('h1').text()

        rows = d.find("#content .row")

        def exclude_cb(element, parent, level):
            css_class = element.get('class', None)
            css_id = element.get('id', None)

            data_provider = element.get('data-provider')

            if data_provider == 'leesook':
                return True

            return False

        self.body = html_to_text(rows.eq(1).find('.field'), exclude_fn=exclude_cb)

        self.date = d.find('span[property="dc:date dc:created"]').text()
        self.byline = ''
