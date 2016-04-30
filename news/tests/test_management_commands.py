from datetime import timedelta

from django.core.management import call_command
from django.test import TestCase, override_settings
from Levenshtein import ratio as levenshtein_ratio

from ..models import Article, Version, SimilarArticle
from .. import parsers
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
        parsers.reset()

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

        print 'start test_parser_flapping'

        parsers.reset()

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

        print 'end test_parser_flapping'

    @override_settings(NEWS_SOURCES=['news.parsers.mock.MockParser', ])
    @responses.activate
    def test_boring(self):
        parsers.reset()

        self._create_response(
            'http://www.mock.nl/mock_article1.html',
            u'\u1d90rticle 1', u"Body \u1d00 1\n", boring=True)
        call_command('scraper')

        self.assertEquals(Version.objects.count(), 0)

    @override_settings(NEWS_SOURCES=[
        'news.parsers.mock.MockParser', 'news.parsers.mock.SimilarMockParser'])
    @responses.activate
    def test_similarity_checking(self):
        parsers.reset()

        quote1 = \
            "Winston kept his back turned to the telescreen. It was safer; " \
            "though, as he well knew, even a back can be revealing. A " \
            "kilometre away the Ministry of Truth, his place of work, " \
            "towered vast and white above the grimy landscape. This, he " \
            "thought with a sort of vague distaste - this was London, " \
            "chief city of Airstrip One, itself the third most populous of " \
            "the provinces of Oceania. He tried to squeeze out some " \
            "childhood memory that should tell him whether London had " \
            "always been quite like this. Were there always these vistas " \
            "of rotting nineteenth-century houses, their sides shored up " \
            "with baulks of timber, their windows patched with cardboard " \
            "and their roofs with corrugated iron, their crazy garden walls " \
            "sagging in all directions? And the bombed sites where the plaster " \
            "dust swirled in the air and the willow-herb straggled over the " \
            "heaps of rubble; and the places where the bombs had cleared a " \
            "larger patch and there had sprung up sordid colonies of wooden " \
            "dwellings like chicken-houses? But it was no use, he could not " \
            "remember: nothing remained of his childhood except a series of " \
            "bright-lit tableaux occurring against no background and mostly " \
            "unintelligible.\n"

        quote2 = \
            "The Ministry of Truth - Minitrue, in Newspeak - was " \
            "startlingly different from any other object in sight. It was " \
            "an enormous pyramidal structure of glittering white concrete, " \
            "soaring up, terrace after terrace, 300 metres into the air. " \
            "From where Winston stood it was just possible to read, picked " \
            "out on its white face in elegant lettering, the three slogans " \
            "of the Party:\n" \
            "WAR IS PEACE\n" \
            "FREEDOM IS SLAVERY\n" \
            "IGNORANCE IS STRENGTH\n"

        article1_content = quote1
        article2_content = quote1 + quote2

        self._create_response(
            'http://www.mock.nl/mock_article1.html',
            u'\u1d90rticle 1', article1_content)

        self._create_response(
            'http://www.similarmock.nl/mock_article1.html',
            u'\u1d90rticle 1', article2_content)

        call_command('scraper')

        version1 = Version.objects.get(content=article1_content)
        article1 = version1.article
        version2 = Version.objects.get(content=article2_content)
        article2 = version2.article

        ratio = levenshtein_ratio(
            [int(x) for x in version1.content_words_hashed],
            [int(x) for x in version2.content_words_hashed])

        expected = {
            'to_article': max(article1.pk, article2.pk),
            'from_article': min(article1.pk, article2.pk),
            'ratio': ratio,
        }

        self.assertEquals(SimilarArticle.objects.filter(**expected).count(), 1)
