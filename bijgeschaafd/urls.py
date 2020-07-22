from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^', include('news.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^robots.txt$', RedirectView.as_view(url='/static/robots.txt', permanent=False)),
]
