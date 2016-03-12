import hashlib
import logging
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils import timezone

from news.models import Article, Version
from news.parsers import all_parsers, load_article
from news.utils import get_diff_info, is_boring

logger = logging.getLogger('scraper')


class Command(BaseCommand):
    help = "Scrape articles which need updating."

    option_list = BaseCommand.option_list + (
        make_option(
            '--all',
            action='store_true',
            default=False,
            help='Update _all_ stored articles'),
        )

    def handle(self, *args, **options):
        self.update_articles(options['all'])

    def get_update_delay(self, minutes_since_update):
        days_since_update = minutes_since_update // (24 * 60)
        if minutes_since_update < 60*3:
            return 15
        elif days_since_update < 1:
            return 60
        elif days_since_update < 7:
            return 180
        elif days_since_update < 30:
            return 60*24*3
        elif days_since_update < 360:
            return 60*24*30
        else:
            return 60*24*365*1e5   # ignore old articles

    def update_articles(self, do_all=False):

        # Based on the URLS found on all the front pages create the
        # corresponding articles.
        for parser in all_parsers():
            feed_urls = parser.feed_urls()
            for i, url in enumerate(feed_urls):
                # Icky hack, but otherwise they're truncated in DB.
                if len(url) > 255:
                    logger.error(
                        "Skipping article with URL %s because the URL is too "
                        "large to store", url)
                    continue
                Article.objects.get_or_create(url=url, defaults={
                    'source': parser.short_name
                })
            logger.info('Stored %s article urls for %s', len(feed_urls), parser.short_name)

        articles = list(Article.objects.all())
        total_articles = len(articles)

        update_priority = \
            lambda x: x.minutes_since_check() * 1. / self.get_update_delay(
                x.minutes_since_update())
        articles = sorted(
            [a for a in articles if update_priority(a) > 1 or do_all],
            key=update_priority, reverse=True)

        logger.info(
            "Checking %s of %s articles", len(articles), total_articles)

        for i, article in enumerate(articles):
            minutes_since_update = article.minutes_since_update()
            minutes_since_check = article.minutes_since_check()
            delay = self.get_update_delay(minutes_since_update)
            if minutes_since_check < delay and not do_all:
                continue
            logger.info(
                "Scraping %s last checked: %d minutes ago "
                "last updated: %d minutes ago", article.url,
                minutes_since_check, minutes_since_update)

            article.last_check = timezone.now()
            try:
                self.update_article(article)
            except Exception:
                logger.exception('Exception when updating %s', article.url)
            article.save()

    def update_article(self, article):

        parsed_article = load_article(article)
        if parsed_article is None:
            return
        to_store = unicode(parsed_article).encode('utf-8')
        to_store_sha1 = hashlib.sha1(to_store).hexdigest()
        current_time = timezone.now()

        boring = parsed_article.boring
        diff_info = None

        try:
            latest_version = article.version_set.latest()
        except Version.DoesNotExist:
            latest_version = None

        if latest_version:
            latest_version_content = latest_version.content.encode('utf-8')

            if latest_version_content == to_store:
                return

            if article.version_set.filter(
                    content_sha1=to_store_sha1).count() >= 2:
                return

            if is_boring(latest_version_content, to_store):
                boring = True
            else:
                diff_info = get_diff_info(latest_version_content, to_store)

        v_row = Version(
            boring=boring,
            title=parsed_article.title,
            byline=parsed_article.byline,
            date=current_time,
            article=article,
            content=to_store,
            content_sha1=to_store_sha1,
        )
        v_row.diff_info = diff_info
        if not boring:
            v_row.save()
            article.last_update = current_time
            article.save()
