# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0022_auto_20160610_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='NatureComptable',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('ncid', models.CharField(max_length=100, default='', verbose_name='Code applicatif')),
                ('nccode', models.CharField(max_length=100, default='', verbose_name='Code nature comptable')),
                ('nclabel', models.CharField(max_length=100, default='', verbose_name='Libellé nature comptable')),
                ('ncenveloppe', models.CharField(max_length=100, default='', verbose_name='Enveloppe')),
                ('pfifleche', models.BooleanField(default=False, verbose_name='Utilisé avec un PFI fléché o/n:')),
                ('ncsecondairecode', models.CharField(max_length=100, default='', verbose_name='Code nature comptable secondaire')),
                ('decalagetresocpae', models.BooleanField(default=False, verbose_name='Décalage de Trésorerie CP<>AE o/n:')),
                ('nctype', models.CharField(max_length=100, default='', verbose_name='Nature utilisée en recette ou en dépenses')),
                ('ccnamesecond', models.CharField(max_length=100, default='', verbose_name='Libellé court nature comptable secondaire')),
            ],
        ),
        migrations.AlterField(
            model_name='comptebudgetaire',
            name='code',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='depense',
            name='cptdep',
            field=models.ForeignKey(to='budgetweb.NatureComptable', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='depensefull',
            name='cptdeplev1',
            field=models.ForeignKey(related_name='cptdeplev1', to='budgetweb.NatureComptable', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='depensefull',
            name='cptdeplev2',
            field=models.ForeignKey(related_name='cptdeplev2', to='budgetweb.NatureComptable', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='cptdeplev1',
            field=models.ForeignKey(related_name='reccptdeplev1', to='budgetweb.NatureComptable', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='cptdeplev2',
            field=models.ForeignKey(related_name='reccptdeplev2', to='budgetweb.NatureComptable', blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='CompteComptable',
        ),
    ]
