from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import RequestLogListView


urlpatterns = [
  url(r'^diff/(?P<vid1>\d+)/(?P<vid2>\d+)/(?P<urlarg>.*)$', 'news.views.diffview', name='diffview'),
  url(r'^about/$', 'news.views.about', name='about'),
  url(r'^request-log/list/$', RequestLogListView.as_view(), name='requestlog_list'),
  url(r'^browse/$', 'news.views.browse', name='browse'),
  url(r'^browse/(.*)$', 'news.views.browse', name='browse'),
  url(r'^article-history/$', 'news.views.article_history', name='article_history'),
  url(r'^article-history/(?P<urlarg>.*)$', 'news.views.article_history', name='article_history'),
  url(r'^json/view/(?P<vid>\d+)/?$', 'news.views.json_view'),
  url(r'^$', RedirectView.as_view(url='/browse/', permanent=False), name='root'),
]
