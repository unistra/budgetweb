# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0006_auto_20160715_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depense',
            name='annee',
            field=models.PositiveIntegerField(verbose_name='Année'),
        ),
    ]
