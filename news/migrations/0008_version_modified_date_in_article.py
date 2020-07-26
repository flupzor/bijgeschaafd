# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20160320_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='modified_date_in_article',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
    ]
