# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0061_auto_20160705_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depensefull',
            name='structlev3',
            field=models.ForeignKey(verbose_name='Structure-CF', related_name='depensestructlev3', to='budgetweb.Structure'),
        ),
    ]
