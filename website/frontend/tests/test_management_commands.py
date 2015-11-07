from datetime import timedelta
from shutil import rmtree
from tempfile import mkdtemp

import mock
from django.core.management import call_command
from django.test import TestCase

import parsers
from frontend.models import Article, Version
from parsers.mock import MockParser


class ParserTests(TestCase):

    def _reset_update_time(self, *articles):
        """ Pretend we did the last check 4 hours ago.  """

        for article in articles:
            article.last_update -= timedelta(hours=4)
            article.last_check -= timedelta(hours=4)
            article.save()

    @mock.patch('frontend.management.commands.parsers.parsers', new=[MockParser])
    @mock.patch('frontend.management.commands.parsers.parser_dict', {'www.mock.nl': MockParser})
    def test_parser(self):
        # Get the initial articles.
        call_command('scraper')

        self.assertEquals(Version.objects.count(), 2)

        v1 = Version.objects.get(
            boring=False,
            byline='',
            title=u'Article http://www.mock.nl/mock_article1.html 1',
            diff_json=None,
        )
        a1 = v1.article

        v2 = Version.objects.get(
            boring=False,
            byline='',
            title=u'Article http://www.mock.nl/mock_article2.html 1',
            diff_json=None,
        )
        a2 = v2.article

        self._reset_update_time(a1, a2)

        # Get the updates.
        call_command('scraper')

        self.assertEquals(
            v1.text(),
            "Date 1\n"
            "Article http://www.mock.nl/mock_article1.html 1\n"
            "\n"
            "Body http://www.mock.nl/mock_article1.html 1\n"
        )
        self.assertEquals(
            v2.text(),
            "Date 1\n"
            "Article http://www.mock.nl/mock_article2.html 1\n"
            "\n"
            "Body http://www.mock.nl/mock_article2.html 1\n"
        )

        self.assertEquals(a1.version_set.count(), 2)
        self.assertEquals(a2.version_set.count(), 2)

        self.assertEquals(a1.version_set.exclude(pk=v1.pk).filter(
            boring=False,
            byline='',
            diff_json=u'{"chars_removed": 3, "chars_added": 3}',
            title=u'Article http://www.mock.nl/mock_article1.html 2'
        ).count(), 1)

        self.assertEquals(a2.version_set.exclude(pk=v2.pk).filter(
            boring=False,
            byline='',
            diff_json=u'{"chars_removed": 3, "chars_added": 3}',
            title=u'Article http://www.mock.nl/mock_article2.html 2'
        ).count(), 1)

        self._reset_update_time(a1, a2)

        # Make sure that the same article is ignored.
        self.assertEquals(Version.objects.count(), 4)
        with mock.patch('parsers.mock.MockParser.updates', False):
            call_command('scraper')
        self.assertEquals(Version.objects.count(), 4)

        self._reset_update_time(a1, a2)

        # Make sure that the article would be downloaded if there
        # was a update.
        self.assertEquals(Version.objects.count(), 4)
        call_command('scraper')
        self.assertEquals(Version.objects.count(), 6)

    @mock.patch('frontend.management.commands.parsers.parsers', new=[MockParser])
    @mock.patch('frontend.management.commands.parsers.parser_dict', {'www.mock.nl': MockParser})
    def test_parser_flapping(self):
        """

        Test that when the content of a article is the same twice, the
        scraper refuses to store this version again.

        e.g. we receive:

        content1
        content2
        content1 # now we refuse to store, because we've seen content1 before.
        """


        a1_url = 'http://www.mock.nl/mock_article1.html'
        a2_url = 'http://www.mock.nl/mock_article2.html'

        # Download version1 of article 1 and 2
        version_counter = {
            a1_url: 0,
            a2_url: 0,
        }
        with mock.patch('parsers.mock.MockParser.version_counter', version_counter):
            call_command('scraper')

        self.assertEquals(Version.objects.count(), 2)

        a1 = Article.objects.get(url=a1_url)
        a2 = Article.objects.get(url=a2_url)

        Version.objects.get(title='Article {} {}'.format(a1.url, 1))
        Version.objects.get(title='Article {} {}'.format(a2.url, 1))

        # Download version 2 of article 1 and 2
        self._reset_update_time(a1, a2)
        version_counter = {
            a1_url: 1,
            a2_url: 1,
        }
        with mock.patch('parsers.mock.MockParser.version_counter', version_counter):
            call_command('scraper')
        self.assertEquals(Version.objects.count(), 4)

        # Download version3 of article 1 and 2
        self._reset_update_time(a1, a2)
        self._reset_update_time(a1, a2)
        version_counter = {
            a1_url: 2,
            a2_url: 2,
        }
        with mock.patch('parsers.mock.MockParser.version_counter', version_counter):
            call_command('scraper')
        self.assertEquals(Version.objects.count(), 6)

        # Download version1 of article1 and version 4 of article2
        self._reset_update_time(a1, a2)
        version_counter = {
            a1_url: 0,
            a2_url: 3,
        }
        with mock.patch('parsers.mock.MockParser.version_counter', version_counter):
            call_command('scraper')
        self.assertEquals(Version.objects.count(), 8)

        # Download version 4 of article 1 and 2
        self._reset_update_time(a1, a2)
        version_counter = {
            a1_url: 4,
            a2_url: 4,
        }
        with mock.patch('parsers.mock.MockParser.version_counter', version_counter):
            call_command('scraper')
        self.assertEquals(Version.objects.count(), 10)

        # Download version1 of article1 and version6 of article2
        self._reset_update_time(a1, a2)
        version_counter = {
            a1_url: 0,
            a2_url: 5,
        }
        with mock.patch('parsers.mock.MockParser.version_counter', version_counter):
            call_command('scraper')
        self.assertEquals(Version.objects.count(), 11)

        # Download version7 of article 1 and 2
        self._reset_update_time(a1, a2)
        version_counter = {
            a1_url: 6,
            a2_url: 6,
        }
        with mock.patch('parsers.mock.MockParser.version_counter', version_counter):
            call_command('scraper')
        self.assertEquals(Version.objects.count(), 13)

        # Download version1 of article1 and version 8 of article2
        self._reset_update_time(a1, a2)
        version_counter = {
            a1_url: 0,
            a2_url: 7,
        }
        with mock.patch('parsers.mock.MockParser.version_counter', version_counter):
            call_command('scraper')
        self.assertEquals(Version.objects.count(), 14)
