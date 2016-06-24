# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0048_planfinancement_cfassoclink'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='structure',
            options={'ordering': ['name']},
        ),
    ]
