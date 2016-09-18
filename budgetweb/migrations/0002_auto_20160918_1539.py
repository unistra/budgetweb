# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depense',
            name='montant_dc',
            field=models.DecimalField(max_digits=12, null=True, verbose_name='Charges / Immo', blank=True, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='recette',
            name='montant_dc',
            field=models.DecimalField(max_digits=12, null=True, verbose_name='Produits / Ressources', blank=True, decimal_places=2),
        ),
    ]
