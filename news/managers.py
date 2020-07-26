from django.db import models, transaction
from django.db.models import Q


class ArticleQueryset(models.QuerySet):
    pass


class SimilarArticleQuerySet(models.QuerySet):
    # What i've implemented is a undirected weighted graph. Since the edges
    # are undirected the ordering of source and destination doesn't matter.
    # This means: SimilarArticle(from, to, weight) == SimilarArticle(to, from,
    # weight)

    # Which means we have to decide which of the two we want to store. I've
    # decided to store the the article with the lowest id as the source and
    # the article with the highest id as the destination.

    @transaction.atomic
    def add_similar_article(self, from_article, to_article, ratio):
        """
        :param Article from_article
        :param Article to_article
        :param integer ratio from 0.0 to 1.0
        :return SimilarArticle instance of SimilarArticle which connects from_article
                               to to_article
        """
        from .models import Article, Cluster

        _from_article = min(from_article, to_article, key=lambda a: a.id)
        _to_article = max(from_article, to_article, key=lambda a: a.id)


        if _from_article == _to_article:
            raise ValueError("It's not possible to create a similarity relation"
                             "to from and to the same Article. An Article is"
                             "always 100% similar to itself.")


        # Find a cluster for this similarity.
        similarities = self.model.objects.indirect_related(from_article, to_article)

        _latest_dates = [_from_article._latest_date, _to_article._latest_date]
        _latest_dates += list(Article.objects.filter(
            pk__in=similarities.article_pks()
        ).values_list('_latest_date', flat=True).order_by('-_latest_date')[:1])
        _latest_dates = [d for d in _latest_dates if d is not None]
        _latest_date = max(_latest_dates) if _latest_dates else None

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

            similarities.update(cluster=cluster)

            for unused_cluster in clusters[1:]:
                unused_cluster.delete()

        else:
            cluster.latest_date = _latest_date
            cluster.save()

        return self.model.objects.create(
            cluster=cluster,
            from_article=_from_article, to_article=_to_article,
            ratio=ratio)

    def article_pks(self):
        similarities = self.values_list('from_article__pk', 'to_article__pk')

        # flatten into a list
        flattened = [article_pk for similarity in similarities for article_pk in similarity]

        return list(set(flattened))

    def direct_related(self, *article_pks):
        """
        Find SimilarObject instances which have a direct relation to the given article.

        :param integer *article_pks
        :return Queryset
        """

        similarities = self.model.objects.filter(
            Q(from_article_id__in=article_pks) | Q(to_article_id__in=article_pks)
        )

        return similarities

    def indirect_related(self, *article_pks):
        """
        Find SimilarObject instances which have a direct or indirect relation to the given article.

        :param integer *article_pks
        :return Queryset
        """

        articles_found = set()
        similarities_found = set()
        look_for = article_pks

        # Keep looking until we've found all articles.
        while len(look_for):
            similarities = self.direct_related(*look_for)

            look_for = []
            for pk, from_article, to_article in similarities.values_list('pk', 'from_article_id', 'to_article_id'):
                if from_article not in articles_found:
                    look_for.append(from_article)
                    articles_found.add(from_article)

                if to_article not in articles_found:
                    look_for.append(to_article)
                    articles_found.add(to_article)

                similarities_found.add(pk)

        return self.model.objects.filter(pk__in=similarities_found)

class SimilarArticleManager(models.Manager.from_queryset(SimilarArticleQuerySet)):
    use_in_migrations = True
