import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from ..models import Article, Cluster, SimilarArticle, Version
from django.utils import timezone


class ArticleFactory(DjangoModelFactory):
    url = factory.Faker('url')
    last_check = factory.Faker('date_time_between', start_date="-1y", end_date="now", tzinfo=timezone.get_current_timezone())
    last_update = factory.Faker('date_time_between', start_date="-1y", end_date="now", tzinfo=timezone.get_current_timezone())

    class Meta:
        model = Article


class VersionFactory(DjangoModelFactory):
    article = factory.SubFactory(ArticleFactory)
    title = factory.LazyAttribute(lambda x: factory.Faker('sentence', nb_words=4))
    byline = ''
    date = factory.Faker('date_time_between', start_date="-1y", end_date="now", tzinfo=timezone.get_current_timezone())
    diff_json = '{}'

    class Meta:
        model = Version

class ClusterFactory(DjangoModelFactory):
    class Meta:
        model = Cluster



class SimilarArticleFactory(DjangoModelFactory):
    cluster = factory.SubFactory(ClusterFactory)
    from_article = factory.SubFactory(ArticleFactory)
    to_article = factory.SubFactory(ArticleFactory)

    ratio = factory.fuzzy.FuzzyDecimal(0.6, 1)

    class Meta:
        model = SimilarArticle
