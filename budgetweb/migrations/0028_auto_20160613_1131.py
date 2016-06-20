# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0027_auto_20160613_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fondbudgetaire',
            name='code',
            field=models.CharField(max_length=100, verbose_name='Code du Fond budgetaire'),
        ),
        migrations.AlterField(
            model_name='naturec',
            name='code',
            field=models.CharField(max_length=100, verbose_name='Code de la nature comptable'),
        ),
        migrations.AlterField(
            model_name='naturecomptable',
            name='fondbudget_rec',
            field=models.ForeignKey(verbose_name='Fond budgetaire', blank=True, to='budgetweb.FondBudgetaire'),
        ),
        migrations.AlterField(
            model_name='naturecomptable',
            name='naturec_dep',
            field=models.ForeignKey(verbose_name='Nature comptable', blank=True, to='budgetweb.NatureC'),
        ),
    ]
