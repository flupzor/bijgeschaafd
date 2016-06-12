import factory
import factory.fuzzy

from ..models import Article, Cluster, SimilarArticle, Version


class ArticleFactory(factory.django.DjangoModelFactory):
    url = factory.Faker('url')
    last_check = factory.Faker('date_time_between', start_date="-1y", end_date="now")
    last_update = factory.Faker('date_time_between', start_date="-1y", end_date="now")

    class Meta:
        model = Article


class VersionFactory(factory.django.DjangoModelFactory):
    article = factory.SubFactory(ArticleFactory)
    title = factory.LazyAttribute(lambda x: factory.Faker('sentence', nb_words=4))
    byline = ''
    date = factory.Faker('date_time_between', start_date="-1y", end_date="now")
    diff_json = '{}'

    class Meta:
        model = Version

class ClusterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cluster



class SimilarArticleFactory(factory.django.DjangoModelFactory):
    cluster = factory.SubFactory(ClusterFactory)
    from_article = factory.SubFactory(ArticleFactory)
    to_article = factory.SubFactory(ArticleFactory)

    ratio = factory.fuzzy.FuzzyDecimal(0.6, 1)

    class Meta:
        model = SimilarArticle
