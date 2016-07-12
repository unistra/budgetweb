# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0069_auto_20160712_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='domainefonctionnel',
            name='is_active',
            field=models.BooleanField(default=True, max_length=100, verbose_name='Actif'),
        ),
    ]
