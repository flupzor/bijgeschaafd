from baseparser import BaseParser
from pyquery import PyQuery as pq

#from BeautifulSoup import BeautifulSoup, Tag


class TelegraafParser(BaseParser):
    domains = ['www.telegraaf.nl']

    feeder_base = 'http://www.telegraaf.nl/'
    feeder_pat  = '^http://www.telegraaf.nl/\w+/\d+/'
    feeder_pages  = ['http://www.telegraaf.nl/', ]

    def _parse(self, html):
        d = pq(html)

        self.title = d.find('#artikel h1').text()
        self.body = d.find('#artikel .wrapper p').text()
        self.date = d.find('.artDatePostings .datum').text()
        self.byline = ''
