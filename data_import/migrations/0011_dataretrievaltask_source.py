# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-09 05:07
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_task_sources(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    DataRetrievalTask = apps.get_model('data_import', 'DataRetrievalTask')

    for task in DataRetrievalTask.objects.all():
        content_type = ContentType.objects.get(id=task.datafile_model_id)
        task.source = content_type.app_label
        task.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('data_import', '0010_migrate_datafiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataretrievaltask',
            name='source',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.RunPython(migrate_task_sources),
    ]