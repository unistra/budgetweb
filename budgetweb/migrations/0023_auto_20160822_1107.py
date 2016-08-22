# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0022_structure_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depense',
            name='pfi',
            field=models.ForeignKey(verbose_name='Plan de financement', to='budgetweb.PlanFinancement'),
        ),
        migrations.AlterField(
            model_name='recette',
            name='pfi',
            field=models.ForeignKey(verbose_name='Plan de financement', to='budgetweb.PlanFinancement'),
        ),
    ]
