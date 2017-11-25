from datetime import datetime, timedelta

from django.test import TestCase, override_settings
from django.utils import timezone

from news.tests.factory_models import ArticleFactory, VersionFactory

from .. import parsers


class ArticleTests(TestCase):
    def test_article_create(self):
        article = ArticleFactory.create()
        self.assertEquals(article._latest_date, None)
        self.assertEquals(article._sum_versions, 0)

    def test_version_create(self):
        tz = timezone.get_current_timezone()

        article = ArticleFactory.create()

        VersionFactory.create(
            article=article,
            date=tz.localize(datetime(2015, 1, 2)),
        )

        article = article.__class__.objects.get(pk=article.pk)

        self.assertEquals(
            article._latest_date, tz.localize(datetime(2015, 1, 2)))
        self.assertEquals(article._sum_versions, 1)

        VersionFactory.create(
            article=article,
            date=tz.localize(datetime(2015, 1, 1)),
        )

        self.assertEquals(
            article._latest_date, tz.localize(datetime(2015, 1, 2)))
        self.assertEquals(article._sum_versions, 2)

        VersionFactory.create(
            article=article,
            date=tz.localize(datetime(2016, 1, 1)),
        )

        self.assertEquals(
            article._latest_date, tz.localize(datetime(2016, 1, 1)))
        self.assertEquals(article._sum_versions, 3)

    @override_settings(NEWS_SOURCES=['news.parsers.mock.MockParser', ])
    def test_needs_update_equal(self):
        parsers.reset()

        current_time = timezone.now()

        last_check=current_time - timedelta(minutes=1)
        last_update=current_time - timedelta(minutes=1)

        article = ArticleFactory.create(
            source='mock.nl',
            last_check=last_check,
            last_update=last_update,
        )
        article.initial_date=current_time - timedelta(days=365)
        article.save()

        self.assertEquals(article.needs_update, False)

    def _needs_update(self, last_check, last_update_min, last_update_max):
        current_time = timezone.now()
        initial_date = current_time - last_update_max - timedelta(days=365)

        article = ArticleFactory.create(
            source='mock.nl',
            last_check=current_time - last_check,
            last_update=current_time - last_update_max,
        )
        article.initial_date=initial_date
        article.save()
        self.assertEquals(article.needs_update, True)

        article = ArticleFactory.create(
            source='mock.nl',
            last_check=current_time - last_check,
            last_update=current_time - last_update_min,
        )
        article.initial_date=initial_date
        article.save()
        self.assertEquals(article.needs_update, True)

        article = ArticleFactory.create(
            source='mock.nl',
            last_check=current_time - last_check + timedelta(minutes=1),
            last_update=current_time - last_update_max,
        )
        article.initial_date=initial_date
        article.save()
        self.assertEquals(article.needs_update, False)

        article = ArticleFactory.create(
            source='mock.nl',
            last_check=current_time - last_check + timedelta(minutes=1),
            last_update=current_time - last_update_min,
        )
        article.initial_date=initial_date
        article.save()
        self.assertEquals(article.needs_update, False)

    @override_settings(NEWS_SOURCES=['news.parsers.mock.MockParser', ])
    def test_needs_update(self):
        """
        from        to          delay
        0 hours     3 hours     15 minute
        3 hours     1 day        1 hour
        1 day       7 days       3 hour
        7 day       30 days      3 days
        30 days     360 days    30 days
        360 days    forever     do not download
        """
        parsers.reset()

        # Every 15 minutes
        self._needs_update(
            timedelta(minutes=15), timedelta(hours=1), timedelta(hours=2, minutes=59)
        )

        # Every hour
        self._needs_update(
            timedelta(hours=1), timedelta(hours=3), timedelta(hours=23, minutes=59)
        )

        # Every 3 hours
        self._needs_update(
            timedelta(hours=3), timedelta(days=1), timedelta(days=9, hours=23, minutes=59)
        )

        # Do not download
        current_time = timezone.now()
        initial_date = current_time - timedelta(days=10) - timedelta(days=365)

        article = ArticleFactory.create(
            source='mock.nl',
            last_check=current_time - timedelta(days=360),
            last_update=current_time - timedelta(days=360),
        )
        article.initial_date = initial_date
        article.save()
        self.assertEquals(article.needs_update, False)
