# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0014_auto_20160513_1532'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authorisation',
            old_name='object',
            new_name='myobject',
        ),
    ]
