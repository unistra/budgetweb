# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Depense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('commentaire', models.TextField(null=True, blank=True)),
                ('lienpiecejointe', models.CharField(null=True, validators=[django.core.validators.URLValidator()], max_length=255, blank=True, verbose_name='Lien vers un fichier')),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(null=True, max_length=100, blank=True)),
                ('modifiele', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('modifiepar', models.CharField(null=True, max_length=100, blank=True)),
                ('montant_dc', models.DecimalField(null=True, decimal_places=2, max_digits=12, blank=True)),
                ('montant_cp', models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, verbose_name='Montant Crédit de Paiement')),
                ('montant_ae', models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, verbose_name="Montant Autorisation d'Engagement")),
                ('fonds', models.CharField(default='NA', editable=False, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DomaineFonctionnel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=100, unique=True, verbose_name='Code')),
                ('label', models.CharField(default='', max_length=255, verbose_name='Libellé')),
                ('label_court', models.CharField(null=True, max_length=100, blank=True, verbose_name='Libellé court', default='')),
                ('is_active', models.BooleanField(default=True, max_length=100, verbose_name='Actif')),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableDepense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Enveloppe')),
                ('label_nature_comptable', models.CharField(max_length=255, verbose_name='Désignation de la nature comptable')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code de la nature comptable')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Code du compte budgétaire')),
                ('label_compte_budgetaire', models.CharField(max_length=255, verbose_name='Désignation du compte budgétaire')),
                ('is_fleche', models.BooleanField(default=True, max_length=100, verbose_name='Fleché')),
                ('is_decalage_tresorerie', models.BooleanField(max_length=100, verbose_name='Décalage trésorerie')),
                ('is_active', models.BooleanField(default=True, max_length=100, verbose_name='Actif')),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='Ordre de tri pour les natures                                             comptables')),
            ],
        ),
        migrations.CreateModel(
            name='NatureComptableRecette',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Enveloppe')),
                ('label_fonds', models.CharField(max_length=255, verbose_name='Désignation de la nature comptable')),
                ('code_fonds', models.CharField(max_length=100, verbose_name='Code du fond')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code de la nature comptable')),
                ('label_nature_comptable', models.CharField(max_length=255, verbose_name='Désignation du compte budgétaire')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Code du compte budgétaire')),
                ('label_compte_budgetaire', models.CharField(max_length=255, verbose_name='Désignation du compte budgétaire')),
                ('is_fleche', models.BooleanField(default=True, max_length=100, verbose_name='Fleché')),
                ('is_active', models.BooleanField(default=True, max_length=100, verbose_name='Actif')),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='Ordre de tri pour les natures                                             comptables')),
            ],
        ),
        migrations.CreateModel(
            name='PeriodeBudget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='Libellé court')),
                ('label', models.CharField(max_length=255, verbose_name='Libellé long')),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activé (oui/,non)')),
            ],
        ),
        migrations.CreateModel(
            name='PlanFinancement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('code', models.CharField(default='NA', max_length=100, verbose_name='Code du PFI')),
                ('label', models.CharField(max_length=255, verbose_name='Libellé')),
                ('eotp', models.CharField(max_length=100, verbose_name="Code court de l'eotp")),
                ('centrecoutderive', models.CharField(max_length=100, verbose_name='Centre de coût associé')),
                ('centreprofitderive', models.CharField(max_length=100, verbose_name='Centre de profit associé')),
                ('is_fleche', models.BooleanField(default=False, verbose_name='Fléché oui/non')),
                ('is_pluriannuel', models.BooleanField(default=False, verbose_name='Pluriannuel oui/non')),
                ('is_active', models.BooleanField(default=True, max_length=100, verbose_name='Actif')),
                ('date_debut', models.DateField(null=True, help_text='Date de début', blank=True, verbose_name='Date de début')),
                ('date_fin', models.DateField(null=True, help_text='Date de fin', blank=True, verbose_name='Date de fin')),
            ],
            options={
                'ordering': ['label'],
            },
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('commentaire', models.TextField(null=True, blank=True)),
                ('lienpiecejointe', models.CharField(null=True, validators=[django.core.validators.URLValidator()], max_length=255, blank=True, verbose_name='Lien vers un fichier')),
                ('annee', models.PositiveIntegerField(verbose_name='Année')),
                ('creele', models.DateTimeField(auto_now_add=True)),
                ('creepar', models.CharField(null=True, max_length=100, blank=True)),
                ('modifiele', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('modifiepar', models.CharField(null=True, max_length=100, blank=True)),
                ('montant_dc', models.DecimalField(null=True, decimal_places=2, max_digits=12, blank=True)),
                ('montant_re', models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, verbose_name='Montant Recette Encaissable')),
                ('montant_ar', models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, verbose_name='Montant Autorisation de Recette')),
                ('domainefonctionnel', models.CharField(default='NA', editable=False, max_length=100)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('type', models.CharField(max_length=100, verbose_name='Type')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Code')),
                ('label', models.CharField(max_length=255, verbose_name='Libellé')),
                ('is_active', models.BooleanField(default=True, max_length=100, verbose_name='Actif')),
                ('depth', models.PositiveIntegerField()),
                ('path', models.TextField(blank=True, verbose_name='Path')),
                ('parent', models.ForeignKey(null=True, blank=True, related_name='fils', to='budgetweb.Structure', verbose_name='Lien direct vers la structure parent')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='StructureAuthorizations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('structures', models.ManyToManyField(related_name='authorized_structures', to='budgetweb.Structure')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('depense_montant_dc', models.DecimalField(default=Decimal('0'), decimal_places=2, max_digits=12)),
                ('depense_montant_cp', models.DecimalField(default=Decimal('0'), decimal_places=2, max_digits=12)),
                ('depense_montant_ae', models.DecimalField(default=Decimal('0'), decimal_places=2, max_digits=12)),
                ('recette_montant_dc', models.DecimalField(default=Decimal('0'), decimal_places=2, max_digits=12)),
                ('recette_montant_re', models.DecimalField(default=Decimal('0'), decimal_places=2, max_digits=12)),
                ('recette_montant_ar', models.DecimalField(default=Decimal('0'), decimal_places=2, max_digits=12)),
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
