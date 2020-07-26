# -*- coding: utf-8 -*-


from django.db import models, migrations

def make_nu_nl_dvn_voetbal_boring(apps, schema_editor):
    Article = apps.get_model("news", "Article")

    for article in Article.objects.filter(url__contains='http://www.nu.nl/dvn/'):
        for version in article.version_set.all():
            version.boring = True
            version.save()

    for article in Article.objects.filter(url__contains='http://www.nu.nl/voetbal/'):
        for version in article.version_set.all():
            version.boring = True
            version.save()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20160102_1359'),
    ]

    operations = [
        migrations.RunPython(make_nu_nl_dvn_voetbal_boring),
    ]
