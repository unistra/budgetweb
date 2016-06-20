# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0036_auto_20160613_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='FondBudgetaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('code', models.CharField(max_length=100, verbose_name='Code du Fond budgetaire')),
                ('label', models.CharField(default='', max_length=100, verbose_name='Libellé')),
                ('enveloppe', models.CharField(blank=True, max_length=50, verbose_name='Enveloppe', default='')),
            ],
        ),
        migrations.RemoveField(
            model_name='naturecomptable',
            name='ncenveloppe',
        ),
        migrations.AddField(
            model_name='comptanature',
            name='enveloppe',
            field=models.CharField(blank=True, max_length=50, verbose_name='Enveloppe', default=''),
        ),
        migrations.AlterField(
            model_name='naturecomptable',
            name='fondbudget_recette',
            field=models.ForeignKey(verbose_name='Fond budgetaire', blank=True, default='', to='budgetweb.FondBudgetaire'),
        ),
        migrations.DeleteModel(
            name='TheFondBudgetaire',
        ),
    ]
