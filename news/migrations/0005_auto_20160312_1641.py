# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import news.models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20160301_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('source', models.CharField(max_length=255, db_index=True)),
                ('url', models.CharField(max_length=255, db_index=True)),
                ('server_address', models.CharField(max_length=255, db_index=True)),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='last_check',
            field=models.DateTimeField(default=news.models.ancient),
        ),
        migrations.AlterField(
            model_name='article',
            name='last_update',
            field=models.DateTimeField(default=news.models.ancient),
        ),
    ]
