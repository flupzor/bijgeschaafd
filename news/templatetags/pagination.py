from urllib import urlencode

from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def build_url(url, base_qs, **extra):
    new_dict = base_qs.copy()
    new_dict.update(extra)
    querystring = urlencode(new_dict)
    return '{url}?{querystring}'.format(
        url=url, querystring=querystring
    )

@register.inclusion_tag('include/pagination.html', takes_context=True)
def pagination(context, page, url, base_qs=None):
    paginator = page.paginator
    current_page = page.number
    pages_each_side = 3

    if current_page <= pages_each_side + 1:
        pages = range(1, min(pages_each_side*2 + 1, paginator.num_pages) + 1)
    else:
        pages = range(current_page-pages_each_side, min(current_page + pages_each_side, paginator.num_pages) + 1)

    return {
        'paginator': paginator,
        'base_qs': base_qs or {},
        'page': page,
        'pages': pages,
        'url': url,
        'current_page': current_page
    }
