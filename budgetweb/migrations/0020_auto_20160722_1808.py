# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0019_auto_20160721_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depense',
            name='periodebudget',
            field=models.ForeignKey(verbose_name='Période budgétaire', to='budgetweb.PeriodeBudget'),
        ),
        migrations.AlterField(
            model_name='recette',
            name='periodebudget',
            field=models.ForeignKey(verbose_name='Période budgétaire', to='budgetweb.PeriodeBudget'),
        ),
    ]
