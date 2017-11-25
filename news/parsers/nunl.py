import lxml
from baseparser import BaseParser
from pyquery import PyQuery as pq

from ..dateparsers import NuNLDateParser
from .exceptions import NotInteresting
from .utils import html_to_text


class NuNLParser(BaseParser):
    short_name = 'nu.nl'
    full_name = 'NU.nl'

    article_list = 'http://www.nu.nl/'
    url_filter = '^http://www.nu.nl/\w+/\d+/'
    url_exclude = [
        '^http://www.nu.nl/voetbal/',
        '^http://www.nu.nl/gadgets/',
        '^http://www.nu.nl/sport/',
        '^http://www.nu.nl/wielrennen/',
        '^http://www.nu.nl/autoweek/',
        '^http://www.nu.nl/film/',
        '^http://www.nu.nl/lifestyle/',
    ]

    dateparser = NuNLDateParser

    @classmethod
    def parse_new_version(cls, url, html):
        d = pq(html)

        def exclude_cb(element, parent, level):
            if element.tag == 'div' and \
               element.get('data-sac-marker', None) == 'block.slideshow':
                return True

            elif element.tag == 'div' and \
                 element.get('data-sac-marker', None) == 'block.articlelink':
                return True
            elif element.tag == 'div' and \
                 element.get('data-sac-marker', None) == 'block.kieskeurig':
                return True
            elif element.tag == 'div' and \
                 element.get('data-sac-marker', None) == 'block.video':
                return True
            elif element.tag == 'div' and \
                 element.get('data-sac-marker', None) == 'block.weather.forecast':
                return True
            elif element.tag == 'div' and \
                 element.get('class', None) == 'copyright':
                return True

            return False

        title = d.find(
            "div[data-sac-marker='block.article.header'] div.title"
        ).text()

        excerpt = html_to_text(d.find("div[data-sac-marker='block.article.header'] div.item-excerpt"))
        body = html_to_text(d.find("div[data-sac-marker='block.article.body']"), exclude_fn=exclude_cb)

        content = u'{excerpt}{body}'.format(excerpt=excerpt, body=body)
        date = cls.dateparser.process(
            d.find("div[data-sac-marker='block.article.header'] div.dates span.published span.small").text()
        )

        if len(d.find('div[data-sac-marker="block.liveblog"]')) > 0:
            raise NotInteresting()

        return {
            'title': title,
            'content': content,
            'date': date,
        }
