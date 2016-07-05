# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0062_auto_20160705_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depensefull',
            name='plfi',
            field=models.ForeignKey(verbose_name='Programme de financement', to='budgetweb.PlanFinancement'),
        ),
    ]
