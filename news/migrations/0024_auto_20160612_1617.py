# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0023_auto_20160605_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='similararticle',
            name='cluster',
            field=models.ForeignKey(to='news.Cluster', on_delete=models.CASCADE),
        ),
    ]
