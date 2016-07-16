# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0008_auto_20160716_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depense',
            name='naturecomptabledepense',
            field=models.ForeignKey(to='budgetweb.NatureComptableDepense', verbose_name='Nature Comptable'),
        ),
        migrations.AlterField(
            model_name='depense',
            name='periodebudget',
            field=models.ForeignKey(blank=True, to='budgetweb.PeriodeBudget', null=True, verbose_name='Période budgétaire', related_name='periodebudgetdepense'),
        ),
        migrations.AlterField(
            model_name='recette',
            name='naturecomptablerecette',
            field=models.ForeignKey(to='budgetweb.NatureComptableRecette', verbose_name='Nature Comptable'),
        ),
        migrations.AlterField(
            model_name='recette',
            name='periodebudget',
            field=models.ForeignKey(blank=True, to='budgetweb.PeriodeBudget', null=True, verbose_name='Période budgétaire', related_name='periodebudgetrecette'),
        ),
    ]
