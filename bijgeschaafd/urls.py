import os

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(THIS_DIR)

urlpatterns = [
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': ROOT_DIR+'/bijgeschaafd/static',
        }, name='static'),
    url(r'^robots.txt$', RedirectView.as_view(url='/static/robots.txt', permanent=False)),
    url(r'^', include('news.urls')),
]
