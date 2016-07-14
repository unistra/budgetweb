# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0002_auto_20160713_2241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='depense',
            old_name='strcture',
            new_name='structure',
        ),
    ]
