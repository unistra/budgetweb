# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0033_naturecomptable_fondbudget_recette'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naturecomptable',
            name='fondbudget_recette',
            field=models.ForeignKey(verbose_name='Fond budgetaire', to='budgetweb.TheFondBudgetaire'),
        ),
    ]
