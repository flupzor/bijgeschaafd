# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from ._migrate_dates import migrate_dates


def migrate_dates_nu_nl(apps, schema_editor):
    migrate_dates(apps, schema_editor, 'nu.nl')


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_migrate_dates_nos_nl'),
    ]

    operations = [
        migrations.RunPython(migrate_dates_nu_nl),
    ]
