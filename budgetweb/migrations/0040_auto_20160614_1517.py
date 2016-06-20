# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0039_auto_20160613_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depensefull',
            name='cptdeplev2',
        ),
        migrations.RemoveField(
            model_name='depensefull',
            name='orfonds',
        ),
        migrations.RemoveField(
            model_name='depensefull',
            name='orfonds2',
        ),
    ]
