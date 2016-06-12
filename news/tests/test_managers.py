from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError

from news.tests.factory_models import ArticleFactory, SimilarArticleFactory, VersionFactory

from ..models import Cluster, SimilarArticle

class SimilarArticleManagerTests(TestCase):
    def test_direct_related(self):
        article1, article2 = ArticleFactory.create_batch(2)
        SimilarArticleFactory.create(from_article=article1, to_article=article2)

        # Article 3 is not _directly_ related to article1
        article3 = ArticleFactory.create()
        SimilarArticleFactory.create(from_article=article2, to_article=article3)

        # Article 4 and 5 are not related at all to article1
        article4, article5 = ArticleFactory.create_batch(2)
        SimilarArticleFactory.create(from_article=article4, to_article=article5)

        similarities = SimilarArticle.objects.direct_related(article1.pk)
        article_pks = similarities.article_pks()

        self.assertEquals(len(article_pks), 2)
        self.assertIn(article1.pk, article_pks)
        self.assertIn(article2.pk, article_pks)

    def test_indirect_related(self):
        article1, article2 = ArticleFactory.create_batch(2)
        SimilarArticleFactory.create(from_article=article1, to_article=article2)

        # Article 3 is indirectly related to article1
        article3 = ArticleFactory.create()
        SimilarArticleFactory.create(from_article=article2, to_article=article3)

        # Article 4 and 5 are not related at all to article1
        article4, article5 = ArticleFactory.create_batch(2)
        SimilarArticleFactory.create(from_article=article4, to_article=article5)

        # Cycle
        article6, article7 = ArticleFactory.create_batch(2)
        SimilarArticleFactory.create(from_article=article1, to_article=article6)
        SimilarArticleFactory.create(from_article=article6, to_article=article7)
        SimilarArticleFactory.create(from_article=article7, to_article=article1)

        similarities = SimilarArticle.objects.indirect_related(article1.pk)
        article_pks = similarities.article_pks()

        self.assertEquals(len(article_pks), 5)
        self.assertIn(article1.pk, article_pks)
        self.assertIn(article2.pk, article_pks)
        self.assertIn(article3.pk, article_pks)
        self.assertIn(article6.pk, article_pks)
        self.assertIn(article7.pk, article_pks)

    def test_add_similar_article(self):

        # these articles should be ignored.
        current_time = timezone.now()
        irrelevant_article1, irrelevant_article2 = ArticleFactory.create_batch(2)
        irrelevant_article1._latest_date = current_time - timedelta(hours=1)
        irrelevant_article1.save()
        irrelevant_article2._latest_date = current_time - timedelta(hours=1)
        irrelevant_article2.save()

        self.assertEquals(Cluster.objects.count(), 0)
        self.assertEquals(SimilarArticle.objects.count(), 0)

        SimilarArticle.objects.add_similar_article(irrelevant_article1, irrelevant_article2, 0.8)

        self.assertEquals(Cluster.objects.count(), 1)
        self.assertEquals(SimilarArticle.objects.count(), 1)

        irrelevant_cluster = Cluster.objects.get()

        current_time = timezone.now()
        article1, article2, article3 = ArticleFactory.create_batch(3)
        article1._latest_date = current_time - timedelta(hours=1)
        article1.save()
        article2._latest_date = current_time - timedelta(hours=2)
        article2.save()
        article3._latest_date = current_time
        article3.save()

        self.assertEquals(Cluster.objects.count(), 1)
        self.assertEquals(SimilarArticle.objects.count(), 1)

        SimilarArticle.objects.add_similar_article(article2, article3, 0.8)

        self.assertEquals(Cluster.objects.count(), 2)
        self.assertEquals(SimilarArticle.objects.count(), 2)

        SimilarArticle.objects.add_similar_article(article1, article2, 0.8)

        self.assertEquals(Cluster.objects.count(), 2)
        self.assertEquals(SimilarArticle.objects.count(), 3)

        c = Cluster.objects.exclude(pk=irrelevant_cluster.pk).get()
        # The latest latest_date should be given to the cluster.
        self.assertEquals(c.latest_date, article3._latest_date)

    def test_add_similar_article_existing(self):
        """
        It should not be possible to have two similarities between two articles articles.
        """
        article1, article2 = ArticleFactory.create_batch(2)
        SimilarArticle.objects.add_similar_article(article2, article1, 0.8)
        with self.assertRaises(IntegrityError) as context:
            SimilarArticle.objects.add_similar_article(article1, article2, 0.8)

        self.assertIn(
            'duplicate key value violates unique constraint', context.exception.message)

        self.assertEquals(SimilarArticle.objects.count(), 1)
