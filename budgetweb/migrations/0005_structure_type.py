# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0004_auto_20160905_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='type',
            field=models.CharField(max_length=255, blank=True, verbose_name='Groupe BudgetWeb 2', null=True),
        ),
    ]
