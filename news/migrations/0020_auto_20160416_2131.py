# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


# Copied from: https://djangosnippets.org/snippets/1170/
def batch_qs(qs, batch_size=1000):
    """
    Returns a (start, end, total, queryset) tuple for each batch in the given
    queryset.

    Usage:
        # Make sure to order your querset
        article_qs = Article.objects.order_by('id')
        for start, end, total, qs in batch_qs(article_qs):
            print "Now processing %s - %s of %s" % (start + 1, end, total)
            for article in qs:
                print article.body
    """
    total = qs.count()
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        yield (start, end, total, qs[start:end])


def hash_djb2(s):
    hash = 5381
    for x in s:
        hash = ((hash << 5) + hash) + ord(x)
    return hash & 0xFFFFFFFF


def hash_content(content):
    return [hash_djb2(word) for word in content.split(' ')]


def hash_words(apps, schema_editor):
    Version = apps.get_model("news", "Version")

    versions = Version.objects.filter(content_words_hashed__isnull=True)
    for start, end, total, qs in batch_qs(versions):
        print "Now processing %s - %s of %s" % (start + 1, end, total)
        for version in qs:
            version.content_words_hashed = hash_content(version.content)
            version.save(update_fields=['content_words_hashed', ])


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0019_auto_20160416_2143'),
    ]

    operations = [
        migrations.RunPython(hash_words),
    ]
