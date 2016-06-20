# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0040_auto_20160614_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depensefull',
            name='cptdeplev1',
            field=models.ForeignKey(blank=True, to='budgetweb.NatureComptable', null=True, related_name='depenses'),
        ),
    ]
