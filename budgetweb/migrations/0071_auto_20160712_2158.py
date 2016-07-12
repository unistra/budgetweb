# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0070_domainefonctionnel_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='naturecomptablerecette',
            name='is_decalage_tresorerie',
        ),
        migrations.AddField(
            model_name='naturecomptablerecette',
            name='code_fonds',
            field=models.CharField(verbose_name='Code de la nature comptable', max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='naturecomptablerecette',
            name='label_fonds',
            field=models.CharField(verbose_name='Désignation de la nature comptable', max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='code_nature_comptable',
            field=models.CharField(verbose_name='Code du compte budgétaire', max_length=100),
        ),
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='label_nature_comptable',
            field=models.CharField(verbose_name='Désignation du compte budgétaire', max_length=100),
        ),
    ]
