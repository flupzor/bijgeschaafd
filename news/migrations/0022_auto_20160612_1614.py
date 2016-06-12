# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import news.managers


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0021_similararticle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latest_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.AlterModelManagers(
            name='similararticle',
            managers=[
                (b'objects', news.managers.SimilarArticleManager()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='similararticle',
            unique_together=set([('from_article', 'to_article')]),
        ),
        migrations.AddField(
            model_name='similararticle',
            name='cluster',
            field=models.ForeignKey(to='news.Cluster', null=True),
        ),
    ]
