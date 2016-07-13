# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recette',
            old_name='strcture',
            new_name='structure',
        ),
        migrations.AlterField(
            model_name='structure',
            name='parent',
            field=models.ForeignKey(blank=True, related_name='fils', null=True, to='budgetweb.Structure', verbose_name='Lien direct vers le parent'),
        ),
    ]
