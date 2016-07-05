# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0055_auto_20160701_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depensefull',
            name='structlev3',
            field=models.ForeignKey(to='budgetweb.Structure', verbose_name='Structure-CF', null=True, blank=True, related_name='depensestructlev3'),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='structlev3',
            field=models.ForeignKey(to='budgetweb.Structure', verbose_name='Structure-CF', null=True, blank=True, related_name='recstructlev3'),
        ),
    ]
