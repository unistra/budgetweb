# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0003_auto_20170427_1132'),
        ('structure', '0002_migrate_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planfinancement',
            name='structure',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='parent',
        ),
        migrations.AlterField(
            model_name='depense',
            name='domainefonctionnel',
            field=models.ForeignKey(verbose_name='Domaine fonctionnel', to='structure.DomaineFonctionnel'),
        ),
        migrations.AlterField(
            model_name='depense',
            name='naturecomptabledepense',
            field=models.ForeignKey(verbose_name='Nature Comptable', to='structure.NatureComptableDepense'),
        ),
        migrations.AlterField(
            model_name='depense',
            name='pfi',
            field=models.ForeignKey(verbose_name='Plan de financement', to='structure.PlanFinancement'),
        ),
        migrations.AlterField(
            model_name='depense',
            name='structure',
            field=models.ForeignKey(verbose_name='Centre financier', to='structure.Structure'),
        ),
        migrations.AlterField(
            model_name='recette',
            name='naturecomptablerecette',
            field=models.ForeignKey(verbose_name='Nature Comptable', to='structure.NatureComptableRecette'),
        ),
        migrations.AlterField(
            model_name='recette',
            name='pfi',
            field=models.ForeignKey(verbose_name='Plan de financement', to='structure.PlanFinancement'),
        ),
        migrations.AlterField(
            model_name='recette',
            name='structure',
            field=models.ForeignKey(verbose_name='Centre financier', to='structure.Structure'),
        ),
        migrations.AlterField(
            model_name='structureauthorizations',
            name='structures',
            field=models.ManyToManyField(related_name='authorized_structures', to='structure.Structure'),
        ),
        migrations.AlterField(
            model_name='structuremontant',
            name='structure',
            field=models.ForeignKey(to='structure.Structure'),
        ),
        migrations.DeleteModel(
            name='DomaineFonctionnel',
        ),
        migrations.DeleteModel(
            name='NatureComptableDepense',
        ),
        migrations.DeleteModel(
            name='NatureComptableRecette',
        ),
        migrations.DeleteModel(
            name='PlanFinancement',
        ),
        migrations.DeleteModel(
            name='Structure',
        ),
    ]
