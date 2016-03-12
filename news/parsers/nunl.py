from pyquery import PyQuery as pq
import lxml

from baseparser import BaseParser

from .utils import html_to_text


class NuNLParser(BaseParser):
    short_name = 'nu.nl'
    full_name = 'NU.nl'

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

        def exclude_cb(element, parent, level):
            if element.tag == 'div' and \
               element.get('data-sac-marker', None) == 'block.slideshow':
                return True

            elif element.tag == 'div' and \
                 element.get('data-sac-marker', None) == 'block.articlelink':
                return True
            elif element.tag == 'div' and \
                 element.get('class', None) == 'copyright':
                return True

            return False

        excerpt = html_to_text(d.find("div[data-sac-marker='block.article.header'] div.item-excerpt"))
        content = html_to_text(d.find("div[data-sac-marker='block.article.body']"), exclude_fn=exclude_cb)

        self.body = u'{excerpt}{content}'.format(excerpt=excerpt, content=content)

        self.date = d.find("div[data-sac-marker='block.article.header'] div.dates span.published span.small").text()
        self.byline = ''

        if len(d.find('div[data-sac-marker="block.liveblog"]')) > 0:
            self.boring = True

        # For now just mark everything in the dvn category as
        # boring. There are interesting things in there, but for
        # it fills up the list with weather etc.
        if "http://www.nu.nl/dvn/" in self.url:
            self.boring = True

        if "http://www.nu.nl/voetbal/" in self.url:
            self.boring = True

        if "http://www.nu.nl/gadgets/" in self.url:
            self.boring = True

