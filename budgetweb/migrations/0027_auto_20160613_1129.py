# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0026_remove_naturecomptable_ncid'),
    ]

    operations = [
        migrations.CreateModel(
            name='FondBudgetaire',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=100, verbose_name='Code du Fond budgetaire')),
                ('label', models.CharField(default='', max_length=100, verbose_name='Libellé')),
            ],
        ),
        migrations.CreateModel(
            name='NatureC',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=100, verbose_name='Code de la nature comptable')),
                ('label', models.CharField(default='', max_length=100, verbose_name='Libellé')),
            ],
        ),
        migrations.RemoveField(
            model_name='naturecomptable',
            name='nccode',
        ),
        migrations.RemoveField(
            model_name='naturecomptable',
            name='nclabel',
        ),
        migrations.AlterField(
            model_name='comptebudget',
            name='code',
            field=models.CharField(max_length=20, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='comptebudget',
            name='description',
            field=models.CharField(default='', verbose_name='Description', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='comptebudget',
            name='label',
            field=models.CharField(default='', verbose_name='Libellé', max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='naturecomptable',
            name='fondbudget_rec',
            field=models.ForeignKey(default='', verbose_name='Fond budgetaire', to='budgetweb.FondBudgetaire', blank=True),
        ),
        migrations.AddField(
            model_name='naturecomptable',
            name='naturec_dep',
            field=models.ForeignKey(default='', verbose_name='Nature comptable', to='budgetweb.NatureC', blank=True),
        ),
    ]
