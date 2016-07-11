# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0065_auto_20160706_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='planfinancement',
            name='date_debut',
            field=models.DateTimeField(verbose_name='Date de début', null=True, help_text='Date de début du programme de financement', blank=True),
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='date_fin',
            field=models.DateTimeField(verbose_name='Date de fin', null=True, help_text='Date de fin du programme de financement', blank=True),
        ),
        migrations.AlterField(
            model_name='comptebudget',
            name='description',
            field=models.CharField(verbose_name='Description', max_length=150, default='', blank=True),
        ),
        migrations.AlterField(
            model_name='comptebudget',
            name='label',
            field=models.CharField(verbose_name='Libellé', max_length=150, default='', blank=True),
        ),
    ]
