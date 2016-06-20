# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0030_auto_20160613_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='TheFondBudgetaire',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('code', models.CharField(max_length=100, verbose_name='Code du Fond budgetaire')),
                ('label', models.CharField(max_length=100, verbose_name='Libellé', default='')),
            ],
        ),
        migrations.AlterField(
            model_name='naturecomptable',
            name='fondbudget_rec',
            field=models.ForeignKey(verbose_name='Fond budgetaire', blank=True, to='budgetweb.TheFondBudgetaire', default=''),
        ),
        migrations.DeleteModel(
            name='FondBudgetaire',
        ),
    ]
