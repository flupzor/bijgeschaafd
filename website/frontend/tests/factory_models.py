import factory

from ..models import Article, Version, Upvote

class ArticleFactory(factory.django.DjangoModelFactory):
    url = factory.Faker('url')
    last_check = factory.Faker('date_time_between', start_date="-1y", end_date="now")
    last_update = factory.Faker('date_time_between', start_date="-1y", end_date="now")
    git_dir = factory.Faker('uri_path')

    class Meta:
        model = Article


class VersionFactory(factory.django.DjangoModelFactory):
    article = factory.SubFactory(ArticleFactory)
    # Git commit
    v = factory.Faker('sha1', raw_output=False)
    title = factory.LazyAttribute(lambda x: factory.Faker('sentence', nb_words=4))
    byline = ''
    date = factory.Faker('date_time_between', start_date="-1y", end_date="now")
    boring = factory.Faker('boolean', chance_of_getting_true=95)
    diff_json = '{}'

    class Meta:
        model = Version


class UpvoteFactory(factory.Factory):
    class Meta:
        model = Upvote
