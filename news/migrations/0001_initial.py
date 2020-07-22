# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(unique=True, max_length=255, db_index=True)),
                ('initial_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField()),
                ('last_check', models.DateTimeField()),
                ('source', models.CharField(max_length=255, db_index=True)),
            ],
            options={
                'db_table': 'Articles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Upvote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article_id', models.IntegerField()),
                ('diff_v1', models.CharField(max_length=255)),
                ('diff_v2', models.CharField(max_length=255)),
                ('creation_time', models.DateTimeField()),
                ('upvoter_ip', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'upvotes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('byline', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('boring', models.BooleanField(default=False)),
                ('diff_json', models.CharField(max_length=255, null=True)),
                ('content_sha1', models.CharField(max_length=40, null=True, db_index=True)),
                ('content', models.TextField(default=b'')),
                ('article', models.ForeignKey(to='news.Article', on_delete=models.CASCADE)),
            ],
            options={
                'db_table': 'version',
                'get_latest_by': 'date',
            },
            bases=(models.Model,),
        ),
    ]
