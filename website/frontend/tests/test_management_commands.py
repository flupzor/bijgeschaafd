import mock
from tempfile import mkdtemp
from shutil import rmtree

from datetime import timedelta

from django.test import TestCase

from django.core.management import call_command

import parsers

from parsers.mock import MockParser
from frontend.models import Article, Version

class ParserTests(TestCase):
    @mock.patch('frontend.management.commands.parsers.parsers', new=[MockParser])
    @mock.patch('frontend.management.commands.parsers.parser_dict', {'www.mock.nl': MockParser})
    def test_parser(self):
        GIT_DIR = mkdtemp() + '/'

        # Get the initial articles.
        with mock.patch('frontend.models.GIT_DIR', new=GIT_DIR):
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

        # Pretend we downloaded the articles four hours ago.
        a1.last_update -= timedelta(hours=4)
        a1.last_check -= timedelta(hours=4)
        a1.save()

        a2.last_update -= timedelta(hours=4)
        a2.last_check -= timedelta(hours=4)
        a2.save()

        # Get the updates.
        with mock.patch('frontend.models.GIT_DIR', new=GIT_DIR):
            call_command('scraper')

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

        rmtree(GIT_DIR)
