# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0028_auto_20160613_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naturecomptable',
            name='fondbudget_rec',
            field=models.ForeignKey(verbose_name='Fond budgetaire', default='', blank=True, to='budgetweb.FondBudgetaire'),
        ),
        migrations.AlterField(
            model_name='naturecomptable',
            name='naturec_dep',
            field=models.ForeignKey(verbose_name='Nature comptable', default='', blank=True, to='budgetweb.NatureC'),
        ),
    ]
