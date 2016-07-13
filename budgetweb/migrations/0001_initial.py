# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authorisation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('myobject', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Depense',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('montantDC', models.DecimalField(null=True, max_digits=12, blank=True, decimal_places=2)),
                ('montantCP', models.DecimalField(null=True, max_digits=12, blank=True, verbose_name='Montant Crédit de Paiement', decimal_places=2)),
                ('montantAE', models.DecimalField(null=True, max_digits=12, blank=True, verbose_name="Montant Autorisation d'Engagement", decimal_places=2)),
                ('fonds', models.CharField(max_length=100, default='NA', editable=False)),
                ('commentaire', models.TextField(null=True, blank=True)),
                ('lienpiecejointe', models.CharField(validators=[django.core.validators.URLValidator()], max_length=255, blank=True, verbose_name='Lien vers un fichier')),
                ('annee', models.PositiveIntegerField(verbose_name='Année de la saisie')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(null=True, max_length=100, blank=True)),
                ('modifiele', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('modifiepar', models.CharField(null=True, max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DomaineFonctionnel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(max_length=100, default='', unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=100, default='', unique=True, verbose_name='Libellé')),
                ('is_active', models.BooleanField(max_length=100, default=True, verbose_name='Actif')),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableDepense',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Enveloppe')),
                ('label_nature_comptable', models.CharField(max_length=100, verbose_name='Désignation de la nature comptable')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code de la nature comptable')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Code du compte budgétaire')),
                ('label_compte_budgetaire', models.CharField(max_length=100, verbose_name='Désignation du compte budgétaire')),
                ('is_fleche', models.BooleanField(max_length=100, default=True, verbose_name='Fleché')),
                ('is_decalage_tresorerie', models.BooleanField(max_length=100, verbose_name='Décalage trésorerie')),
                ('is_active', models.BooleanField(max_length=100, default=True, verbose_name='Actif')),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableRecette',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Enveloppe')),
                ('label_fonds', models.CharField(max_length=100, verbose_name='Désignation de la nature comptable')),
                ('code_fonds', models.CharField(max_length=100, verbose_name='Code de la nature comptable')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code du compte budgétaire')),
                ('label_nature_comptable', models.CharField(max_length=100, verbose_name='Désignation du compte budgétaire')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Code du compte budgétaire')),
                ('label_compte_budgetaire', models.CharField(max_length=100, verbose_name='Désignation du compte budgétaire')),
                ('is_fleche', models.BooleanField(max_length=100, default=True, verbose_name='Fleché')),
                ('is_active', models.BooleanField(max_length=100, default=True, verbose_name='Actif')),
            ],
        ),
        migrations.CreateModel(
            name='PeriodeBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='Libellé court')),
                ('label', models.CharField(max_length=100, verbose_name='Libellé long')),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activé (oui/,non)')),
            ],
        ),
        migrations.CreateModel(
            name='PlanFinancement',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(max_length=100, default='NA', verbose_name='Code du PFI')),
                ('label', models.CharField(max_length=100, verbose_name='Libellé')),
                ('eotp', models.CharField(max_length=100, verbose_name="Code court de l'eotp")),
                ('centrecoutderive', models.CharField(max_length=100, verbose_name='Centre de coût associé')),
                ('centreprofitderive', models.CharField(max_length=100, verbose_name='Centre de profit associé')),
                ('is_fleche', models.BooleanField(default=False, verbose_name='Fléché oui/non')),
                ('is_pluriannuel', models.BooleanField(default=False, verbose_name='Pluriannuel oui/non')),
                ('is_active', models.BooleanField(max_length=100, default=True, verbose_name='Actif')),
                ('date_debut', models.DateTimeField(null=True, help_text='Date de début du programme de financement', blank=True, verbose_name='Date de début')),
                ('date_fin', models.DateTimeField(null=True, help_text='Date de fin du programme de financement', blank=True, verbose_name='Date de fin')),
            ],
            options={
                'ordering': ['label'],
            },
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('montantDC', models.DecimalField(null=True, max_digits=12, blank=True, decimal_places=2)),
                ('montantRE', models.DecimalField(null=True, max_digits=12, blank=True, verbose_name='Montant Recette Encaissable', decimal_places=2)),
                ('montantAR', models.DecimalField(null=True, max_digits=12, blank=True, verbose_name='Montant Autorisation de Recette', decimal_places=2)),
                ('domainefonctionnel', models.CharField(max_length=100, default='NA', editable=False)),
                ('commentaire', models.TextField(null=True, blank=True)),
                ('lienpiecejointe', models.CharField(validators=[django.core.validators.URLValidator()], max_length=255, blank=True, verbose_name='Lien vers un fichier')),
                ('annee', models.PositiveIntegerField(verbose_name='Année de la saisie')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(null=True, max_length=100, blank=True)),
                ('modifiele', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('modifiepar', models.CharField(null=True, max_length=100, blank=True)),
                ('naturecomptablerecette', models.ForeignKey(to='budgetweb.NatureComptableRecette', verbose_name='Nature Comptable Recette')),
                ('periodebudget', models.ForeignKey(null=True, to='budgetweb.PeriodeBudget', related_name='periodebudgetrecette', blank=True)),
                ('pfi', models.ForeignKey(to='budgetweb.PlanFinancement', verbose_name='Programme de financement')),
            ],
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('type', models.CharField(max_length=100, verbose_name='Type')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=100, verbose_name='Libellé')),
                ('is_active', models.BooleanField(max_length=100, default=True, verbose_name='Actif')),
                ('parent', models.ForeignKey(null=True, verbose_name='Lien direct vers la structure parent', to='budgetweb.Structure', related_name='fils', blank=True)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.AddField(
            model_name='recette',
            name='strcture',
            field=models.ForeignKey(to='budgetweb.Structure', verbose_name='Centre financier'),
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='structure',
            field=models.ForeignKey(to='budgetweb.Structure', verbose_name='Lien direct vers le CF'),
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
            field=models.ForeignKey(null=True, to='budgetweb.PeriodeBudget', related_name='periodebudgetdepense', blank=True),
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
