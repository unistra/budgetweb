# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0046_structure_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='structure',
            name='parent',
            field=models.ForeignKey(blank=True, to='budgetweb.Structure', verbose_name='Lien direct vers la structure parent', related_name='fils', null=True),
        ),
    ]
