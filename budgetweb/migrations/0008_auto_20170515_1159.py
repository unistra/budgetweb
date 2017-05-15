# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0007_period'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='periodebudget',
            name='code',
        ),
        migrations.RemoveField(
            model_name='periodebudget',
            name='label',
        ),
        migrations.AddField(
            model_name='periodebudget',
            name='period',
            field=models.ForeignKey(verbose_name='Period', default=1, to='budgetweb.Period'),
            preserve_default=False,
        ),
    ]
