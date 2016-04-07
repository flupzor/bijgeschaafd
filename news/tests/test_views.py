from datetime import timedelta, datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.formats import localize
from django.utils.timezone import localtime
from django_webtest import WebTest

from .factory_models import ArticleFactory, VersionFactory


class ViewTests(WebTest):
    def test_browse(self):
        """
        Test that the browse view is sorted properly.
        """

        tz = timezone.get_default_timezone()

        update_time = tz.localize(datetime(2015, 1, 25, 8, 0))

        article1 = ArticleFactory.create(
            url="http://www.news-site.nl/article1.html",
            last_check=update_time,
            last_update=update_time,
        )

        article1_version1 = VersionFactory.create(
            title="article1 revision1",
            article=article1,
            date=update_time - timedelta(hours=2),
        )

        article1_version2 = VersionFactory.create(
            title="article1 revision 2",
            article=article1,
            date=update_time - timedelta(hours=3),
        )

        article1_version3 = VersionFactory.create(
            title="article 1 revision 3",
            article=article1,
            date=update_time - timedelta(days=1, hours=3),
        )

        article2 = ArticleFactory.create(
            url="http://www.news-site.nl/article2.html",
            last_check=update_time,
            last_update=update_time,
        )

        article2_version1 = VersionFactory.create(
            title="article2 revision1",
            article=article2,
            date=update_time - timedelta(hours=3),
        )

        article2_version2 = VersionFactory.create(
            title="article2 revision1",
            article=article2,
            date=update_time - timedelta(hours=4),
        )

        response = self.app.get(reverse('browse'))
        rows = response.pyquery.find('table tbody tr')

        def assert_article_row(row, article, version1, version2):
            column1 = row.find('td').eq(0)

            article_link = column1.find('a').eq(0).attr('href')
            article_title = column1.find('a').eq(0).text()
            expected_article_link = reverse(
                'article_history', args=[article.filename(), ])
            self.assertEquals(article_link, expected_article_link)
            self.assertEquals(article_title, article.latest_version().title)

            column2 = row.find('td').eq(1)
            self.assertEquals(
                column2.text(),
                localize(localtime(article.latest_version().date))
            )

            self.assertEquals(version1, article.version_set.all()[0])
            self.assertEquals(version2, article.version_set.all()[1])

            column3 = row.find('td').eq(2)
            expected_diff_link = reverse(
                'diffview', kwargs={
                    'vid1': version2.pk,
                    'vid2': version1.pk,
                    'urlarg': article.filename()
                })
            diff_link = column3.find('a').attr('href')
            self.assertEquals(diff_link, expected_diff_link)

        def assert_version_row(row, version1, version2):
            column1 = row.find('td').eq(0)
            self.assertEquals(
                column1.text(),
                localize(localtime(version1.date))
            )

            if version2:
                column2 = row.find('td').eq(1)
                expected_diff_link = reverse(
                    'diffview', kwargs={
                        'vid1': version2.pk,
                        'vid2': version1.pk,
                        'urlarg': article1.filename()
                    })
                diff_link = column2.find('a').attr('href')

                self.assertEquals(expected_diff_link, diff_link)

        assert_article_row(
            rows.eq(0), article1, article1_version1, article1_version2)
        assert_version_row(
            rows.eq(1), article1_version2, article1_version3)
        assert_version_row(
            rows.eq(2), article1_version3, None)
        assert_article_row(
            rows.eq(3), article2, article2_version1, article2_version2)
        assert_version_row(
            rows.eq(4), article2_version2, None)
