# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def make_articles_boring(apps, schema_editor):
    Article = apps.get_model("news", "Article")

    for article in Article.objects.filter(url__contains='http://www.nu.nl/gadgets/'):
        for version in article.version_set.all():
            version.boring = True
            version.save()

    for article in Article.objects.filter(url__contains='http://www.telegraaf.nl/prive/'):
        for version in article.version_set.all():
            version.boring = True
            version.save()

    for article in Article.objects.filter(url__contains='http://www.telegraaf.nl/autovisie/'):
        for version in article.version_set.all():
            version.boring = True
            version.save()

    for article in Article.objects.filter(url__contains='http://www.telegraaf.nl/reiskrant/'):
        for version in article.version_set.all():
            version.boring = True
            version.save()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20160123_1510'),
    ]

    operations = [
    ]
