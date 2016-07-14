# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0003_auto_20160714_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='code_fonds',
            field=models.CharField(max_length=100, verbose_name='Code du fond'),
        ),
        migrations.AlterField(
            model_name='naturecomptablerecette',
            name='code_nature_comptable',
            field=models.CharField(max_length=100, verbose_name='Code de la nature comptable'),
        ),
    ]
