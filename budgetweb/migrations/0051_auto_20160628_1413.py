# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0050_auto_20160628_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depensefull',
            name='structlev1',
        ),
        migrations.RemoveField(
            model_name='depensefull',
            name='structlev2',
        ),
        migrations.RemoveField(
            model_name='recettefull',
            name='structlev1',
        ),
        migrations.RemoveField(
            model_name='recettefull',
            name='structlev2',
        ),
    ]
