from datetime import timedelta
from django.test import TestCase, override_settings
from django.utils import timezone

from news.tests.factory_models import ArticleFactory, VersionFactory



class ArticleTests(TestCase):
    @override_settings(NEWS_SOURCES=['news.parsers.mock.MockParser', ])
    def test_needs_update_equal(self):
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
            timedelta(hours=3), timedelta(days=1), timedelta(days=6, hours=23, minutes=59)
        )

        # Every 3 days
        self._needs_update(
            timedelta(days=3), timedelta(days=7), timedelta(days=29, hours=23, minutes=59)
        )

        # Every 30 days
        self._needs_update(
            timedelta(days=30), timedelta(days=30), timedelta(days=359, hours=23, minutes=59)
        )

        # Do not download
        current_time = timezone.now()
        initial_date = current_time - timedelta(days=360) - timedelta(days=365)

        article = ArticleFactory.create(
            source='mock.nl',
            last_check=current_time - timedelta(days=360),
            last_update=current_time - timedelta(days=360),
        )
        article.initial_date=initial_date
        article.save()
        self.assertEquals(article.needs_update, False)

