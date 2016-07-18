# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0009_auto_20160716_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='domainefonctionnel',
            name='label_court',
            field=models.CharField(verbose_name='Libellé court', null=True, blank=True, default='', max_length=100),
        ),
    ]
