# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0049_auto_20160624_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depensefull',
            name='structlev1',
            field=models.ForeignKey(null=True, related_name='depensestructlev1', to='budgetweb.Structure', blank=True),
        ),
        migrations.AlterField(
            model_name='depensefull',
            name='structlev2',
            field=models.ForeignKey(null=True, related_name='depensestructlev2', to='budgetweb.Structure', blank=True),
        ),
        migrations.AlterField(
            model_name='depensefull',
            name='structlev3',
            field=models.ForeignKey(null=True, related_name='depensestructlev3', to='budgetweb.Structure', blank=True),
        ),
    ]
