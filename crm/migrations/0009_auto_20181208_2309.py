# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-12-08 15:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20181208_2254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='depart',
            new_name='depart2',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='depart',
            new_name='depart1',
        ),
    ]