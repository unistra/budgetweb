# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0005_auto_20170503_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='Virement',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('document_number', models.PositiveIntegerField(verbose_name='Numéro de document SIFAC')),
                ('document_type', models.CharField(verbose_name='Type de document SIFAC', max_length=100)),
                ('version', models.CharField(verbose_name='Version de budget', max_length=100)),
                ('perimetre', models.CharField(verbose_name='Périmètre financier', max_length=10)),
                ('process', models.CharField(verbose_name='Type de virement', max_length=10)),
                ('creator_login', models.CharField(verbose_name='Compte SIFAC ayant créé le virement', max_length=100)),
                ('creation_date', models.DateTimeField(verbose_name='Date de création du virement')),
                ('value_date', models.DateField(verbose_name='Date de valeur')),
            ],
            options={
                'verbose_name': 'transfer',
                'verbose_name_plural': 'transfers'
            },
        ),
        migrations.AddField(
            model_name='depense',
            name='virement',
            field=models.ForeignKey(
                verbose_name="Renvoie vers le virement correspondant s'il existe",
                to='budgetweb.Virement', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recette',
            name='virement',
            field=models.ForeignKey(
                verbose_name="Renvoie vers le virement correspondant s'il existe",
                to='budgetweb.Virement', null=True, blank=True),
        ),
    ]
