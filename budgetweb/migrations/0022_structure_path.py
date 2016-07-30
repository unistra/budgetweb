# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0021_auto_20160727_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='path',
            field=models.TextField(blank=True, verbose_name='Path'),
        ),
    ]
