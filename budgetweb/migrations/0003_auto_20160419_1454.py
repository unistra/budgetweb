# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-19 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0002_auto_20160419_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domainefonctionnel',
            name='code',
        ),
        migrations.RemoveField(
            model_name='domainefonctionnel',
            name='label',
        ),
        migrations.AddField(
            model_name='domainefonctionnel',
            name='dfcode',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='domainefonctionnel',
            name='dfdesc',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='domainefonctionnel',
            name='dfgrpcumul',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='domainefonctionnel',
            name='dfgrpfonc',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='domainefonctionnel',
            name='dflabel',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='domainefonctionnel',
            name='dfrmq',
            field=models.CharField(default='', max_length=100),
        ),
    ]
