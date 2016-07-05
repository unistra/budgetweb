# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0058_auto_20160705_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dfcode',
            field=models.CharField(default='', verbose_name='Code', unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dfdesc',
            field=models.CharField(default='', verbose_name='Description', blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dfgrpcumul',
            field=models.CharField(default='', verbose_name='Groupe de cumul', blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dfgrpfonc',
            field=models.CharField(default='', verbose_name='Groupe fonctionnel', blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dfrmq',
            field=models.CharField(default='', verbose_name='Remarque', blank=True, max_length=100),
        ),
    ]
