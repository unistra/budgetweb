# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0003_auto_20160912_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='is_ar_and_re',
            field=models.BooleanField(verbose_name='AR et RE', max_length=100),
        ),
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='is_non_budgetaire',
            field=models.BooleanField(verbose_name='Non budgétaire dont PI', max_length=100),
        ),
    ]
