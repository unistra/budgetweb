# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0010_domainefonctionnel_label_court'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainefonctionnel',
            name='label',
            field=models.CharField(max_length=100, verbose_name='Libellé', default=''),
        ),
    ]
