# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-12-08 14:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_pruduct'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pruduct',
            new_name='Product',
        ),
    ]
