# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0005_auto_20160715_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planfinancement',
            name='date_debut',
            field=models.DateField(null=True, blank=True, verbose_name='Date de début', help_text='Date de début'),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='date_fin',
            field=models.DateField(null=True, blank=True, verbose_name='Date de fin', help_text='Date de fin'),
        ),
    ]
