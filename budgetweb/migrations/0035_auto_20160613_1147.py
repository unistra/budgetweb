# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0034_auto_20160613_1141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='naturecomptable',
            name='fondbudget_recette',
        ),
        migrations.RemoveField(
            model_name='naturecomptable',
            name='naturec_dep',
        ),
    ]
