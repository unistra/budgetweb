# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0053_auto_20160628_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='structure',
            name='modifdate',
            field=models.CharField(max_length=100, default='', verbose_name='Date de modification'),
        ),
    ]
