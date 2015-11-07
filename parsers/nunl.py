from pyquery import PyQuery as pq

from baseparser import BaseParser


class NuNLParser(BaseParser):
    SUFFIX = ''
    domains = ['www.nu.nl']

    feeder_base = 'http://www.nu.nl/'
    feeder_pat = '^http://www.nu.nl/\w+/\d+/'
    feeder_pages = ['http://www.nu.nl/', ]

    def _parse(self, html):
        d = pq(html)

        self.title = d.find(
            "div[data-sac-marker='block.article.header'] div.title"
        ).text()

        excerpt = d.find(
            "div[data-sac-marker='block.article.header'] div.item-excerpt"
        ).text()
        content = d.find("div[data-sac-marker='block.article.body']").text()
        self.body = excerpt + content

        self.date = d.find("div[data-sac-marker='block.article.header'] div.dates span.published span.small").text()
        self.byline = ''
