# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import connection, migrations


def delete_old_data(apps, schema_editor):
    tables = [
        'DomaineFonctionnel', 'NatureComptableDepense',
        'NatureComptableRecette', 'PlanFinancement', 'Structure',
    ]

    # Erase the old tables
    with connection.cursor() as cursor:
        for table in tables:
            # Check the rowcount
            name = table.lower()
            model = apps.get_model('structure', table)
            cursor.execute("SELECT count(*) FROM budgetweb_%s" % name)
            source_count = cursor.fetchone()[0]
            dest_count = model.objects.count()
            if source_count == dest_count:
                cursor.execute("DROP TABLE budgetweb_%s" % name)
            else:
                raise Exception(
                    'The rowcount is different between budgetweb_{} and '
                    'structure_{}'.format(name))


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0002_migrate_data'),
        ('budgetweb', '0004_auto_20170503_1015'),
    ]

    operations = [
        migrations.RunPython(delete_old_data)
    ]
