# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0054_auto_20160628_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depensefull',
            name='myfile',
            field=models.TextField(blank=True, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AlterField(
            model_name='depensefull',
            name='myid',
            field=models.CharField(default='', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='myid',
            field=models.CharField(default='', max_length=100, verbose_name='Code court', blank=True),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='myfile',
            field=models.TextField(blank=True, validators=[django.core.validators.URLValidator()]),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='myid',
            field=models.CharField(default='', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='structure',
            name='myid',
            field=models.CharField(default='', max_length=100, verbose_name='Code', blank=True),
        ),
    ]
