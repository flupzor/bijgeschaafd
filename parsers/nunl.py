from pyquery import PyQuery as pq
import lxml

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

        def _parse_content(element, parent=None, level=0):
            add_tail = False
            add_text = False
            add_newline = False
            look_at_children = True

            if isinstance(element, lxml.etree._Comment):
                if parent.tag == 'p' or parent.tag == 'a' or \
                   parent.tag == 'br':
                    add_tail = True
                add_text = False
                look_at_children = False

            if element.tag == 'div' and \
               element.get('data-sac-marker', None) == 'block.slideshow':
                add_tail = False
                add_text = False
                look_at_children = False

            elif element.tag == 'div' and \
                 element.get('data-sac-marker', None) == 'block.articlelink':
                add_tail = False
                add_text = False
                look_at_children = False
            elif element.tag == 'script':
                if parent.tag == 'p':
                    add_tail = True
                add_text = False
                look_at_children = False
            elif element.tag == 'br':
                add_tail = True
                add_text = False
                add_newline = True
                look_at_children = False
            elif element.tag == 'p':
                add_tail = False
                add_text = True
                add_newline = True
                look_at_children = True
            elif element.tag == 'em':
                add_tail = True
                add_text = True
                look_at_children = True
            elif element.tag == 'a':
                if parent.tag == 'p':
                    add_tail = True
                add_text = True
                look_at_children = True
            elif element.tag == 'h1' or element.tag == 'h2' or \
                    element.tag == 'h3':
                add_tail = True
                add_text = True
                add_newline = True
                look_at_children = True

            text = []

#            print "{} tag: {}: text: '{}' ({}) tail: '{}' ({}) newline: {}".format(
#                level,
#                element.tag,
#                "None" if element.text is None else element.text.encode("unicode-escape"),
#                "y" if add_text else "n",
#                "None" if element.tail is None else element.tail.encode("unicode-escape"),
#                "y" if add_tail else "n",
#                "y" if add_newline else "n"
#            )

            if add_text and element.text:
                text += [element.text, ]

            if look_at_children:
                for child in element.getchildren():
                    text += _parse_content(child, element, level=level+1)

            if add_newline:
                text += ['\n']

            if add_tail and element.tail:
                text += [element.tail, ]

            return text

        def parse_content(elements):
            if isinstance(elements, lxml.etree._Element) \
               and elements.tag == 'script':
                return u''

            text = []
            for element in elements:
                text += _parse_content(element)

            return ''.join([p for p in text])

        # Filter out:
        # data-sac-marker="block.slideshow"

        excerpt = html_to_text(d.find("div[data-sac-marker='block.article.header'] div.item-excerpt"))
        content = parse_content(d.find("div[data-sac-marker='block.article.body']"))

        self.body = u'{excerpt}\n{content}'.format(excerpt=excerpt, content=content)

        self.date = d.find("div[data-sac-marker='block.article.header'] div.dates span.published span.small").text()
        self.byline = ''
