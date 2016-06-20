# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0020_auto_20160608_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='planfinancement',
            name='fond',
            field=models.CharField(verbose_name='Fonds', max_length=100, default=''),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='cfassoc',
            field=models.CharField(verbose_name='Centre financier associé', max_length=100, default=''),
        ),
    ]
