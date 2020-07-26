# -*- coding: utf-8 -*-


from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_remove_version_boring'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='_latest_date',
            field=models.DateTimeField(default=None, null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='_sum_versions',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
