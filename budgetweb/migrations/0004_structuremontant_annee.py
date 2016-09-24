# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0003_auto_20160918_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='structuremontant',
            name='annee',
            field=models.PositiveIntegerField(verbose_name='Année', default=2000),
            preserve_default=False,
        ),
    ]
