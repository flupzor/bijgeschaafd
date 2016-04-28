# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0020_auto_20160416_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimilarArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ratio', models.FloatField()),
                ('from_article', models.ForeignKey(related_name='from_article', to='news.Article')),
                ('to_article', models.ForeignKey(related_name='to_article', to='news.Article')),
            ],
        ),
    ]
