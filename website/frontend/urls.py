from django.conf.urls import url
from django.views.generic.base import RedirectView


urlpatterns = [
  url(r'^diff/(?P<vid1>\d+)/(?P<vid2>\d+)/(?P<urlarg>.*)$', 'website.frontend.views.diffview', name='diffview'),
  url(r'^about/$', 'website.frontend.views.about', name='about'),
  url(r'^browse/$', 'website.frontend.views.browse', name='browse'),
  url(r'^browse/(.*)$', 'website.frontend.views.browse', name='browse'),
  url(r'^article-history/$', 'website.frontend.views.article_history', name='article_history'),
  url(r'^article-history/(?P<urlarg>.*)$', 'website.frontend.views.article_history', name='article_history'),
  url(r'^json/view/(?P<vid>\d+)/?$', 'website.frontend.views.json_view'),
  url(r'^$', RedirectView.as_view(url='/browse/'), name='root'),
]
