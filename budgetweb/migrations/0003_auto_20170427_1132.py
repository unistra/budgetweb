# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0002_auto_20170426_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodebudget',
            name='ordre',
            field=models.PositiveIntegerField(default=0, verbose_name='Sous-ordre de tri pour les périodes                                          budgétaire'),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='date_debut_admin',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les                           super-utilisateurs'),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='date_debut_dfi',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les utilisateurs                           appartenant au groupe DFI'),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='date_debut_retardataire',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les utilisateurs                           appartenant au groupe RETARDATAIRE'),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='date_debut_saisie',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie                                           pour les utilisateurs'),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='date_fin_admin',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les                           superutilisateurs'),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='date_fin_dfi',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les utilisateurs                           appartenant au groupe DFI'),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='date_fin_retardataire',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les utilisateurs                           appartenant au groupe RETARDATAIRE'),
        ),
    ]
