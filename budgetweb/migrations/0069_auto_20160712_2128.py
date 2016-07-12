# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0068_auto_20160712_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Depense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('montantDC', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('montantCP', models.DecimalField(max_digits=12, blank=True, null=True, verbose_name='Montant Crédit de Paiement', decimal_places=2)),
                ('montantAE', models.DecimalField(max_digits=12, blank=True, null=True, verbose_name="Montant Autorisation d'Engagement", decimal_places=2)),
                ('fonds', models.CharField(default='NA', max_length=100, editable=False)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('lienpiecejointe', models.CharField(blank=True, validators=[django.core.validators.URLValidator()], verbose_name='Lien vers un fichier', max_length=255)),
                ('annee', models.PositiveIntegerField(verbose_name='Année de la saisie')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(blank=True, max_length=100, null=True)),
                ('modifiele', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('modifiepar', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableDepense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Enveloppe')),
                ('label_nature_comptable', models.CharField(max_length=100, verbose_name='Désignation de la nature comptable')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code de la nature comptable')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Code du compte budgétaire')),
                ('label_compte_budgetaire', models.CharField(max_length=100, verbose_name='Désignation du compte budgétaire')),
                ('is_fleche', models.BooleanField(max_length=100, verbose_name='Fleché', default=True)),
                ('is_decalage_tresorerie', models.BooleanField(max_length=100, verbose_name='Décalage trésorerie')),
                ('is_active', models.BooleanField(max_length=100, verbose_name='Actif', default=True)),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableRecette',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Enveloppe')),
                ('label_nature_comptable', models.CharField(max_length=100, verbose_name='Désignation de la nature comptable')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code de la nature comptable')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Code du compte budgétaire')),
                ('label_compte_budgetaire', models.CharField(max_length=100, verbose_name='Désignation du compte budgétaire')),
                ('is_fleche', models.BooleanField(max_length=100, verbose_name='Fleché', default=True)),
                ('is_decalage_tresorerie', models.BooleanField(max_length=100, verbose_name='Décalage trésorerie')),
                ('is_active', models.BooleanField(max_length=100, verbose_name='Actif', default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('montantDC', models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)),
                ('montantRE', models.DecimalField(max_digits=12, blank=True, null=True, verbose_name='Montant Recette Encaissable', decimal_places=2)),
                ('montantAR', models.DecimalField(max_digits=12, blank=True, null=True, verbose_name='Montant Autorisation de Recette', decimal_places=2)),
                ('domainefonctionnel', models.CharField(default='NA', max_length=100, editable=False)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('lienpiecejointe', models.CharField(blank=True, validators=[django.core.validators.URLValidator()], verbose_name='Lien vers un fichier', max_length=255)),
                ('annee', models.PositiveIntegerField(verbose_name='Année de la saisie')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(blank=True, max_length=100, null=True)),
                ('modifiele', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('modifiepar', models.CharField(blank=True, max_length=100, null=True)),
                ('naturecomptablerecette', models.ForeignKey(to='budgetweb.NatureComptableRecette', verbose_name='Nature Comptable Recette')),
                ('periodebudget', models.ForeignKey(blank=True, null=True, to='budgetweb.PeriodeBudget', related_name='periodebudgetrecette')),
                ('pfi', models.ForeignKey(to='budgetweb.PlanFinancement', verbose_name='Programme de financement')),
            ],
        ),
        migrations.RemoveField(
            model_name='depensefull',
            name='cptdeplev1',
        ),
        migrations.RemoveField(
            model_name='depensefull',
            name='domfonc',
        ),
        migrations.RemoveField(
            model_name='depensefull',
            name='periodebudget',
        ),
        migrations.RemoveField(
            model_name='depensefull',
            name='plfi',
        ),
        migrations.RemoveField(
            model_name='depensefull',
            name='structlev3',
        ),
        migrations.RemoveField(
            model_name='naturecomptable',
            name='ccbd',
        ),
        migrations.RemoveField(
            model_name='naturecomptable',
            name='fondbudget_recette',
        ),
        migrations.RemoveField(
            model_name='naturecomptable',
            name='naturec_dep',
        ),
        migrations.RemoveField(
            model_name='recettefull',
            name='cptdeplev1',
        ),
        migrations.RemoveField(
            model_name='recettefull',
            name='domfonc',
        ),
        migrations.RemoveField(
            model_name='recettefull',
            name='periodebudget',
        ),
        migrations.RemoveField(
            model_name='recettefull',
            name='plfi',
        ),
        migrations.RemoveField(
            model_name='recettefull',
            name='structlev3',
        ),
        migrations.RemoveField(
            model_name='domainefonctionnel',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='structure',
            name='is_active',
            field=models.BooleanField(max_length=100, verbose_name='Actif', default=True),
        ),
        migrations.DeleteModel(
            name='ComptaNature',
        ),
        migrations.DeleteModel(
            name='CompteBudget',
        ),
        migrations.DeleteModel(
            name='DepenseFull',
        ),
        migrations.DeleteModel(
            name='FondBudgetaire',
        ),
        migrations.DeleteModel(
            name='NatureComptable',
        ),
        migrations.DeleteModel(
            name='RecetteFull',
        ),
        migrations.AddField(
            model_name='recette',
            name='strcture',
            field=models.ForeignKey(to='budgetweb.Structure', verbose_name='Centre financier'),
        ),
        migrations.AddField(
            model_name='depense',
            name='domainefonctionnel',
            field=models.ForeignKey(to='budgetweb.DomaineFonctionnel', verbose_name='Domaine fonctionnel'),
        ),
        migrations.AddField(
            model_name='depense',
            name='naturecomptabledepense',
            field=models.ForeignKey(to='budgetweb.NatureComptableDepense', verbose_name='Nature Comptable Dépense'),
        ),
        migrations.AddField(
            model_name='depense',
            name='periodebudget',
            field=models.ForeignKey(blank=True, null=True, to='budgetweb.PeriodeBudget', related_name='periodebudgetdepense'),
        ),
        migrations.AddField(
            model_name='depense',
            name='pfi',
            field=models.ForeignKey(to='budgetweb.PlanFinancement', verbose_name='Programme de financement'),
        ),
        migrations.AddField(
            model_name='depense',
            name='strcture',
            field=models.ForeignKey(to='budgetweb.Structure', verbose_name='Centre financier'),
        ),
    ]
