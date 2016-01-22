from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django_webtest import WebTest

from .factory_models import ArticleFactory, VersionFactory


class ViewTests(WebTest):
    def test_browse(self):
        """
        Test that the browse view is sorted properly.
        """

        update_time = datetime(2015, 1, 25, 8, 0)

        article1 = ArticleFactory.create(
            url="http://www.news-site.nl/article1.html",
            last_check=update_time,
            last_update=update_time,
        )

        article1_version1 = VersionFactory.create(
            title="article1 revision1",
            article=article1,
            boring=False,
            date=update_time - timedelta(hours=2),
        )

        article1_version2 = VersionFactory.create(
            title="article1 revision 2",
            article=article1,
            boring=False,
            date=update_time - timedelta(hours=3),
        )

        article1_version3 = VersionFactory.create(
            title="article 1 revision 3",
            article=article1,
            boring=False,
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
            boring=False,
            date=update_time - timedelta(hours=3),
        )

        article2_version2 = VersionFactory.create(
            title="article2 revision1",
            article=article2,
            boring=False,
            date=update_time - timedelta(hours=4),
        )

        response = self.app.get(reverse('browse'))
        rows = response.pyquery.find('table tbody tr')
        table_matrix = [
            {
                "column1": rows.eq(i).find('td').eq(0).html(),
                "column2": rows.eq(i).find('td').eq(1).html(),
                "column3": rows.eq(i).find('td').eq(2).html()
            } for i in range(len(rows))
        ]

        expected = [{
            'column1': '<a href="{}">article1 revision1</a> '
                       '(<a href="{}">None</a>)<br/>'.format(
                           reverse(
                               'article_history',
                               args=[article1.filename(), ]
                           ),
                           article1.url
                       ),
            'column2': '25 januari 2015 06:00',
            'column3': '<a href="{}">(Vergelijk)</a>'.format(
                reverse(
                    'diffview',
                    kwargs={
                        'vid1': article1_version2.pk,
                        'vid2': article1_version1.pk,
                        'urlarg': article1.filename()
                    }
                )),
        }, {
            'column1': '25 januari 2015 05:00',
            'column2': '<a href="{}">(Vergelijk)</a>'.format(
                reverse(
                    'diffview',
                    kwargs={
                        'vid1': article1_version3.pk,
                        'vid2': article1_version2.pk,
                        'urlarg': article1.filename()
                    }
                )),
            'column3': None,
        }, {
            'column1': '24 januari 2015 05:00',
            'column2': None,
            'column3': None,
        }, {
            'column1': '<a href="{}">article2 revision1</a> '
                       '(<a href="{}">None</a>)<br/>'.format(
                           reverse(
                               'article_history',
                               args=[article2.filename(), ]
                           ),
                           article2.url
                       ),
            'column2': '25 januari 2015 05:00',
            'column3': '<a href="{}">(Vergelijk)</a>'.format(
                reverse(
                    'diffview',
                    kwargs={
                        'vid1': article2_version2.pk,
                        'vid2': article2_version1.pk,
                        'urlarg': article2.filename()
                    }
                )),
        }, {
            'column1': '25 januari 2015 04:00',
            'column2': None,
            'column3': None,
        }]

        self.assertEquals(table_matrix, expected)
