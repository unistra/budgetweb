# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0007_auto_20160716_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recette',
            name='annee',
            field=models.PositiveIntegerField(verbose_name='Année'),
        ),
    ]
