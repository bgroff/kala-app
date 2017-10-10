# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-08 21:23
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def add_uuid(apps, schema_editor):
    Document = apps.get_model('documents', 'Document')
    for row in Document.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_document_uuid'),
    ]

    operations = [
        migrations.RunPython(add_uuid),
        migrations.AlterField(
            model_name='document',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
