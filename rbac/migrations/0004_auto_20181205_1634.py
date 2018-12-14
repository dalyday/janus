# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-12-05 08:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_auto_20181205_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=32, verbose_name='菜单标题'),
        ),
        migrations.AlterField(
            model_name='permissiongroup',
            name='caption',
            field=models.CharField(max_length=32, verbose_name='权限组名称'),
        ),
        migrations.AlterField(
            model_name='permissiongroup',
            name='menu',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='所属菜单'),
        ),
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='rbac.Permission', verbose_name='拥有的所有权限'),
        ),
    ]