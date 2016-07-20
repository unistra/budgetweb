# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0015_auto_20160720_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depense',
            name='periodebudget',
            field=models.ForeignKey(verbose_name='Période budgétaire', related_name='periodebudgetdepense', default='toto', to='budgetweb.PeriodeBudget'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recette',
            name='periodebudget',
            field=models.ForeignKey(verbose_name='Période budgétaire', related_name='periodebudgetrecette', default='toto', to='budgetweb.PeriodeBudget'),
            preserve_default=False,
        ),
    ]
