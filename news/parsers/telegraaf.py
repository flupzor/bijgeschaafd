from baseparser import BaseParser
from pyquery import PyQuery as pq

from .exceptions import NotInteresting
from .utils import html_to_text


class TelegraafParser(BaseParser):
    short_name = 'telegraaf.nl'
    full_name = 'Telegraaf'

    article_list = 'http://www.telegraaf.nl/'
    url_filter = '^http://www.telegraaf.nl/\w+/\d+/'
    url_exclude = [
    "^http://www.telegraaf.nl/prive/",
    "^http://www.telegraaf.nl/autovisie",
    "^http://www.telegraaf.nl/reiskrant/",
    "^http://www.telegraaf.nl/vaarkrant/",
    "^http://www.telegraaf.nl/telesport/",
    "^http://www.telegraaf.nl/vrouw/",
    "^http://www.telegraaf.nl/avond/",
    ]

    @classmethod
    def parse_new_version(cls, url, html):
        d = pq(html)

        def exclude_cb(element, parent, level):
            css_class = element.get('class', None)
            css_id = element.get('id', None)

            if element.tag == 'h1':
                return True

            if css_class and "tg-related-articles" in css_class:
                return True

            if css_class and "tg-related-articles" in css_class:
                return True

            if element.tag == 'span' and css_class == 'ui-table-cell ui-tab-gothic-bold ui-text-tiny':
                return True

            if css_class == 'topbar':
                return True

            if css_class == 'premiumline':
                return True

            if css_class == 'premiumoverlaytop':
                return True

            if css_class == 'premiumheader':
                return True

            if css_class == 'kolomRelated':
                return True

            if css_class == 'bannercenter clearfix artspacer':
                return True

            if css_id == 'wuzcontainer':
                return True

            if css_id == 'videoBlockMostWatched':
                return True

            if css_id == 'spotXAd':
                return True

            if css_id == 'twitter-widget-0':
                return True

            if css_class == 'broodtxt':
                return True

            if css_class == 'twitter-timeline':
                return True

            return False

        title = d.find('.tg-article-page h1').text()
        content = html_to_text(d.find('.tg-article-page'), exclude_fn=exclude_cb)
        date = None

        return {
            'title': title,
            'content': content,
            'date': date,
        }
