# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0020_auto_20160722_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='structuremontant',
            name='depense_montant_ae',
            field=models.DecimalField(decimal_places=2, max_digits=12, default=Decimal('0')),
        ),
        migrations.AlterField(
            model_name='structuremontant',
            name='depense_montant_cp',
            field=models.DecimalField(decimal_places=2, max_digits=12, default=Decimal('0')),
        ),
        migrations.AlterField(
            model_name='structuremontant',
            name='depense_montant_dc',
            field=models.DecimalField(decimal_places=2, max_digits=12, default=Decimal('0')),
        ),
        migrations.AlterField(
            model_name='structuremontant',
            name='recette_montant_ar',
            field=models.DecimalField(decimal_places=2, max_digits=12, default=Decimal('0')),
        ),
        migrations.AlterField(
            model_name='structuremontant',
            name='recette_montant_dc',
            field=models.DecimalField(decimal_places=2, max_digits=12, default=Decimal('0')),
        ),
        migrations.AlterField(
            model_name='structuremontant',
            name='recette_montant_re',
            field=models.DecimalField(decimal_places=2, max_digits=12, default=Decimal('0')),
        ),
    ]
