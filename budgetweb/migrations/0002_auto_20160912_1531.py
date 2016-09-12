# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='naturecomptabledepense',
            name='is_non_budgetaire',
            field=models.BooleanField(verbose_name='Non budgétaire', default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='naturecomptabledepense',
            name='is_pi_cfg',
            field=models.BooleanField(verbose_name='PI/CFG', default=0, max_length=100),
            preserve_default=False,
        ),
    ]
