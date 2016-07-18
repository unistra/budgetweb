# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0011_auto_20160718_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='label',
            field=models.CharField(default='', verbose_name='Libellé', max_length=255),
        ),
        migrations.AlterField(
            model_name='naturecomptabledepense',
            name='label_compte_budgetaire',
            field=models.CharField(verbose_name='Désignation du compte budgétaire', max_length=255),
        ),
        migrations.AlterField(
            model_name='naturecomptabledepense',
            name='label_nature_comptable',
            field=models.CharField(verbose_name='Désignation de la nature comptable', max_length=255),
        ),
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='label_compte_budgetaire',
            field=models.CharField(verbose_name='Désignation du compte budgétaire', max_length=255),
        ),
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='label_fonds',
            field=models.CharField(verbose_name='Désignation de la nature comptable', max_length=255),
        ),
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='label_nature_comptable',
            field=models.CharField(verbose_name='Désignation du compte budgétaire', max_length=255),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='label',
            field=models.CharField(verbose_name='Libellé long', max_length=255),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='label',
            field=models.CharField(verbose_name='Libellé', max_length=255),
        ),
        migrations.AlterField(
            model_name='structure',
            name='label',
            field=models.CharField(verbose_name='Libellé', max_length=255),
        ),
    ]
