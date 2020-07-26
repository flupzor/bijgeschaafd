# -*- coding: utf-8 -*-


from django.db import models, migrations


def add_cache(apps, schema_editor):
    Article = apps.get_model("news", "Article")

    for article in Article.objects.all():
        version_count = article.version_set.count()
        if version_count == 0:
            article.delete()
            continue

        article._latest_date = \
            article.version_set.latest('date').date
        article._sum_versions = version_count
        article.save()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0016_auto_20160407_1442'),
    ]

    operations = [
        migrations.RunPython(add_cache),
    ]
