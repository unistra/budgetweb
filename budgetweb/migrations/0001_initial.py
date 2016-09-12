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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('commentaire', models.TextField(null=True, blank=True)),
                ('lienpiecejointe', models.CharField(verbose_name='Lien vers un fichier', max_length=255, validators=[django.core.validators.URLValidator()], null=True, blank=True)),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(max_length=100, null=True, blank=True)),
                ('modifiele', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('modifiepar', models.CharField(max_length=100, null=True, blank=True)),
                ('montant_dc', models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)),
                ('montant_cp', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Montant Crédit de Paiement', null=True, blank=True)),
                ('montant_ae', models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Montant Autorisation d'Engagement", null=True, blank=True)),
                ('fonds', models.CharField(max_length=100, default='NA', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DomaineFonctionnel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code', default='')),
                ('label', models.CharField(max_length=255, verbose_name='Libellé', default='')),
                ('label_court', models.CharField(default='', max_length=100, verbose_name='Libellé court', null=True, blank=True)),
                ('is_active', models.BooleanField(max_length=100, verbose_name='Actif', default=True)),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableDepense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Enveloppe')),
                ('label_nature_comptable', models.CharField(max_length=255, verbose_name='Désignation de la nature comptable')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code de la nature comptable')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Code du compte budgétaire')),
                ('label_compte_budgetaire', models.CharField(max_length=255, verbose_name='Désignation du compte budgétaire')),
                ('is_fleche', models.BooleanField(max_length=100, verbose_name='Fleché', default=True)),
                ('is_decalage_tresorerie', models.BooleanField(max_length=100, verbose_name='Décalage trésorerie')),
                ('is_non_budgetaire', models.BooleanField(max_length=100, verbose_name='Non budgétaire')),
                ('is_pi_cfg', models.BooleanField(max_length=100, verbose_name='PI/CFG')),
                ('is_active', models.BooleanField(max_length=100, verbose_name='Actif', default=True)),
                ('priority', models.PositiveIntegerField(verbose_name='Ordre de tri pour les natures                                             comptables', default=1)),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableRecette',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Enveloppe')),
                ('code_fonds', models.CharField(max_length=100, verbose_name='Code du fonds')),
                ('label_fonds', models.CharField(max_length=255, verbose_name='Désignation du fonds')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code de la nature comptable')),
                ('label_nature_comptable', models.CharField(max_length=255, verbose_name='Désignation de la nature comptable')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Code du compte budgétaire')),
                ('label_compte_budgetaire', models.CharField(max_length=255, verbose_name='Désignation du compte budgétaire')),
                ('is_fleche', models.BooleanField(max_length=100, verbose_name='Fleché', default=True)),
                ('is_ar_and_re', models.BooleanField(max_length=100, verbose_name='AR et RE')),
                ('is_non_budgetaire', models.BooleanField(max_length=100, verbose_name='Non budgétaire dont PI')),
                ('is_active', models.BooleanField(max_length=100, verbose_name='Actif', default=True)),
                ('priority', models.PositiveIntegerField(verbose_name='Ordre de tri pour les natures                                             comptables', default=1)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodeBudget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(max_length=20, verbose_name='Libellé court')),
                ('label', models.CharField(max_length=255, verbose_name='Libellé long')),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('is_active', models.BooleanField(verbose_name='Activé (oui/,non)', default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanFinancement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(max_length=100, verbose_name='Code du PFI', default='NA')),
                ('label', models.CharField(max_length=255, verbose_name='Libellé')),
                ('eotp', models.CharField(max_length=100, verbose_name="Code court de l'eotp")),
                ('centrecoutderive', models.CharField(max_length=100, verbose_name='Centre de coût associé')),
                ('centreprofitderive', models.CharField(max_length=100, verbose_name='Centre de profit associé')),
                ('groupe1', models.CharField(max_length=255, verbose_name='Groupe BudgetWeb 1', null=True, blank=True)),
                ('groupe2', models.CharField(max_length=255, verbose_name='Groupe BudgetWeb 2', null=True, blank=True)),
                ('is_fleche', models.BooleanField(verbose_name='Fléché oui/non', default=False)),
                ('is_pluriannuel', models.BooleanField(verbose_name='Pluriannuel oui/non', default=False)),
                ('is_active', models.BooleanField(max_length=100, verbose_name='Actif', default=True)),
                ('date_debut', models.DateField(help_text='Date de début', verbose_name='Date de début', null=True, blank=True)),
                ('date_fin', models.DateField(help_text='Date de fin', verbose_name='Date de fin', null=True, blank=True)),
            ],
            options={
                'ordering': ['label'],
            },
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('commentaire', models.TextField(null=True, blank=True)),
                ('lienpiecejointe', models.CharField(verbose_name='Lien vers un fichier', max_length=255, validators=[django.core.validators.URLValidator()], null=True, blank=True)),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(max_length=100, null=True, blank=True)),
                ('modifiele', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('modifiepar', models.CharField(max_length=100, null=True, blank=True)),
                ('montant_dc', models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)),
                ('montant_re', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Montant Recette Encaissable', null=True, blank=True)),
                ('montant_ar', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Montant Autorisation de Recette', null=True, blank=True)),
                ('domainefonctionnel', models.CharField(max_length=100, default='NA', editable=False)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=255, verbose_name='Libellé')),
                ('groupe1', models.CharField(max_length=255, verbose_name='Groupe BudgetWeb 1', null=True, blank=True)),
                ('groupe2', models.CharField(max_length=255, verbose_name='Groupe BudgetWeb 2', null=True, blank=True)),
                ('is_active', models.BooleanField(max_length=100, verbose_name='Actif', default=True)),
                ('depth', models.PositiveIntegerField()),
                ('path', models.TextField(verbose_name='Path', blank=True)),
                ('parent', models.ForeignKey(null=True, related_name='fils', to='budgetweb.Structure', blank=True, verbose_name='Lien direct vers la structure parent')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='StructureAuthorizations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('structures', models.ManyToManyField(related_name='authorized_structures', to='budgetweb.Structure')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'structure authorization',
                'verbose_name_plural': 'structures authorizations',
            },
        ),
        migrations.CreateModel(
            name='StructureMontant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('depense_montant_dc', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('depense_montant_cp', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('depense_montant_ae', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('recette_montant_dc', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('recette_montant_re', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('recette_montant_ar', models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('periodebudget', models.ForeignKey(related_name='periodebudgetmontants', to='budgetweb.PeriodeBudget')),
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
            unique_together=set([('structure', 'periodebudget')]),
        ),
    ]
