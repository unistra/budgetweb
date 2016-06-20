# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0032_remove_naturecomptable_fondbudget_rec'),
    ]

    operations = [
        migrations.AddField(
            model_name='naturecomptable',
            name='fondbudget_recette',
            field=models.ForeignKey(to='budgetweb.TheFondBudgetaire', verbose_name='Fond budgetaire', blank=True, default=''),
        ),
    ]
