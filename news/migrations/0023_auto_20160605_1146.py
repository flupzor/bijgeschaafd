# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def make_clusters(apps, schema_editor):
    Article = apps.get_model("news", "Article")
    Cluster = apps.get_model("news", "Cluster")
    SimilarArticle = apps.get_model("news", "SimilarArticle")

    assert SimilarArticle.objects.filter(cluster__isnull=False).count() == 0, "Expected no attached clusters."

    article_pks = SimilarArticle.objects.article_pks()

    while len(article_pks) > 0:
        article_pk = article_pks.pop()

        # Find a cluster for this similarity.
        similarities = SimilarArticle.objects.indirect_related(article_pk)

        _latest_dates = list(Article.objects.filter(
            pk__in=similarities.article_pks() + [article_pk, ]
        ).values_list('_latest_date', flat=True).order_by('-_latest_date')[:1])
        _latest_date = max(_latest_dates)

        clusters = list(similarities.values_list('cluster', flat=True).distinct())
        try:
            cluster = Cluster.objects.get(pk__in=clusters)
        except Cluster.DoesNotExist:
            cluster = Cluster.objects.create(latest_date=_latest_date)
        except Cluster.MultipleObjectsReturned as e:
            # Merge
            cluster = Cluster.objects.filter(pk=clusters[0]).get()
            cluster.latest_date=_latest_date
            cluster.save()

            for unused_cluster in clusters[1:]:
                unused_cluster.delete()

        else:
            cluster.latest_date = _latest_date
            cluster.save()

        similarities.update(cluster=cluster)


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0022_auto_20160612_1614'),
    ]

    operations = [
        migrations.RunPython(make_clusters),
    ]
