import factory

from ..models import Article, Version


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
