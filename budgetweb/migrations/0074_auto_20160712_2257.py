# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0073_planfinancement_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planfinancement',
            name='structure',
            field=models.ForeignKey(default='', to='budgetweb.Structure', verbose_name='Lien direct vers le CF'),
            preserve_default=False,
        ),
    ]
