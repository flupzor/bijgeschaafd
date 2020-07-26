# -*- coding: utf-8 -*-


from django.db import models, migrations

from ._migrate_dates import migrate_dates


def migrate_dates_telegraaf(apps, schema_editor):
    migrate_dates(apps, schema_editor, 'telegraaf.nl')


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_migrate_dates_nu_nl'),
    ]

    operations = [
        migrations.RunPython(migrate_dates_telegraaf),
    ]
