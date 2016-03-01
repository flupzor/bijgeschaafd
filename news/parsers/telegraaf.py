from pyquery import PyQuery as pq

from baseparser import BaseParser

from .utils import html_to_text


class TelegraafParser(BaseParser):
    domains = ['www.telegraaf.nl']

    feeder_base = 'http://www.telegraaf.nl/'
    feeder_pat = '^http://www.telegraaf.nl/\w+/\d+/'
    feeder_pages = ['http://www.telegraaf.nl/', ]

    def _parse(self, html):
        d = pq(html)

        def exclude_cb(element, parent, level):
            css_class = element.get('class', None)
            css_id = element.get('id', None)

            if css_class == 'kolomRelated':
                return True

            if css_class == 'bannercenter clearfix artspacer':
                return True

            if css_id == 'wuzcontainer':
                return True

            if css_class == 'broodtxt':
                return True

            return False

        self.title = d.find('#artikel h1').text()
        self.body = html_to_text(d.find('#artikel #artikelKolom'), exclude_fn=exclude_cb)
        self.date = d.find('.artDatePostings .datum').text()
        self.byline = ''

        if "http://www.telegraaf.nl/prive/" in self.url:
            self.boring = True

        if "http://www.telegraaf.nl/autovisie" in self.url:
            self.boring = True

        if "http://www.telegraaf.nl/reiskrant/" in self.url:
            self.boring = True
