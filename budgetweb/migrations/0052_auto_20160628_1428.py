# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0051_auto_20160628_1413'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='planfinancement',
            options={'ordering': ['name']},
        ),
    ]
