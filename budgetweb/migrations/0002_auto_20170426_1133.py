# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodebudget',
            name='date_debut_admin',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les super-utilisateurs'),
        ),
        migrations.AddField(
            model_name='periodebudget',
            name='date_debut_dfi',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les utilisateurs appartenant au groupe DFI'),
        ),
        migrations.AddField(
            model_name='periodebudget',
            name='date_debut_retardataire',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les utilisateurs appartenant au groupe RETARDATAIRE'),
        ),
        migrations.AddField(
            model_name='periodebudget',
            name='date_debut_saisie',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les utilisateurs'),
        ),
        migrations.AddField(
            model_name='periodebudget',
            name='date_fin_admin',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les superutilisateurs'),
        ),
        migrations.AddField(
            model_name='periodebudget',
            name='date_fin_dfi',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les utilisateurs appartenant au groupe DFI'),
        ),
        migrations.AddField(
            model_name='periodebudget',
            name='date_fin_retardataire',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de la saisie pour les utilisateurs appartenant au groupe RETARDATAIRE'),
        ),
        migrations.AddField(
            model_name='periodebudget',
            name='date_fin_saisie',
            field=models.DateField(blank=True, null=True, verbose_name='Date de fin de la saisie pour les utilisateurs'),
        ),
    ]
