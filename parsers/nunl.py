from pyquery import PyQuery as pq

from baseparser import BaseParser

from .utils import html_to_text


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

        # Filter out:
        # data-sac-marker="block.slideshow"

        excerpt = html_to_text(d.find("div[data-sac-marker='block.article.header'] div.item-excerpt"))
        content = html_to_text(d.find("div[data-sac-marker='block.article.body']"))

        self.body = excerpt + content

        self.date = d.find("div[data-sac-marker='block.article.header'] div.dates span.published span.small").text()
        self.byline = ''
