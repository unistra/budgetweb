# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0004_auto_20160912_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='label_nature_comptable',
            field=models.CharField(max_length=255, verbose_name='Désignation de la nature comptable'),
        ),
    ]
