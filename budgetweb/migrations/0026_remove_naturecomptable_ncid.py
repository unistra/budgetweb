# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0025_remove_naturecomptable_ccnamesecond'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='naturecomptable',
            name='ncid',
        ),
    ]
