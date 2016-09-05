# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0002_auto_20160905_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planfinancement',
            name='groupe1',
            field=models.CharField(max_length=255, null=True, verbose_name='Groupe BudgetWeb 1', blank=True),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='groupe2',
            field=models.CharField(max_length=255, null=True, verbose_name='Groupe BudgetWeb 2', blank=True),
        ),
    ]
