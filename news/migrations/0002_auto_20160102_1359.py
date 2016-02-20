# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Upvote',
        ),
        migrations.AlterModelOptions(
            name='version',
            options={'ordering': ['-date'], 'get_latest_by': 'date'},
        ),
    ]
