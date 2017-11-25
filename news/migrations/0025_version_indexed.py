# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0024_auto_20160612_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='indexed',
            field=models.BooleanField(default=False),
        ),
    ]
