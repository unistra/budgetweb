# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0017_structuremontant'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='depth',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
