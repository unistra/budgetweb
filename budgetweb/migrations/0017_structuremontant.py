# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0016_auto_20160720_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='StructureMontant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depense_montant_dc', models.DecimalField(blank=True, max_digits=12, null=True, decimal_places=2)),
                ('depense_montant_cp', models.DecimalField(blank=True, max_digits=12, null=True, decimal_places=2)),
                ('depense_montant_ae', models.DecimalField(blank=True, max_digits=12, null=True, decimal_places=2)),
                ('recette_montant_dc', models.DecimalField(blank=True, max_digits=12, null=True, decimal_places=2)),
                ('recette_montant_re', models.DecimalField(blank=True, max_digits=12, null=True, decimal_places=2)),
                ('recette_montant_ar', models.DecimalField(blank=True, max_digits=12, null=True, decimal_places=2)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('structure', models.OneToOneField(to='budgetweb.Structure')),
            ],
        ),
    ]
