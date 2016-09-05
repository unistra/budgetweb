# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0003_auto_20160905_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='structure',
            name='type',
        ),
        migrations.AddField(
            model_name='structure',
            name='groupe1',
            field=models.CharField(max_length=255, null=True, blank=True, verbose_name='Groupe BudgetWeb 1'),
        ),
        migrations.AddField(
            model_name='structure',
            name='groupe2',
            field=models.CharField(max_length=255, null=True, blank=True, verbose_name='Groupe BudgetWeb 2'),
        ),
    ]
