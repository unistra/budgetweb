# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0004_auto_20160714_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planfinancement',
            name='date_debut',
            field=models.DateField(help_text='Date de début du programme de financement', verbose_name='Date de début', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='date_fin',
            field=models.DateField(help_text='Date de fin du programme de financement', verbose_name='Date de fin', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='structure',
            name='parent',
            field=models.ForeignKey(related_name='fils', verbose_name='Lien direct vers la structure parent', blank=True, to='budgetweb.Structure', null=True),
        ),
    ]
