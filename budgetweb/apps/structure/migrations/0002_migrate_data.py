# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import connection, migrations


def migrate_structure_data(apps, schema_editor):
    tables = [
        'DomaineFonctionnel', 'NatureComptableDepense',
        'NatureComptableRecette', 'PlanFinancement', 'Structure',
    ]

    # Returns if the migration is launched by the unit tests
    if getattr(settings, 'TEST_MODE', False):
        return

    with connection.cursor() as cursor:
        for table in tables:
            name = table.lower()
            data = []

            # Clean destination tables
            cursor.execute("DELETE FROM structure_%s" % name)

            # Get all data
            cursor.execute("SELECT * FROM budgetweb_%s" % name)
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # Copy the data
            model = apps.get_model('structure', table)
            model.objects.bulk_create([model(**row) for row in data])


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_structure_data)
    ]
