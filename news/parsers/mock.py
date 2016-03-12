from baseparser import BaseParser


class MockParser(BaseParser):
    short_name = 'mock.nl'
    full_name = 'Mock'

    SUFFIX = ''
    domains = ['www.mock.nl']

    feeder_base = 'http://www.mock.nl/'
    feeder_pat = '^http://www.mock.nl/\w+/'
    feeder_pages = ['http://www.mock.nl/', ]

    version_counter = {}

    updates = True

    set_to_boring = False

    def __init__(self, url):
        MockParser.version_counter.setdefault(url, 0)

        if self.updates:
            MockParser.version_counter[url] += 1

        current_article = MockParser.version_counter[url]
        self.title = u'\u1d90rticle {} {}'.format(url, current_article)
        self.date = u'\u1d81ate {}'.format(current_article)
        self.byline = ''
        self.body = u'Body \u1d00 {} {}'.format(url, current_article)
        self.boring = self.set_to_boring

    @classmethod
    def feed_urls(cls):
        return [
            cls.feeder_base + 'mock_article1.html',
            cls.feeder_base + 'mock_article2.html',
        ]
