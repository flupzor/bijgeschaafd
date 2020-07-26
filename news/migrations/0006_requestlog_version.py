# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20160312_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestlog',
            name='version',
            field=models.ForeignKey(to='news.Version', null=True, on_delete=models.CASCADE),
        ),
    ]
