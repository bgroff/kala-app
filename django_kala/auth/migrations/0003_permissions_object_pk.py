# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-08 20:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kala_auth', '0002_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='permissions',
            name='object_pk',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
