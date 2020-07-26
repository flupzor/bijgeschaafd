# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0014_auto_20160407_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='boring',
        ),
    ]
