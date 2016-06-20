# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0043_auto_20160615_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planfinancement',
            name='orfonds',
        ),
    ]
