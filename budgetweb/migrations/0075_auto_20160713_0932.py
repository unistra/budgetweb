# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0074_auto_20160712_2257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='periodebudget',
            old_name='name',
            new_name='code',
        ),
        migrations.RemoveField(
            model_name='periodebudget',
            name='bloque',
        ),
        migrations.AddField(
            model_name='periodebudget',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Activé (oui/,non)'),
        ),
        migrations.AlterField(
            model_name='periodebudget',
            name='annee',
            field=models.PositiveIntegerField(default='2017', verbose_name='Année'),
            preserve_default=False,
        ),
    ]
