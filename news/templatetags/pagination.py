from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('include/pagination.html', takes_context=True)
def pagination(context, page, label, *args):
    url = reverse(label, args=args)
    paginator = page.paginator
    current_page = page.number
    pages_each_side = 3

    if current_page <= pages_each_side + 1:
        pages = range(1, min(pages_each_side*2 + 1, paginator.num_pages) + 1)
    else:
        pages = range(current_page-pages_each_side, min(current_page + pages_each_side, paginator.num_pages) + 1)

    return {
        'paginator': paginator,
        'page': page,
        'pages': pages,
        'url': url,
        'current_page': current_page
    }
