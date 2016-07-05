# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0060_auto_20160705_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depensefull',
            name='myfile',
            field=models.TextField(validators=[django.core.validators.URLValidator()], blank=True, verbose_name='Lien vers un fichier'),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='myfile',
            field=models.TextField(validators=[django.core.validators.URLValidator()], blank=True, verbose_name='Lien vers un fichier'),
        ),
    ]
