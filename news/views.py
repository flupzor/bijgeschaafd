from datetime import datetime
import json

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Count, Max
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import Context, RequestContext, loader
from django.utils import timezone
from django.views.decorators.cache import cache_page

import models
from models import Article, Version
from .parsers import all_parsers

SEARCH_ENGINES = """
http://www.ask.com
http://www.google
https://www.google
search.yahoo.com
http://www.bing.com
""".split()


def came_from_search_engine(request):
    return any(x in request.META.get('HTTP_REFERER', '')
               for x in SEARCH_ENGINES)


def Http400():
    t = loader.get_template('404.html')
    return HttpResponse(t.render(Context()), status=400)


def get_first_update(source):
    if source is None:
        source = ''
    updates = models.Article.objects.order_by('last_update').filter(
        last_update__gt=datetime(1990, 1, 1, 0, 0, tzinfo=timezone.get_current_timezone()),
        url__contains=source
    )
    try:
        return updates[0].last_update
    except IndexError:
        return timezone.now()


def get_last_update(source):
    if source is None:
        source = ''
    updates = models.Article.objects.order_by('-last_update').filter(
        last_update__gt=datetime(1990, 1, 1, 0, 0, tzinfo=timezone.get_current_timezone()),
        url__contains=source
    )
    try:
        return updates[0].last_update
    except IndexError:
        return timezone.now()


def is_valid_source(source):
    valid_sources = [parser.short_name for parser in all_parsers()]

    return any(source.endswith(valid_source) for valid_source in valid_sources)


@cache_page(60 * 30)  #30 minute cache
def browse(request, source=''):
    if not (source == '' or is_valid_source(source)):
        raise Http404

    first_update = get_first_update(source)
    articles = Article.objects.filter(version__boring=False)

    if source:
        articles = articles.filter(source=source)

    articles = articles.annotate(
        version_count=Count('version'), age=Max('version__date')
    ).filter(
        version_count__gte=2,
    ).order_by('-age')

    paginator = Paginator(articles, 10)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render_to_response('browse.html', {
        'source': source, 'articles': articles,
        'page': page,
        'first_update': first_update,
        'sources': [parser.short_name for parser in all_parsers()]
    })


def diffview(request, vid1, vid2, urlarg):
    # urlarg is unused, and only for readability
    # Could be strict and enforce urlarg == article.filename()
    try:
        v1 = Version.objects.get(id=int(vid1))
        v2 = Version.objects.get(id=int(vid2))
    except Version.DoesNotExist:
        raise Http404

    article = v1.article

    if v1.article != v2.article:
        raise Http404

    title = article.latest_version().title

    versions = dict(enumerate(article.versions()))

    adjacent_versions = []
    dates = []
    texts = []

    for v in (v1, v2):
        texts.append(v.text())
        dates.append(v.date)

        indices = [i for i, x in versions.items() if x == v]
        if not indices:
            # One of these versions doesn't exist / is boring
            return Http400()
        index = indices[0]
        adjacent_versions.append([versions.get(index+offset)
                                  for offset in (-1, 1)])

    if any(x is None for x in texts):
        return Http400()

    links = []
    for i in range(2):
        if all(x[i] for x in adjacent_versions):
            diffl = reverse('diffview', kwargs=dict(vid1=adjacent_versions[0][i].id,
                                                    vid2=adjacent_versions[1][i].id,
                                                    urlarg=article.filename()))
            links.append(diffl)
        else:
            links.append('')

    return render_to_response('diffview.html', {
            'title': title,
            'date1': dates[0], 'date2': dates[1],
            'text1': texts[0], 'text2': texts[1],
            'prev': links[0], 'next': links[1],
            'article_shorturl': article.filename(),
            'article_url': article.url, 'v1': v1, 'v2': v2,
            'display_search_banner': came_from_search_engine(request),
            })


def get_rowinfo(article, version_lst=None):
    if version_lst is None:
        version_lst = article.versions()
    rowinfo = []
    lastv = None
    urlarg = article.filename()

    for version in version_lst:
        if lastv is None:
            diffl = ''
        else:
            diffl = reverse('diffview', kwargs=dict(vid1=lastv.id,
                                                    vid2=version.id,
                                                    urlarg=urlarg))
        rowinfo.append((diffl, version))
        lastv = version

    rowinfo.reverse()

    return rowinfo


def prepend_http(url):
    """Return a version of the url that starts with the proper scheme.

    url may look like

    www.nytimes.com
    https:/www.nytimes.com    <- because double slashes get stripped
    http://www.nytimes.com
    """
    components = url.split('/', 2)
    if len(components) <= 2 or '.' in components[0]:
        components = ['http:', '']+components
    elif components[1]:
        components[1:1] = ['']
    return '/'.join(components)


def article_history(request, urlarg=''):
    url = request.GET.get('url') # this is the deprecated interface.
    if url is None:
        url = urlarg
    if len(url) == 0:
        return HttpResponseRedirect(reverse(about))

    url = url.split('?')[0]  #For if user copy-pastes from news site

    url = prepend_http(url)

    # This is a hack to deal with unicode passed in the URL.
    # Otherwise gives an error, since our table character set is latin1.
    url = url.encode('ascii', 'ignore')

    # Give an error on urls with the wrong hostname without hitting the
    # database.  These queries are usually spam.
    source = url.split('/')[2]
    if not is_valid_source(source):
        return render_to_response('article_history_missing.html', {'url': url})

    try:
        article = Article.objects.get(url=url)
    except Article.DoesNotExist:
        try:
            return render_to_response('article_history_missing.html', {'url': url})
        except (TypeError, ValueError):
            # bug in django + mod_rewrite can cause this. =/
            return HttpResponse('Bug!')

    if len(urlarg) == 0:
        return HttpResponseRedirect(reverse(article_history, args=[article.filename()]))

    rowinfo = get_rowinfo(article)
    return render_to_response('article_history.html', {'article': article,
                                                       'versions': rowinfo,
            'display_search_banner': came_from_search_engine(request),

                                                       })

def json_view(request, vid):
    version = get_object_or_404(Version, id=int(vid))
    data = dict(
        title=version.title,
        byline=version.byline,
        date=version.date.isoformat(),
        text=version.text(),
        )
    return HttpResponse(json.dumps(data), mimetype="application/json")


def about(request):
    return render_to_response('about.html', {})


