# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0018_auto_20160531_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='comptecomptable',
            name='ccbd',
            field=models.CharField(verbose_name='Code compte budgétaire dérivé', max_length=100, default=''),
        ),
        migrations.AddField(
            model_name='comptecomptable',
            name='ccbdlabel',
            field=models.CharField(verbose_name='Libellé compte budgétaire dérivé', max_length=100, default=''),
        ),
        migrations.AddField(
            model_name='comptecomptable',
            name='ccnamesecond',
            field=models.CharField(verbose_name='Libellé court nature comptable secondaire', max_length=100, default=''),
        ),
        migrations.AddField(
            model_name='comptecomptable',
            name='decalagetresocpae',
            field=models.BooleanField(verbose_name='Décalage de Trésorerie CP<>AE o/n:', default=False),
        ),
        migrations.AddField(
            model_name='comptecomptable',
            name='pourpfifleche',
            field=models.BooleanField(verbose_name='Utilisé avec un PFI fléché o/n:', default=False),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='ccid',
            field=models.CharField(verbose_name='Code applicatif', max_length=100, default=''),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='ccinput',
            field=models.CharField(verbose_name='Input du cc', max_length=100, default=''),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='cclabel',
            field=models.CharField(verbose_name='Libellé long nature comptable primaire', max_length=100, default=''),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='ccname',
            field=models.CharField(verbose_name='Libellé court nature comptable primaire', max_length=100, default=''),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='ccparent',
            field=models.CharField(verbose_name='Code applicatif du cc parent', max_length=100, default=''),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='cctype',
            field=models.CharField(verbose_name='Type de cc', max_length=100, default=''),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='cctypectrl',
            field=models.CharField(verbose_name='Ctonrol du cc', max_length=100, default=''),
        ),
    ]
