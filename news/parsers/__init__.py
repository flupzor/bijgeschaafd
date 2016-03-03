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


logger = logging.getLogger('parsers')


_parsers = """
nosnl.NOSNLParser
nunl.NuNLParser
telegraaf.TelegraafParser
""".split()

parser_dict = {}

# Import the parsers and fill in parser_dict: domain -> parser
for parsername in _parsers:
    module, classname = parsername.rsplit('.', 1)
    parser = getattr(__import__(module, globals(), fromlist=[classname]), classname)
    for domain in parser.domains:
        parser_dict[domain] = parser

# Each feeder places URLs into the database to be checked periodically.
parsers = [p for p in parser_dict.values()]


def get_parser(url):
    return parser_dict[url.split('/')[2]]


def _canonicalize_url(url):
    return url.split('?')[0].split('#')[0].strip()


def get_all_article_urls():
    ans = set()
    for parser in parsers:
        urls = parser.feed_urls()
        ans = ans.union(map(_canonicalize_url, urls))
    return ans


def load_article(url):
    try:
        parser = get_parser(url)
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

__all__ = ['parsers', 'get_parser', 'get_all_article_urls', 'load_article']
