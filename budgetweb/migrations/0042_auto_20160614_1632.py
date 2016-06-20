# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0041_auto_20160614_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recettefull',
            name='cptdeplev2',
        ),
        migrations.RemoveField(
            model_name='recettefull',
            name='orfonds',
        ),
        migrations.RemoveField(
            model_name='recettefull',
            name='orfonds2',
        ),
        migrations.AddField(
            model_name='recettefull',
            name='montantdc',
            field=models.DecimalField(max_digits=12, blank=True, decimal_places=2, null=True),
        ),
    ]
