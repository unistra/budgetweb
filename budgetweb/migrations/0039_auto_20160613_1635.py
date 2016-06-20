# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0038_auto_20160613_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naturecomptable',
            name='fondbudget_recette',
            field=models.ForeignKey(null=True, to='budgetweb.FondBudgetaire', verbose_name='Fond budgetaire', blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='naturecomptable',
            name='naturec_dep',
            field=models.ForeignKey(null=True, to='budgetweb.ComptaNature', verbose_name='Nature comptable', blank=True, default=''),
        ),
    ]
