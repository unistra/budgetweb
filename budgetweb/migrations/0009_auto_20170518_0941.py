# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0008_auto_20170515_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodebudget',
            name='date_fin_admin',
            field=models.DateField(verbose_name='Date de fin de la saisie pour les                           superutilisateurs', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='date_fin_dfi',
            field=models.DateField(verbose_name='Date de fin de la saisie pour les utilisateurs                           appartenant au groupe DFI', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='date_fin_retardataire',
            field=models.DateField(verbose_name='Date de fin de la saisie pour les utilisateurs                           appartenant au groupe RETARDATAIRE', blank=True, null=True),
        ),
    ]
