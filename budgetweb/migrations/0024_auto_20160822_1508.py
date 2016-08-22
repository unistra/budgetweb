# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0023_auto_20160822_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='naturecomptabledepense',
            name='priority',
            field=models.PositiveIntegerField(default=1, verbose_name='Ordre de tri pour les natures                                             comptables'),
        ),
        migrations.AddField(
            model_name='naturecomptablerecette',
            name='priority',
            field=models.PositiveIntegerField(default=1, verbose_name='Ordre de tri pour les natures                                             comptables'),
        ),
    ]
