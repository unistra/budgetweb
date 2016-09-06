# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Depense',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('lienpiecejointe', models.CharField(blank=True, verbose_name='Lien vers un fichier', max_length=255, null=True, validators=[django.core.validators.URLValidator()])),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(blank=True, max_length=100, null=True)),
                ('modifiele', models.DateTimeField(verbose_name='Date de modification', auto_now=True)),
                ('modifiepar', models.CharField(blank=True, max_length=100, null=True)),
                ('montant_dc', models.DecimalField(blank=True, max_digits=12, decimal_places=2, null=True)),
                ('montant_cp', models.DecimalField(blank=True, verbose_name='Montant Crédit de Paiement', max_digits=12, null=True, decimal_places=2)),
                ('montant_ae', models.DecimalField(blank=True, verbose_name="Montant Autorisation d'Engagement", max_digits=12, null=True, decimal_places=2)),
                ('fonds', models.CharField(max_length=100, default='NA', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DomaineFonctionnel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('code', models.CharField(verbose_name='Code', unique=True, max_length=100, default='')),
                ('label', models.CharField(verbose_name='Libellé', max_length=255, default='')),
                ('label_court', models.CharField(blank=True, verbose_name='Libellé court', max_length=100, null=True, default='')),
                ('is_active', models.BooleanField(verbose_name='Actif', max_length=100, default=True)),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableDepense',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('enveloppe', models.CharField(verbose_name='Enveloppe', max_length=100)),
                ('label_nature_comptable', models.CharField(verbose_name='Désignation de la nature comptable', max_length=255)),
                ('code_nature_comptable', models.CharField(verbose_name='Code de la nature comptable', max_length=100)),
                ('code_compte_budgetaire', models.CharField(verbose_name='Code du compte budgétaire', max_length=100)),
                ('label_compte_budgetaire', models.CharField(verbose_name='Désignation du compte budgétaire', max_length=255)),
                ('is_fleche', models.BooleanField(verbose_name='Fleché', max_length=100, default=True)),
                ('is_decalage_tresorerie', models.BooleanField(verbose_name='Décalage trésorerie', max_length=100)),
                ('is_active', models.BooleanField(verbose_name='Actif', max_length=100, default=True)),
                ('priority', models.PositiveIntegerField(verbose_name='Ordre de tri pour les natures                                             comptables', default=1)),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableRecette',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('enveloppe', models.CharField(verbose_name='Enveloppe', max_length=100)),
                ('label_fonds', models.CharField(verbose_name='Désignation de la nature comptable', max_length=255)),
                ('code_fonds', models.CharField(verbose_name='Code du fond', max_length=100)),
                ('code_nature_comptable', models.CharField(verbose_name='Code de la nature comptable', max_length=100)),
                ('label_nature_comptable', models.CharField(verbose_name='Désignation du compte budgétaire', max_length=255)),
                ('code_compte_budgetaire', models.CharField(verbose_name='Code du compte budgétaire', max_length=100)),
                ('label_compte_budgetaire', models.CharField(verbose_name='Désignation du compte budgétaire', max_length=255)),
                ('is_fleche', models.BooleanField(verbose_name='Fleché', max_length=100, default=True)),
                ('is_active', models.BooleanField(verbose_name='Actif', max_length=100, default=True)),
                ('priority', models.PositiveIntegerField(verbose_name='Ordre de tri pour les natures                                             comptables', default=1)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodeBudget',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('code', models.CharField(verbose_name='Libellé court', max_length=20)),
                ('label', models.CharField(verbose_name='Libellé long', max_length=255)),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('is_active', models.BooleanField(verbose_name='Activé (oui/,non)', default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanFinancement',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('code', models.CharField(verbose_name='Code du PFI', max_length=100, default='NA')),
                ('label', models.CharField(verbose_name='Libellé', max_length=255)),
                ('eotp', models.CharField(verbose_name="Code court de l'eotp", max_length=100)),
                ('centrecoutderive', models.CharField(verbose_name='Centre de coût associé', max_length=100)),
                ('centreprofitderive', models.CharField(verbose_name='Centre de profit associé', max_length=100)),
                ('groupe1', models.CharField(blank=True, verbose_name='Groupe BudgetWeb 1', max_length=255, null=True)),
                ('groupe2', models.CharField(blank=True, verbose_name='Groupe BudgetWeb 2', max_length=255, null=True)),
                ('is_fleche', models.BooleanField(verbose_name='Fléché oui/non', default=False)),
                ('is_pluriannuel', models.BooleanField(verbose_name='Pluriannuel oui/non', default=False)),
                ('is_active', models.BooleanField(verbose_name='Actif', max_length=100, default=True)),
                ('date_debut', models.DateField(blank=True, verbose_name='Date de début', null=True, help_text='Date de début')),
                ('date_fin', models.DateField(blank=True, verbose_name='Date de fin', null=True, help_text='Date de fin')),
            ],
            options={
                'ordering': ['label'],
            },
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('lienpiecejointe', models.CharField(blank=True, verbose_name='Lien vers un fichier', max_length=255, null=True, validators=[django.core.validators.URLValidator()])),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(blank=True, max_length=100, null=True)),
                ('modifiele', models.DateTimeField(verbose_name='Date de modification', auto_now=True)),
                ('modifiepar', models.CharField(blank=True, max_length=100, null=True)),
                ('montant_dc', models.DecimalField(blank=True, max_digits=12, decimal_places=2, null=True)),
                ('montant_re', models.DecimalField(blank=True, verbose_name='Montant Recette Encaissable', max_digits=12, null=True, decimal_places=2)),
                ('montant_ar', models.DecimalField(blank=True, verbose_name='Montant Autorisation de Recette', max_digits=12, null=True, decimal_places=2)),
                ('domainefonctionnel', models.CharField(max_length=100, default='NA', editable=False)),
                ('naturecomptablerecette', models.ForeignKey(verbose_name='Nature Comptable', to='budgetweb.NatureComptableRecette')),
                ('periodebudget', models.ForeignKey(verbose_name='Période budgétaire', to='budgetweb.PeriodeBudget')),
                ('pfi', models.ForeignKey(verbose_name='Plan de financement', to='budgetweb.PlanFinancement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('code', models.CharField(verbose_name='Code', unique=True, max_length=100)),
                ('label', models.CharField(verbose_name='Libellé', max_length=255)),
                ('groupe1', models.CharField(blank=True, verbose_name='Groupe BudgetWeb 1', max_length=255, null=True)),
                ('groupe2', models.CharField(blank=True, verbose_name='Groupe BudgetWeb 2', max_length=255, null=True)),
                ('is_active', models.BooleanField(verbose_name='Actif', max_length=100, default=True)),
                ('depth', models.PositiveIntegerField()),
                ('path', models.TextField(blank=True, verbose_name='Path')),
                ('parent', models.ForeignKey(blank=True, verbose_name='Lien direct vers la structure parent', null=True, related_name='fils', to='budgetweb.Structure')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='StructureAuthorizations',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
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
            field=models.ForeignKey(verbose_name='Centre financier', to='budgetweb.Structure'),
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='structure',
            field=models.ForeignKey(verbose_name='Lien direct vers le CF', to='budgetweb.Structure'),
        ),
        migrations.AddField(
            model_name='depense',
            name='domainefonctionnel',
            field=models.ForeignKey(verbose_name='Domaine fonctionnel', to='budgetweb.DomaineFonctionnel'),
        ),
        migrations.AddField(
            model_name='depense',
            name='naturecomptabledepense',
            field=models.ForeignKey(verbose_name='Nature Comptable', to='budgetweb.NatureComptableDepense'),
        ),
        migrations.AddField(
            model_name='depense',
            name='periodebudget',
            field=models.ForeignKey(verbose_name='Période budgétaire', to='budgetweb.PeriodeBudget'),
        ),
        migrations.AddField(
            model_name='depense',
            name='pfi',
            field=models.ForeignKey(verbose_name='Plan de financement', to='budgetweb.PlanFinancement'),
        ),
        migrations.AddField(
            model_name='depense',
            name='structure',
            field=models.ForeignKey(verbose_name='Centre financier', to='budgetweb.Structure'),
        ),
        migrations.AlterUniqueTogether(
            name='structuremontant',
            unique_together=set([('structure', 'periodebudget')]),
        ),
    ]
