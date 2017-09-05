# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Depense',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('lienpiecejointe', models.CharField(blank=True, validators=[django.core.validators.URLValidator()], max_length=255, null=True, verbose_name='Lien vers un fichier')),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(blank=True, max_length=100, null=True)),
                ('modifiele', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('modifiepar', models.CharField(blank=True, max_length=100, null=True)),
                ('montant_dc', models.DecimalField(blank=True, max_digits=12, decimal_places=2, null=True, verbose_name='Charges / Immo')),
                ('montant_cp', models.DecimalField(blank=True, max_digits=12, decimal_places=2, null=True, verbose_name='Montant Crédit de Paiement')),
                ('montant_ae', models.DecimalField(blank=True, max_digits=12, decimal_places=2, null=True, verbose_name="Montant Autorisation d'Engagement")),
                ('fonds', models.CharField(max_length=100, editable=False, default='NA')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DomaineFonctionnel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=100, unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=255, default='', verbose_name='Libellé')),
                ('label_court', models.CharField(blank=True, max_length=100, default='', null=True, verbose_name='Libellé court')),
                ('is_active', models.BooleanField(max_length=100, default=True, verbose_name='Actif')),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableDepense',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Enveloppe')),
                ('label_nature_comptable', models.CharField(max_length=255, verbose_name='Désignation de la nature comptable')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code de la nature comptable')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Code du compte budgétaire')),
                ('label_compte_budgetaire', models.CharField(max_length=255, verbose_name='Désignation du compte budgétaire')),
                ('is_fleche', models.BooleanField(max_length=100, default=True, verbose_name='Fleché')),
                ('is_decalage_tresorerie', models.BooleanField(max_length=100, verbose_name='Décalage trésorerie')),
                ('is_non_budgetaire', models.BooleanField(max_length=100, verbose_name='Non budgétaire')),
                ('is_pi_cfg', models.BooleanField(max_length=100, verbose_name='PI/CFG')),
                ('is_active', models.BooleanField(max_length=100, default=True, verbose_name='Actif')),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='Ordre de tri pour les natures                                             comptables')),
                ('ordre', models.PositiveIntegerField(default=1, verbose_name='Sous-ordre de tri pour les natures                                          comptables')),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableRecette',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Enveloppe')),
                ('code_fonds', models.CharField(max_length=100, verbose_name='Code du fonds')),
                ('label_fonds', models.CharField(max_length=255, verbose_name='Désignation du fonds')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code de la nature comptable')),
                ('label_nature_comptable', models.CharField(max_length=255, verbose_name='Désignation de la nature comptable')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Code du compte budgétaire')),
                ('label_compte_budgetaire', models.CharField(max_length=255, verbose_name='Désignation du compte budgétaire')),
                ('is_fleche', models.BooleanField(max_length=100, default=True, verbose_name='Fleché')),
                ('is_ar_and_re', models.BooleanField(max_length=100, verbose_name='AR et RE')),
                ('is_non_budgetaire', models.BooleanField(max_length=100, verbose_name='Non budgétaire dont PI')),
                ('is_active', models.BooleanField(max_length=100, default=True, verbose_name='Actif')),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='Ordre de tri pour les natures                                             comptables')),
                ('ordre', models.PositiveIntegerField(default=1, verbose_name='Sous-ordre de tri pour les natures                                          comptables')),
            ],
        ),
        migrations.CreateModel(
            name='PeriodeBudget',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='Libellé court')),
                ('label', models.CharField(max_length=255, verbose_name='Libellé long')),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activé (oui/non)')),
            ],
        ),
        migrations.CreateModel(
            name='PlanFinancement',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, default='NA', verbose_name='Code du PFI')),
                ('label', models.CharField(max_length=255, verbose_name='Libellé')),
                ('eotp', models.CharField(max_length=100, verbose_name="Code court de l'eotp")),
                ('centrecoutderive', models.CharField(max_length=100, verbose_name='Centre de coût associé')),
                ('centreprofitderive', models.CharField(max_length=100, verbose_name='Centre de profit associé')),
                ('groupe1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Groupe BudgetWeb 1')),
                ('groupe2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Groupe BudgetWeb 2')),
                ('is_fleche', models.BooleanField(default=False, verbose_name='Fléché oui/non')),
                ('is_pluriannuel', models.BooleanField(default=False, verbose_name='Pluriannuel oui/non')),
                ('is_active', models.BooleanField(max_length=100, default=True, verbose_name='Actif')),
                ('date_debut', models.DateField(blank=True, help_text='Date de début', null=True, verbose_name='Date de début')),
                ('date_fin', models.DateField(blank=True, help_text='Date de fin', null=True, verbose_name='Date de fin')),
            ],
            options={
                'ordering': ['label'],
            },
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('lienpiecejointe', models.CharField(blank=True, validators=[django.core.validators.URLValidator()], max_length=255, null=True, verbose_name='Lien vers un fichier')),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(blank=True, max_length=100, null=True)),
                ('modifiele', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('modifiepar', models.CharField(blank=True, max_length=100, null=True)),
                ('montant_dc', models.DecimalField(blank=True, max_digits=12, decimal_places=2, null=True, verbose_name='Produits / Ressources')),
                ('montant_re', models.DecimalField(blank=True, max_digits=12, decimal_places=2, null=True, verbose_name='Montant Recette Encaissable')),
                ('montant_ar', models.DecimalField(blank=True, max_digits=12, decimal_places=2, null=True, verbose_name='Montant Autorisation de Recette')),
                ('domainefonctionnel', models.CharField(max_length=100, editable=False, default='NA')),
                ('naturecomptablerecette', models.ForeignKey(to='budgetweb.NatureComptableRecette', verbose_name='Nature Comptable')),
                ('periodebudget', models.ForeignKey(to='budgetweb.PeriodeBudget', verbose_name='Période budgétaire')),
                ('pfi', models.ForeignKey(to='budgetweb.PlanFinancement', verbose_name='Plan de financement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=255, verbose_name='Libellé')),
                ('groupe1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Groupe BudgetWeb 1')),
                ('groupe2', models.CharField(blank=True, max_length=255, null=True, verbose_name='Groupe BudgetWeb 2')),
                ('is_active', models.BooleanField(max_length=100, default=True, verbose_name='Actif')),
                ('depth', models.PositiveIntegerField()),
                ('path', models.TextField(blank=True, verbose_name='Path')),
                ('parent', models.ForeignKey(null=True, blank=True, verbose_name='Lien direct vers la structure parent', to='budgetweb.Structure', related_name='fils')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='StructureAuthorizations',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('structures', models.ManyToManyField(to='budgetweb.Structure', related_name='authorized_structures')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'structures authorizations',
                'verbose_name': 'structure authorization',
            },
        ),
        migrations.CreateModel(
            name='StructureMontant',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('depense_montant_dc', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('depense_montant_cp', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('depense_montant_ae', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('recette_montant_dc', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('recette_montant_re', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('recette_montant_ar', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('periodebudget', models.ForeignKey(to='budgetweb.PeriodeBudget', related_name='periodebudgetmontants')),
                ('structure', models.ForeignKey(to='budgetweb.Structure')),
            ],
        ),
        migrations.AddField(
            model_name='recette',
            name='structure',
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
            field=models.ForeignKey(to='budgetweb.NatureComptableDepense', verbose_name='Nature Comptable'),
        ),
        migrations.AddField(
            model_name='depense',
            name='periodebudget',
            field=models.ForeignKey(to='budgetweb.PeriodeBudget', verbose_name='Période budgétaire'),
        ),
        migrations.AddField(
            model_name='depense',
            name='pfi',
            field=models.ForeignKey(to='budgetweb.PlanFinancement', verbose_name='Plan de financement'),
        ),
        migrations.AddField(
            model_name='depense',
            name='structure',
            field=models.ForeignKey(to='budgetweb.Structure', verbose_name='Centre financier'),
        ),
        migrations.AlterUniqueTogether(
            name='structuremontant',
            unique_together=set([('structure', 'periodebudget', 'annee')]),
        ),
    ]
