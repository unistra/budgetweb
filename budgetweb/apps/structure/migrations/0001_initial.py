# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0004_migrate_structure')
    ]

    state_operations = [
        migrations.CreateModel(
            name='DomaineFonctionnel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(unique=True, default='', max_length=100, verbose_name='Code')),
                ('label', models.CharField(default='', max_length=255, verbose_name='Label')),
                ('label_court', models.CharField(blank=True, null=True, default='', max_length=100, verbose_name='Short label')),
                ('is_active', models.BooleanField(default=True, max_length=100, verbose_name='Is active')),
            ],
            options={
                'verbose_name': 'functional domain',
                'verbose_name_plural': 'functional domains'
            },
        ),
        migrations.CreateModel(
            name='NatureComptableDepense',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Envelope')),
                ('label_nature_comptable', models.CharField(max_length=255, verbose_name='Label')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Budget account code')),
                ('label_compte_budgetaire', models.CharField(max_length=255, verbose_name='Budget account label')),
                ('is_fleche', models.BooleanField(default=True, max_length=100, verbose_name='Is labeled')),
                ('is_decalage_tresorerie', models.BooleanField(max_length=100, verbose_name='Is cash shift')),
                ('is_non_budgetaire', models.BooleanField(max_length=100, verbose_name='Is non budgetary')),
                ('is_pi_cfg', models.BooleanField(max_length=100, verbose_name='Is PFI/CFG')),
                ('is_active', models.BooleanField(default=True, max_length=100, verbose_name='Is active')),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='Sorting order for the accounting natures')),
                ('ordre', models.PositiveIntegerField(default=1, verbose_name='Sorting sub-order for the accounting natures')),
            ],
            options={
                'verbose_name': 'expense accounting nature',
                'verbose_name_plural': 'expenses accounting natures'
            },
        ),
        migrations.CreateModel(
            name='NatureComptableRecette',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('enveloppe', models.CharField(max_length=100, verbose_name='Envelope')),
                ('code_fonds', models.CharField(max_length=100, verbose_name='Funds code')),
                ('label_fonds', models.CharField(max_length=255, verbose_name='Funds label')),
                ('code_nature_comptable', models.CharField(max_length=100, verbose_name='Code')),
                ('label_nature_comptable', models.CharField(max_length=255, verbose_name='Label')),
                ('code_compte_budgetaire', models.CharField(max_length=100, verbose_name='Budget account code')),
                ('label_compte_budgetaire', models.CharField(max_length=255, verbose_name='Budget account label')),
                ('is_fleche', models.BooleanField(default=True, max_length=100, verbose_name='Is labeled')),
                ('is_ar_and_re', models.BooleanField(max_length=100, verbose_name='Is AR et RE')),
                ('is_non_budgetaire', models.BooleanField(max_length=100, verbose_name='Is non budgetary')),
                ('is_active', models.BooleanField(default=True, max_length=100, verbose_name='Is active')),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='Sorting order for the accounting natures')),
                ('ordre', models.PositiveIntegerField(default=1, verbose_name='Sorting sub-order for the accounting natures')),
            ],
            options={
                'verbose_name': 'receipt accounting nature',
                'verbose_name_plural': 'receipts accounting natures'
            },
        ),
        migrations.CreateModel(
            name='PlanFinancement',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='NA', max_length=100, verbose_name='Code')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('eotp', models.CharField(max_length=100, verbose_name='EOTP short label')),
                ('centrecoutderive', models.CharField(max_length=100, verbose_name='Related cost center')),
                ('centreprofitderive', models.CharField(max_length=100, verbose_name='Related profit center')),
                ('groupe1', models.CharField(blank=True, null=True, max_length=255, verbose_name='BudgetWeb group 1')),
                ('groupe2', models.CharField(blank=True, null=True, max_length=255, verbose_name='BudgetWeb group 2')),
                ('is_fleche', models.BooleanField(default=False, verbose_name='Is labeled')),
                ('is_pluriannuel', models.BooleanField(default=False, verbose_name='Is multi-year')),
                ('is_active', models.BooleanField(default=True, max_length=100, verbose_name='Is active')),
                ('date_debut', models.DateField(blank=True, help_text='Date de début', verbose_name='Begin date', null=True)),
                ('date_fin', models.DateField(blank=True, help_text='Date de fin', verbose_name='End date', null=True)),
            ],
            options={
                'ordering': ['label'],
                'verbose_name': 'financial plan', 'ordering': ['label'],
                'verbose_name_plural': 'financial plans',
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(unique=True, max_length=100, verbose_name='Code')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('groupe1', models.CharField(blank=True, null=True, max_length=255, verbose_name='BudgetWeb group 1')),
                ('groupe2', models.CharField(blank=True, null=True, max_length=255, verbose_name='BudgetWeb group 2')),
                ('is_active', models.BooleanField(default=True, max_length=100, verbose_name='Is active')),
                ('depth', models.PositiveIntegerField(verbose_name='Depth')),
                ('path', models.TextField(blank=True, verbose_name='Path')),
                ('parent', models.ForeignKey(null=True, to='structure.Structure', blank=True, related_name='fils', verbose_name='Lien direct vers la structure parent')),
            ],
            options={
                'ordering': ['code'],
                'verbose_name': 'structure', 'ordering': ['code'],
                'verbose_name_plural': 'structures'
            },
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='structure',
            field=models.ForeignKey(to='structure.Structure', verbose_name='structure'),
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
