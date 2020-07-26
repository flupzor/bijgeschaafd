# -*- coding: utf-8 -*-


from django.db import models, migrations

def delete_logs(apps, schema_editor):
    RequestLog = apps.get_model("news", "RequestLog")

    RequestLog.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_requestlog_version'),
    ]

    operations = [
        migrations.RunPython(delete_logs),
    ]
