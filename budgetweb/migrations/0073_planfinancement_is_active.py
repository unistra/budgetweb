# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0072_auto_20160712_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='planfinancement',
            name='is_active',
            field=models.BooleanField(verbose_name='Actif', default=True, max_length=100),
        ),
    ]
