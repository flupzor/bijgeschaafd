from django.conf.urls import url

urlpatterns = [
  # These are deprecated, and meant to preserve legacy URLs:
  url(r'^diffview/$', 'website.frontend.views.old_diffview'),
  url(r'^article-history/$', 'website.frontend.views.article_history', name='article_history'),

  # These are current:
  url(r'^upvote/$', 'website.frontend.views.upvote', name='upvote'),
  url(r'^diff/(?P<vid1>\d+)/(?P<vid2>\d+)/(?P<urlarg>.*)$', 'website.frontend.views.diffview', name='diffview'),
  url(r'^about/$', 'website.frontend.views.about', name='about'),
  url(r'^browse/$', 'website.frontend.views.browse', name='browse'),
  url(r'^browse/(.*)$', 'website.frontend.views.browse', name='browse'),
  url(r'^feed/browse/(.*)$', 'website.frontend.views.feed', name='feed'),
  url(r'^contact/$', 'website.frontend.views.contact', name='contact'),
  url(r'^examples/$', 'website.frontend.views.examples', name='examples'),
  url(r'^subscribe/$', 'website.frontend.views.subscribe', name='subscribe'),
  url(r'^press/$', 'website.frontend.views.press', name='press'),
  url(r'^feed/article-history/(.*)$', 'website.frontend.views.article_history_feed', name='article_history_feed'),
  url(r'^article-history/(?P<urlarg>.*)$', 'website.frontend.views.article_history', name='article_history'),
  url(r'^json/view/(?P<vid>\d+)/?$', 'website.frontend.views.json_view'),
  url(r'^$', 'website.frontend.views.front', name='root'),
]
