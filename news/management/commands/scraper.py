#!/usr/bin/python

import hashlib
import logging
import subprocess
import traceback
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils import timezone

from news import models
from news.parsers import get_all_article_urls, load_article
from news.utils import get_diff_info, is_boring

logger = logging.getLogger('scraper')


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--all',
            action='store_true',
            default=False,
            help='Update _all_ stored articles'),
        )

    help = '''Scrape websites.

By default, scan front pages for new articles, and scan
existing and new articles to archive their current contents.

Articles that haven't changed in a while are skipped if we've
scanned them recently, unless --all is passed.
'''.strip()

    def handle(self, *args, **options):
        self.update_articles()
        self.update_versions(options['all'])

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

    def update_articles(self):
        logger.info('Starting scraper; looking for new URLs')
        all_urls = get_all_article_urls()
        logger.info('Got all %s urls; storing to database' % len(all_urls))
        for i, url in enumerate(all_urls):
            logger.debug('Woo: %d/%d is %s' % (i+1, len(all_urls), url))
            # Icky hack, but otherwise they're truncated in DB.
            if len(url) > 255:
                continue
            if not models.Article.objects.filter(url=url).count():
                logger.debug('Adding!')
                models.Article(url=url).save()
        logger.info('Done storing to database')

    def update_versions(self, do_all=False):
        logger.info('Looking for articles to check')
        articles = list(models.Article.objects.exclude())
        total_articles = len(articles)

        update_priority = \
            lambda x: x.minutes_since_check() * 1. / self.get_update_delay(
                x.minutes_since_update())
        articles = sorted(
            [a for a in articles if update_priority(a) > 1 or do_all],
            key=update_priority, reverse=True)

        logger.info(
            'Checking %s of %s articles', len(articles), total_articles)

        logger.info('Done!')
        for i, article in enumerate(articles):
            logger.debug('Woo: %s %s %s (%s/%s)',
                         article.minutes_since_update(),
                         article.minutes_since_check(),
                         update_priority(article), i+1, len(articles))
            delay = self.get_update_delay(article.minutes_since_update())
            if article.minutes_since_check() < delay and not do_all:
                continue
            logger.info('Considering %s', article.url)

            article.last_check = timezone.now()
            try:
                self.update_article(article)
            except Exception, e:
                if isinstance(e, subprocess.CalledProcessError):
                    logger.error(
                        'CalledProcessError when updating %s', article.url)
                    logger.error(repr(e.output))
                else:
                    logger.error(
                        'Unknown exception when updating %s', article.url)

                logger.error(traceback.format_exc())
            article.save()
        logger.info('Done!')

    def update_article(self, article):

        parsed_article = load_article(article.url)
        if parsed_article is None:
            return
        to_store = unicode(parsed_article).encode('utf-8')
        to_store_sha1 = hashlib.sha1(to_store).hexdigest()
        t = timezone.now()
        logger.debug(
            'Article %s: boring %s', article.url, parsed_article.boring)

        boring = parsed_article.boring
        diff_info = None

        try:
            latest_version = article.version_set.latest()
        except models.Version.DoesNotExist:
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

        v_row = models.Version(
            boring=boring,
            title=parsed_article.title,
            byline=parsed_article.byline,
            date=t,
            article=article,
            content=to_store,
            content_sha1=to_store_sha1,
        )
        v_row.diff_info = diff_info
        if not boring:
            v_row.save()
            article.last_update = t
            article.save()
