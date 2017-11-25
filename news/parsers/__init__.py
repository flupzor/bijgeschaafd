#!/usr/bin/python

# To start tracking a new site:
#  - create a parser class in another file, based off (say) bbc.BBCParser
#  - add it to parsers (below)
# Test with test_parser.py

# List of parsers to import and use based on parser.domains
import httplib
import logging
import traceback
import urllib2

from django.conf import settings

from .exceptions import ParserDoesNotExist

logger = logging.getLogger('parsers')

__parsers = None


def __init_cache():
    global __parsers
    __parsers = {}
    for news_source in settings.NEWS_SOURCES:
        module, classname = news_source.rsplit('.', 1)
        parser = getattr(__import__(module, globals(), fromlist=[classname]), classname)

        __parsers[parser.short_name] = parser


def reset():
    __init_cache()


def get_parser(source):
    if __parsers is None:
        __init_cache()

    parser = __parsers.get(source)

    if not parser:
        raise ParserDoesNotExist("Parser with short_name \"{}\" could not be found".format(source))

    return parser


def all_parsers():
    if __parsers is None:
        __init_cache()

    return __parsers.values()

def load_article(article):
    try:
        parser = get_parser(article.source)
    except KeyError:
        logger.info('Unable to parse domain, skipping')
        return
    try:
        parsed_article = parser(article.url)
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

__all__ = ['parsers', 'get_parser', 'get_all_article_urls', 'load_article', 'reset']
