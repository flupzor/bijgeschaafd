#!/usr/bin/python

import errno
import hashlib
import httplib
import logging
import os
import subprocess
import sys
import time
import traceback
import urllib2
from datetime import datetime
from optparse import make_option

from django.core.management.base import BaseCommand

from bijgeschaafd import diff_match_patch
import parsers
from news import models
from parsers.baseparser import canonicalize

logger = logging.getLogger('scraper')


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--update',
            action='store_true',
            default=False,
            help='DEPRECATED; this is the default'),
        make_option('--all',
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
        update_articles()
        update_versions(options['all'])

# Begin utility functions
def canonicalize_url(url):
    return url.split('?')[0].split('#')[0].strip()

def strip_prefix(string, prefix):
    if string.startswith(prefix):
        string = string[len(prefix):]
    return string

def url_to_filename(url):
    return strip_prefix(url, 'http://').rstrip('/')


class IndexLockError(OSError):
    pass

def get_all_article_urls():
    ans = set()
    for parser in parsers.parsers:
        logger.info('Looking up %s' % parser.domains)
        urls = parser.feed_urls()
        ans = ans.union(map(canonicalize_url, urls))
    return ans

CHARSET_LIST = """EUC-JP GB2312 EUC-KR Big5 SHIFT_JIS windows-1252
IBM855
IBM866
ISO-8859-2
ISO-8859-5
ISO-8859-7
KOI8-R
MacCyrillic
TIS-620
windows-1250
windows-1251
windows-1253
windows-1255""".split()
def is_boring(old, new):
    oldu = canonicalize(old.decode('utf8'))
    newu = canonicalize(new.decode('utf8'))

    def extra_canonical(s):
        """Ignore changes in whitespace or the date line"""
        nondate_portion = s.split('\n', 1)[1]
        return nondate_portion.split()

    if extra_canonical(oldu) == extra_canonical(newu):
        return True

    for charset in CHARSET_LIST:
        try:
            if oldu.encode(charset) == new:
                logger.debug('Boring!')
                return True
        except UnicodeEncodeError:
            pass
    return False

def get_diff_info(old, new):
    dmp = diff_match_patch.diff_match_patch()
    dmp.Diff_Timeout = 3 # seconds; default of 1 is too little
    diff = dmp.diff_main(old, new)
    dmp.diff_cleanupSemantic(diff)
    chars_added   = sum(len(text) for (sign, text) in diff if sign == 1)
    chars_removed = sum(len(text) for (sign, text) in diff if sign == -1)
    return dict(chars_added=chars_added, chars_removed=chars_removed)

def load_article(url):
    try:
        parser = parsers.get_parser(url)
    except KeyError:
        logger.info('Unable to parse domain, skipping')
        return
    try:
        parsed_article = parser(url)
    except (AttributeError, urllib2.HTTPError, httplib.HTTPException), e:
        if isinstance(e, urllib2.HTTPError) and e.msg == 'Gone':
            return
        logger.error('Exception when parsing %s', url)
        logger.error(traceback.format_exc())
        logger.error('Continuing')
        return
    if not parsed_article.real_article:
        return
    return parsed_article

#Update url in git
#Return whether it changed
def update_article(article):

    parsed_article = load_article(article.url)
    if parsed_article is None:
        return
    to_store = unicode(parsed_article).encode('utf-8')
    to_store_sha1 = hashlib.sha1(to_store).hexdigest()
    t = datetime.now()
    logger.debug('Article %s: boring %s', article.url, parsed_article.boring)

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

        if article.version_set.filter(content_sha1=to_store_sha1).count() >= 2:
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
    v_row.save()
    if not boring:
        article.last_update = t
        article.save()

def update_articles():
    logger.info('Starting scraper; looking for new URLs')
    all_urls = get_all_article_urls()
    logger.info('Got all %s urls; storing to database' % len(all_urls))
    for i, url in enumerate(all_urls):
        logger.debug('Woo: %d/%d is %s' % (i+1, len(all_urls), url))
        if len(url) > 255:  #Icky hack, but otherwise they're truncated in DB.
            continue
        if not models.Article.objects.filter(url=url).count():
            logger.debug('Adding!')
            models.Article(url=url).save()
    logger.info('Done storing to database')

def get_update_delay(minutes_since_update):
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
        return 60*24*365*1e5  #ignore old articles

def update_versions(do_all=False):
    logger.info('Looking for articles to check')
    articles = list(models.Article.objects.exclude())
    total_articles = len(articles)

    update_priority = lambda x: x.minutes_since_check() * 1. / get_update_delay(x.minutes_since_update())
    articles = sorted([a for a in articles if update_priority(a) > 1 or do_all],
                      key=update_priority, reverse=True)

    logger.info('Checking %s of %s articles', len(articles), total_articles)

    logger.info('Done!')
    for i, article in enumerate(articles):
        logger.debug('Woo: %s %s %s (%s/%s)',
                     article.minutes_since_update(),
                     article.minutes_since_check(),
                     update_priority(article), i+1, len(articles))
        delay = get_update_delay(article.minutes_since_update())
        if article.minutes_since_check() < delay and not do_all:
            continue
        logger.info('Considering %s', article.url)

        article.last_check = datetime.now()
        try:
            update_article(article)
        except Exception, e:
            if isinstance(e, subprocess.CalledProcessError):
                logger.error('CalledProcessError when updating %s', article.url)
                logger.error(repr(e.output))
            else:
                logger.error('Unknown exception when updating %s', article.url)

            logger.error(traceback.format_exc())
        article.save()
    logger.info('Done!')

if __name__ == '__main__':
    print >> sys.stderr, "Try `python bijgeschaafd/manage.py scraper`."
