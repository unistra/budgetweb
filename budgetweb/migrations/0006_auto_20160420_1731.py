# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-20 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0005_auto_20160420_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='planfinancement',
            name='creedate',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='creepar',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='dem',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='eotp',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='idabrege',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='modifdate',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='modifpar',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='myid',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
