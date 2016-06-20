# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0042_auto_20160614_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depensefull',
            name='cptdeplev1',
            field=models.ForeignKey(verbose_name='Nature comptable', related_name='depenses', null=True, to='budgetweb.NatureComptable', blank=True),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='cptdeplev1',
            field=models.ForeignKey(verbose_name='Nature comptable', related_name='recettes', null=True, to='budgetweb.NatureComptable', blank=True),
        ),
    ]
