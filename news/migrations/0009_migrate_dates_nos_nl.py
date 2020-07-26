# -*- coding: utf-8 -*-


from django.db import models, migrations

from ._migrate_dates import migrate_dates


def migrate_dates_nos_nl(apps, schema_editor):
    migrate_dates(apps, schema_editor, 'nos.nl')


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_version_modified_date_in_article'),
    ]

    operations = [
        migrations.RunPython(migrate_dates_nos_nl),
    ]
