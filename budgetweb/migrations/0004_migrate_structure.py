# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    tables = [
        'DomaineFonctionnel', 'NatureComptableDepense',
        'NatureComptableRecette', 'PlanFinancement', 'Structure',
    ]

    dependencies = [
        ('budgetweb', '0003_auto_20170427_1132')
    ]

    database_operations = [
        migrations.AlterModelTable(table, 'structure_%s' % table.lower())
        for table in tables
    ]

    state_operations = [migrations.DeleteModel(table) for table in tables]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations
        )
    ]
