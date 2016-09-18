# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0002_auto_20160918_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='naturecomptabledepense',
            name='ordre',
            field=models.PositiveIntegerField(default=1, verbose_name='Sous-ordre de tri pour les natures                                          comptables'),
        ),
        migrations.AddField(
            model_name='naturecomptablerecette',
            name='ordre',
            field=models.PositiveIntegerField(default=1, verbose_name='Sous-ordre de tri pour les natures                                          comptables'),
        ),
    ]
