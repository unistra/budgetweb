# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-04 13:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0010_auto_20160504_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecetteFull',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myid', models.CharField(max_length=100)),
                ('montant', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('montantar', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('montantre', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('commentaire', models.CharField(blank=True, max_length=100, null=True)),
                ('cptdeplev1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reccptdeplev1', to='budgetweb.CompteComptable')),
                ('cptdeplev2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reccptdeplev2', to='budgetweb.CompteComptable')),
                ('domfonc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgetweb.DomaineFonctionnel')),
                ('orfonds', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recorfonds', to='budgetweb.OrigineFonds')),
                ('orfonds2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recorfonds2', to='budgetweb.OrigineFonds')),
                ('plfi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgetweb.PlanFinancement')),
                ('structlev1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recstructlev1', to='budgetweb.Structure')),
                ('structlev2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recstructlev2', to='budgetweb.Structure')),
                ('structlev3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recstructlev3', to='budgetweb.Structure')),
            ],
        ),
    ]
