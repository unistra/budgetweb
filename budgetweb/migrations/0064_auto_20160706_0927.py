# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0063_auto_20160705_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recettefull',
            name='structlev3',
            field=models.ForeignKey(verbose_name='Structure-CF', related_name='recstructlev3', to='budgetweb.Structure'),
        ),
    ]
