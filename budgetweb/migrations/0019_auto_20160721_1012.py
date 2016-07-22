# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0018_structure_depth'),
    ]

    operations = [
        migrations.AddField(
            model_name='structuremontant',
            name='periodebudget',
            field=models.ForeignKey(related_name='periodebudgetmontants', to='budgetweb.PeriodeBudget'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='structuremontant',
            name='structure',
            field=models.ForeignKey(to='budgetweb.Structure'),
        ),
        migrations.AlterUniqueTogether(
            name='structuremontant',
            unique_together=set([('structure', 'periodebudget')]),
        ),
    ]
