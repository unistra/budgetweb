# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='planfinancement',
            name='groupe1',
            field=models.CharField(verbose_name='Groupe BudgetWeb 1', max_length=255, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='groupe2',
            field=models.CharField(verbose_name='Groupe BudgetWeb 2', max_length=255, default=''),
            preserve_default=False,
        ),
    ]
