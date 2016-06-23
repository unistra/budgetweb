# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0045_auto_20160616_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='parent',
            field=models.ForeignKey(blank=True, related_name='fils', to='budgetweb.Structure', null=True),
        ),
    ]
