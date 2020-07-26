# -*- coding: utf-8 -*-


from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0017_auto_20160407_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='content_words_hashed',
            field=django.contrib.postgres.fields.ArrayField(null=True, base_field=models.BigIntegerField(), size=None),
        ),
        migrations.AlterField(
            model_name='article',
            name='_sum_versions',
            field=models.IntegerField(default=0),
        ),
    ]
