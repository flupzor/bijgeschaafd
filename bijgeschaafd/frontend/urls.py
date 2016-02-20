from django.conf.urls import url
from django.views.generic.base import RedirectView


urlpatterns = [
  url(r'^diff/(?P<vid1>\d+)/(?P<vid2>\d+)/(?P<urlarg>.*)$', 'bijgeschaafd.frontend.views.diffview', name='diffview'),
  url(r'^about/$', 'bijgeschaafd.frontend.views.about', name='about'),
  url(r'^browse/$', 'bijgeschaafd.frontend.views.browse', name='browse'),
  url(r'^browse/(.*)$', 'bijgeschaafd.frontend.views.browse', name='browse'),
  url(r'^article-history/$', 'bijgeschaafd.frontend.views.article_history', name='article_history'),
  url(r'^article-history/(?P<urlarg>.*)$', 'bijgeschaafd.frontend.views.article_history', name='article_history'),
  url(r'^json/view/(?P<vid>\d+)/?$', 'bijgeschaafd.frontend.views.json_view'),
  url(r'^$', RedirectView.as_view(url='/browse/'), name='root'),
]
