# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-12-07 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20181206_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='depart_code',
            field=models.IntegerField(default=1, verbose_name='部门编码'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='use_status',
            field=models.IntegerField(blank=True, choices=[(1, 'ON'), (2, 'OFF')], null=True, verbose_name='使用状态'),
        ),
    ]
