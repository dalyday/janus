# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-12-09 15:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_userinfo_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tools',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_code', models.IntegerField(verbose_name='物料编码')),
                ('material_name', models.CharField(max_length=32, verbose_name='物料名称')),
                ('toolholder', models.IntegerField(verbose_name='刀柄长/mm')),
                ('tool_top', models.IntegerField(verbose_name='刀刃长/mm')),
                ('tool_butoom', models.IntegerField(verbose_name='直径/mm')),
                ('unit', models.CharField(max_length=32, verbose_name='单位')),
                ('number', models.IntegerField(verbose_name='数量')),
                ('depart', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='crm.Department', verbose_name='物料名称')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='仓库名称')),
            ],
        ),
        migrations.AddField(
            model_name='tools',
            name='warehouse',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='crm.Warehouse', verbose_name='仓库名称'),
        ),
    ]
