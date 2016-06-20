# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0035_auto_20160613_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='naturecomptable',
            name='fondbudget_recette',
            field=models.ForeignKey(verbose_name='Fond budgetaire', to='budgetweb.TheFondBudgetaire', default='', blank=True),
        ),
        migrations.AddField(
            model_name='naturecomptable',
            name='naturec_dep',
            field=models.ForeignKey(verbose_name='Nature comptable', to='budgetweb.ComptaNature', default='', blank=True),
        ),
    ]
