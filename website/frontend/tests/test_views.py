from datetime import datetime, timedelta
from unittest import skip

from django.test import TestCase

from ..models import Article, Version
from ..views import get_articles
from .factory_models import ArticleFactory, VersionFactory


class ViewTests(TestCase):
    def test_get_articles(self):
        """
        Retrieve the articles and versions which should
        be shown on the browse page on page 1.

        This means to request the articles from one
        day ago untill now.
        """

        update_time = datetime.now() - timedelta(hours=4)

        created_article = ArticleFactory.create(
            last_check=update_time,
            last_update=update_time,
        )

        created_version1 = VersionFactory.create(
            article=created_article,
            boring=False,
            date=datetime.now() - timedelta(hours=2),
        )

        created_version2 = VersionFactory.create(
            article=created_article,
            boring=False,
            date=datetime.now() - timedelta(hours=3),
        )

        # Outside the requested timeframe, but should still
        # be returned in the query.
        created_version3 = VersionFactory.create(
            article=created_article,
            boring=False,
            date=datetime.now() - timedelta(days=1, hours=3),
        )

        article_list = get_articles()

        self.assertEquals(len(article_list), 1)

        article, version, rowinfo = article_list[0]

        self.assertEquals(version.pk, created_version1.pk)

        self.assertEquals(len(rowinfo), 3)

        diff1, version1 = rowinfo[0]
        diff2, version2 = rowinfo[1]
        diff3, version3 = rowinfo[2]

        self.assertEquals(version1.pk, created_version1.pk)
        self.assertEquals(version2.pk, created_version2.pk)
        self.assertEquals(version3.pk, created_version3.pk)

    def test_get_articles_boring(self):
        """
        Make sure that if two versions exists for a article, but
        one is boring, the articles shouldn't be returned.
        """

        update_time = datetime.now() - timedelta(hours=4)

        created_article = ArticleFactory.create(
            last_check=update_time,
            last_update=update_time,
        )

        # Two versions exists, but one is boring,
        # so it should be ignored.
        created_version1 = VersionFactory.create(
            article=created_article,
            boring=False,
            date=datetime.now() - timedelta(hours=2),
        )

        created_version2 = VersionFactory.create(
            article=created_article,
            boring=True,
            date=datetime.now() - timedelta(hours=3),
        )

        article_list = get_articles()

        self.assertEquals(len(article_list), 0)

    def test_get_articles_before_date_window(self):
        """
        Make sure that if all the versions are outside
        of the requested date window, no articles are returned.
        """

        update_time = datetime.now() - timedelta(hours=4)

        created_article = ArticleFactory.create(
            last_check=update_time,
            last_update=update_time,
        )


        # Two versions exists, but one is boring,
        # so it should be ignored.
        created_version1 = VersionFactory.create(
            article=created_article,
            boring=False,
            date=datetime.now() - timedelta(days=1, hours=1),
        )

        created_version2 = VersionFactory.create(
            article=created_article,
            boring=False,
            date=datetime.now() - timedelta(days=1),
        )

        article_list = get_articles()

        self.assertEquals(len(article_list), 0)

    def test_get_articles_partially_after_date_window(self):
        """
        Request the yesterday's articles, while there are two version
        which where created yesterday, but one version which was
        created today. Since the latest date is leading, this article
        should not show on yesterday's page.
        """

        update_time = datetime.now() - timedelta(hours=4)

        created_article = ArticleFactory.create(
            last_check=update_time,
            last_update=update_time,
        )

        created_version1 = VersionFactory.create(
            article=created_article,
            boring=False,
            date=datetime.now() - timedelta(hours=2),
        )

        created_version2 = VersionFactory.create(
            article=created_article,
            boring=False,
            date=datetime.now() - timedelta(days=1, hours=3),
        )

        created_version3 = VersionFactory.create(
            article=created_article,
            boring=False,
            date=datetime.now() - timedelta(days=1, hours=4),
        )

        # request yesterday
        article_list = get_articles(distance=1)

        self.assertEquals(len(article_list), 0)
