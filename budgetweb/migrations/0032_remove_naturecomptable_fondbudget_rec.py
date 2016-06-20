# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0031_auto_20160613_1139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='naturecomptable',
            name='fondbudget_rec',
        ),
    ]
