# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0017_auto_20160531_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comptecomptable',
            name='ccid',
            field=models.CharField(max_length=100, verbose_name='Code applicatif'),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='ccinput',
            field=models.CharField(max_length=100, verbose_name='Input du cc'),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='cclabel',
            field=models.CharField(max_length=100, verbose_name='Libellé long'),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='ccname',
            field=models.CharField(max_length=100, verbose_name='Libellé court'),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='ccparent',
            field=models.CharField(max_length=100, verbose_name='Code applicatif du cc parent'),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='cctype',
            field=models.CharField(max_length=100, verbose_name='Type de cc'),
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='cctypectrl',
            field=models.CharField(max_length=100, verbose_name='Ctonrol du cc'),
        ),
    ]
