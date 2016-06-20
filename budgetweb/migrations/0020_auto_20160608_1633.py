# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0019_auto_20160531_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='depensefull',
            name='myfile',
            field=models.TextField(default='', validators=[django.core.validators.URLValidator()]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recettefull',
            name='myfile',
            field=models.TextField(default='', validators=[django.core.validators.URLValidator()]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comptecomptable',
            name='cctypectrl',
            field=models.CharField(default='', max_length=100, verbose_name='Control pour le cc'),
        ),
        migrations.AlterField(
            model_name='originefonds',
            name='ofbudget',
            field=models.CharField(verbose_name='Budget', max_length=100),
        ),
        migrations.AlterField(
            model_name='originefonds',
            name='ofid',
            field=models.CharField(verbose_name='Code du fond', max_length=100),
        ),
        migrations.AlterField(
            model_name='originefonds',
            name='oflabel',
            field=models.CharField(verbose_name='Nom long du fond', max_length=100),
        ),
        migrations.AlterField(
            model_name='originefonds',
            name='ofname',
            field=models.CharField(verbose_name='Nom court du fond', max_length=100),
        ),
        migrations.AlterField(
            model_name='originefonds',
            name='ofnomades',
            field=models.CharField(verbose_name='Nomades', max_length=100),
        ),
        migrations.AlterField(
            model_name='originefonds',
            name='ofparent',
            field=models.CharField(verbose_name='Code du fond parent', max_length=100),
        ),
        migrations.AlterField(
            model_name='originefonds',
            name='oftype',
            field=models.CharField(verbose_name='Type du fond', max_length=100),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='annee',
            field=models.DateField(verbose_name='Année', null=True),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='bloque',
            field=models.BooleanField(default=True, verbose_name='Bloqué (False=Actif)'),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='label',
            field=models.CharField(verbose_name='Libellé long', max_length=100),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='name',
            field=models.CharField(verbose_name='Libellé court', max_length=20),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='ccassoc',
            field=models.CharField(default='', max_length=100, verbose_name='Centre de coût associé'),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='cfassoc',
            field=models.CharField(default='', max_length=100, verbose_name='Centre dinancier associé'),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='cpassoc',
            field=models.CharField(default='', max_length=100, verbose_name='Centre de profit associé'),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='creele',
            field=models.DateTimeField(verbose_name='Date de création', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='creepar',
            field=models.CharField(verbose_name='Créé par', blank=True, null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='eotp',
            field=models.CharField(verbose_name="Code court de l'eotp", max_length=100),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='fleche',
            field=models.BooleanField(default=False, verbose_name='Fléché oui/non'),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='modifiele',
            field=models.DateTimeField(verbose_name='Date de modification', auto_now=True),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='modifiepar',
            field=models.CharField(verbose_name='Date de modification', blank=True, null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='myid',
            field=models.CharField(verbose_name='Code court', max_length=100),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='name',
            field=models.CharField(verbose_name='Libellé', max_length=100),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='pluriannuel',
            field=models.BooleanField(default=False, verbose_name='Pluriannuel oui/non'),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='societe',
            field=models.CharField(default='', max_length=100, verbose_name='Société'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='bloq',
            field=models.CharField(verbose_name='Bloqué', max_length=100),
        ),
        migrations.AlterField(
            model_name='structure',
            name='dfmc',
            field=models.CharField(verbose_name='DFMC', max_length=100),
        ),
        migrations.AlterField(
            model_name='structure',
            name='fdr',
            field=models.CharField(verbose_name='FDR', max_length=100),
        ),
        migrations.AlterField(
            model_name='structure',
            name='label',
            field=models.CharField(verbose_name='Libellé long', max_length=100),
        ),
        migrations.AlterField(
            model_name='structure',
            name='modifdate',
            field=models.CharField(verbose_name='Date de modification', max_length=100),
        ),
        migrations.AlterField(
            model_name='structure',
            name='modifpar',
            field=models.CharField(verbose_name='Modifié par', max_length=100),
        ),
        migrations.AlterField(
            model_name='structure',
            name='myid',
            field=models.CharField(verbose_name='Code', max_length=100),
        ),
        migrations.AlterField(
            model_name='structure',
            name='name',
            field=models.CharField(verbose_name='Libellé court', max_length=100),
        ),
        migrations.AlterField(
            model_name='structure',
            name='niv',
            field=models.CharField(verbose_name='Niveau', max_length=100),
        ),
        migrations.AlterField(
            model_name='structure',
            name='ordre',
            field=models.CharField(verbose_name='Ordre', max_length=100),
        ),
        migrations.AlterField(
            model_name='structure',
            name='parentid',
            field=models.CharField(verbose_name='Code de la structure père', max_length=100),
        ),
        migrations.AlterField(
            model_name='structure',
            name='type',
            field=models.CharField(verbose_name='Type', max_length=100),
        ),
    ]
