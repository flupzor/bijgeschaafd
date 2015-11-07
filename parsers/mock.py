from baseparser import BaseParser


class MockParser(BaseParser):
    SUFFIX = ''
    domains = ['www.mock.nl']

    feeder_base = 'http://www.mock.nl/'
    feeder_pat = '^http://www.mock.nl/\w+/'
    feeder_pages = ['http://www.mock.nl/', ]

    version_counter = {}

    updates = True

    def __init__(self, url):

        MockParser.version_counter.setdefault(url, 0)

        if self.updates:
            MockParser.version_counter[url] += 1

        current_article = MockParser.version_counter[url]
        self.title = 'Article {} {}'.format(url, current_article)
        self.date = 'Date {}'.format(current_article)
        self.byline = ''
        self.body = 'Body {} {}'.format(url, current_article)
        self.boring = False

    @classmethod
    def feed_urls(cls):
        return [
            cls.feeder_base + 'mock_article1.html',
            cls.feeder_base + 'mock_article2.html',
        ]
