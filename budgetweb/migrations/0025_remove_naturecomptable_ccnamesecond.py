# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0024_auto_20160610_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='naturecomptable',
            name='ccnamesecond',
        ),
    ]
