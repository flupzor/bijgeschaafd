# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def delete_boring(apps, schema_editor):
    Version = apps.get_model("news", "Version")

    Version.objects.filter(boring=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_migrate_titles'),
    ]

    operations = [
        migrations.RunPython(delete_boring),
    ]
