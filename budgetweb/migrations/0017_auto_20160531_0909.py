# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0016_auto_20160530_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dfcode',
            field=models.CharField(max_length=100, default='', verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dfdesc',
            field=models.CharField(max_length=100, default='', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dfgrpcumul',
            field=models.CharField(max_length=100, default='', verbose_name='Groupe de cumul'),
        ),
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dfgrpfonc',
            field=models.CharField(max_length=100, default='', verbose_name='Groupe fonctionnel'),
        ),
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dflabel',
            field=models.CharField(max_length=100, default='', verbose_name='Libellé'),
        ),
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dfrmq',
            field=models.CharField(max_length=100, default='', verbose_name='Remarque'),
        ),
    ]
