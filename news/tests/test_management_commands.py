from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase, override_settings

from ..models import Article, Version
import responses


class MockParserTests(TestCase):

    def _reset_update_time(self, *articles):
        """ Pretend we did the last check 4 hours ago.  """

        for article in articles:
            article.last_update -= timedelta(hours=4)
            article.last_check -= timedelta(hours=4)
            article.save()

    def _create_response(self, url, title, content, boring=False):
        template = u'<p id="title">{title}</p><p id="content">{content}</p>'
        body = template.format(
            title=title.encode('ascii', 'xmlcharrefreplace'),
            content=content.encode('ascii', 'xmlcharrefreplace')
        )

        if boring:
            body += '<p id="boring">boring</p>'

        responses.add(responses.GET, url,
                      body=body, status=200,
                      content_type='text/html')

    @override_settings(NEWS_SOURCES=['news.parsers.mock.MockParser', ])
    @responses.activate
    def test_parser(self):

        self._create_response(
            u'http://www.mock.nl/mock_article1.html',
            u'\u1d90rticle 1', u"Body \u1d00 1\n")
        self._create_response(
            u'http://www.mock.nl/mock_article2.html',
            u'\u1d90rticle 1', u"Body \u1d00 1\n")

        # Get the initial articles.
        call_command('scraper')

        self.assertEquals(Version.objects.count(), 2)

        # TODO: CHECK DATES
        v1 = Version.objects.get(
            article__url='http://www.mock.nl/mock_article1.html',
            byline='',
            title=u'\u1d90rticle 1',
            diff_json=None,
        )
        a1 = v1.article

        v2 = Version.objects.get(
            article__url='http://www.mock.nl/mock_article2.html',
            byline='',
            title=u'\u1d90rticle 1',
            diff_json=None,
        )
        a2 = v2.article

        self.assertEquals(
            v1.text(),
            u"Body \u1d00 1\n"
        )
        self.assertEquals(
            v2.text(),
            u"Body \u1d00 1\n"
        )

        responses.reset()
        self._create_response(
            u'http://www.mock.nl/mock_article1.html',
            u'\u1d90rticle 2', u"Body \u1d00 2\n")
        self._create_response(
            u'http://www.mock.nl/mock_article2.html',
            u'\u1d90rticle 2', u"Body \u1d00 2\n")

        self._reset_update_time(a1, a2)

        # Get the updates.
        call_command('scraper')

        self.assertEquals(a1.version_set.count(), 2)
        self.assertEquals(a2.version_set.count(), 2)

        self.assertEquals(a1.version_set.exclude(pk=v1.pk).filter(
            article__url='http://www.mock.nl/mock_article1.html',
            byline='',
            diff_json=u'{"chars_removed": 1, "chars_added": 1}',
            title=u'\u1d90rticle 2'
        ).count(), 1)

        self.assertEquals(a2.version_set.exclude(pk=v2.pk).filter(
            article__url='http://www.mock.nl/mock_article2.html',
            byline='',
            diff_json=u'{"chars_removed": 1, "chars_added": 1}',
            title=u'\u1d90rticle 2'
        ).count(), 1)

        self._reset_update_time(a1, a2)

        # Make sure that the same article is ignored.
        self.assertEquals(Version.objects.count(), 4)
        call_command('scraper')
        self.assertEquals(Version.objects.count(), 4)

        self._reset_update_time(a1, a2)

        # Make sure that the article would be downloaded if there
        # was a update.
        responses.reset()
        self._create_response(
            u'http://www.mock.nl/mock_article1.html',
            u'\u1d90rticle 3', u"Body \u1d00 3\n")
        self._create_response(
            u'http://www.mock.nl/mock_article2.html',
            u'\u1d90rticle 3', u"Body \u1d00 3\n")

        self.assertEquals(Version.objects.count(), 4)
        call_command('scraper')
        self.assertEquals(Version.objects.count(), 6)

    @override_settings(NEWS_SOURCES=['news.parsers.mock.MockParser', ])
    @responses.activate
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
        self._create_response(a1_url, u'\u1d90rticle 1', u"Body \u1d00 1\n")
        self._create_response(a2_url, u'\u1d90rticle 1', u"Body \u1d00 1\n")
        call_command('scraper')

        self.assertEquals(Version.objects.count(), 2)

        a1 = Article.objects.get(url=a1_url)
        a2 = Article.objects.get(url=a2_url)

        Version.objects.get(
            article__url=a1.url,
            title=u'\u1d90rticle 1')
        Version.objects.get(
            article__url=a2.url,
            title=u'\u1d90rticle 1')

        # Download version 2 of article 1 and 2
        self._reset_update_time(a1, a2)

        responses.reset()
        self._create_response(a1_url, u'\u1d90rticle 2', u"Body \u1d00 2\n")
        self._create_response(a2_url, u'\u1d90rticle 2', u"Body \u1d00 2\n")

        call_command('scraper')
        self.assertEquals(Version.objects.count(), 4)

        # Download version3 of article 1 and 2
        self._reset_update_time(a1, a2)

        responses.reset()
        self._create_response(a1_url, u'\u1d90rticle 3', u"Body \u1d00 3\n")
        self._create_response(a2_url, u'\u1d90rticle 3', u"Body \u1d00 3\n")

        call_command('scraper')
        self.assertEquals(Version.objects.count(), 6)

        # Download version1 of article1 and version 4 of article2
        self._reset_update_time(a1, a2)

        responses.reset()
        self._create_response(a1_url, u'\u1d90rticle 1', u"Body \u1d00 1\n")
        self._create_response(a2_url, u'\u1d90rticle 4', u"Body \u1d00 4\n")

        call_command('scraper')
        self.assertEquals(Version.objects.count(), 8)

        # Download version 5 of article 1 and 2
        self._reset_update_time(a1, a2)

        responses.reset()
        self._create_response(a1_url, u'\u1d90rticle 5', u"Body \u1d00 5\n")
        self._create_response(a2_url, u'\u1d90rticle 5', u"Body \u1d00 5\n")

        call_command('scraper')
        self.assertEquals(Version.objects.count(), 10)

        # Download version1 of article1 and version6 of article2
        self._reset_update_time(a1, a2)

        responses.reset()
        self._create_response(a1_url, u'\u1d90rticle 1', u"Body \u1d00 1\n")
        self._create_response(a2_url, u'\u1d90rticle 6', u"Body \u1d00 6\n")

        call_command('scraper')
        self.assertEquals(Version.objects.count(), 11)

        # Download version7 of article 1 and 2
        self._reset_update_time(a1, a2)

        responses.reset()
        self._create_response(a1_url, u'\u1d90rticle 7', u"Body \u1d00 7\n")
        self._create_response(a2_url, u'\u1d90rticle 7', u"Body \u1d00 7\n")

        call_command('scraper')
        self.assertEquals(Version.objects.count(), 13)

        # Download version1 of article1 and version 8 of article2
        self._reset_update_time(a1, a2)

        responses.reset()
        self._create_response(a1_url, u'\u1d90rticle 1', u"Body \u1d00 1\n")
        self._create_response(a2_url, u'\u1d90rticle 8', u"Body \u1d00 8\n")

        call_command('scraper')
        self.assertEquals(Version.objects.count(), 14)

    @override_settings(NEWS_SOURCES=['news.parsers.mock.MockParser', ])
    @responses.activate
    def test_boring(self):
        self._create_response(
            'http://www.mock.nl/mock_article1.html',
            u'\u1d90rticle 1', u"Body \u1d00 1\n", boring=True)
        call_command('scraper')

        self.assertEquals(Version.objects.count(), 0)
