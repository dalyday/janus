# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-12-08 15:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_auto_20181208_2309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='depart2',
            new_name='depart',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='depart1',
            new_name='depart',
        ),
    ]