# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0004_structuremontant_annee'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='structuremontant',
            unique_together=set([('structure', 'periodebudget', 'annee')]),
        ),
    ]
