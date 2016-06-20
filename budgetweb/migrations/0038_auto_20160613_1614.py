# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0037_auto_20160613_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comptanature',
            name='enveloppe',
        ),
        migrations.RemoveField(
            model_name='fondbudgetaire',
            name='enveloppe',
        ),
        migrations.AddField(
            model_name='naturecomptable',
            name='enveloppe',
            field=models.CharField(blank=True, verbose_name='Enveloppe', max_length=50, default=''),
        ),
    ]
