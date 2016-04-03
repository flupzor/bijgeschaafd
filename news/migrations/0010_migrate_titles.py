# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.models import F

def migrate_titles(apps, schema_editor):
    Version = apps.get_model("news", "Version")

    for version in Version.objects.filter(content__startswith=F('title')):
        version.content = version.content.replace(version.title, '').lstrip()
        version.save()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_migrate_dates'),
    ]

    operations = [
        migrations.RunPython(migrate_titles),
    ]
