# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from ._migrate_dates import migrate_dates


def migrate_dates_metro(apps, schema_editor):
    migrate_dates(apps, schema_editor, 'metronieuws.nl')


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_migrate_dates_telegraaf'),
    ]

    operations = [
        migrations.RunPython(migrate_dates_metro),
    ]
