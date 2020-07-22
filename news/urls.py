from django.conf.urls import url
from django.views.generic.base import RedirectView

from .views import about, browse, article_history, diffview, diffview2, json_view, RequestLogListView, SearchView, SimilarArticleListView

urlpatterns = [
  url(r'^diff/(?P<vid1>\d+)/(?P<vid2>\d+)/(?P<urlarg>.*)$', diffview, name='diffview'),
  url(r'^diff2/(?P<vid1>\d+)/(?P<vid2>\d+)/$', diffview2, name='diffview2'),
  url(r'^about/$', about, name='about'),
  url(r'^request-log/list/$', RequestLogListView.as_view(), name='requestlog_list'),
  url(r'^browse/$', browse, name='browse'),
  url(r'^browse/(?P<source>.*)$', browse, name='browse'),
  url(r'^similararticle/list/$', SimilarArticleListView.as_view(), name='similararticle_list'),
  url(r'^search/$', SearchView.as_view(), name='search'),
  url(r'^article-history/$', article_history, name='article_history'),
  url(r'^article-history/(?P<urlarg>.*)$', article_history, name='article_history'),
  url(r'^json/view/(?P<vid>\d+)/?$', json_view),
  url(r'^$', RedirectView.as_view(url='/browse/', permanent=False), name='root'),
]
