# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0002_auto_20160912_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='naturecomptablerecette',
            name='is_ar_and_re',
            field=models.BooleanField(max_length=100, default=True, verbose_name='AR et RE'),
        ),
        migrations.AddField(
            model_name='naturecomptablerecette',
            name='is_non_budgetaire',
            field=models.BooleanField(max_length=100, default=True, verbose_name='Non budgétaire dont PI'),
        ),
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='code_fonds',
            field=models.CharField(max_length=100, verbose_name='Code du fonds'),
        ),
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='label_fonds',
            field=models.CharField(max_length=255, verbose_name='Désignation du fonds'),
        ),
    ]
