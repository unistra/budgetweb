# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0059_auto_20160705_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='dflabel',
            field=models.CharField(verbose_name='Libellé', default='', max_length=100, unique=True),
        ),
    ]
