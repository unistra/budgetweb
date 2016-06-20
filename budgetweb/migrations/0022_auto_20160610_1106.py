# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0021_auto_20160610_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planfinancement',
            name='fond',
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='orfonds',
            field=models.ForeignKey(blank=True, to='budgetweb.OrigineFonds', null=True, verbose_name='Fonds'),
        ),
    ]
