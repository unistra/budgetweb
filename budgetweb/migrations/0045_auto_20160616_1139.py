# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0044_remove_planfinancement_orfonds'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AdresseBudgetaire',
        ),
        migrations.DeleteModel(
            name='CompteBudgetaire',
        ),
        migrations.RemoveField(
            model_name='depense',
            name='cptdep',
        ),
        migrations.RemoveField(
            model_name='depense',
            name='domfonc',
        ),
        migrations.RemoveField(
            model_name='depense',
            name='orfonds',
        ),
        migrations.RemoveField(
            model_name='depense',
            name='plfi',
        ),
        migrations.RemoveField(
            model_name='depense',
            name='struct',
        ),
        migrations.DeleteModel(
            name='MasseMouvementees',
        ),
        migrations.DeleteModel(
            name='Depense',
        ),
        migrations.DeleteModel(
            name='OrigineFonds',
        ),
    ]
