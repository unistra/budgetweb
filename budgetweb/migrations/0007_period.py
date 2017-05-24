# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import migrations, models

from budgetweb.models import Period


def forwards_migrate_period(apps, schema_editor):
    call_command('loaddata', 'periods')


def reverse_migrate_period(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0006_virement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(verbose_name='Code', max_length=20)),
                ('label', models.CharField(verbose_name='Label', max_length=255)),
                ('order', models.PositiveIntegerField(verbose_name='Order', default=0)),
            ],
        ),
        migrations.RunPython(forwards_migrate_period, reverse_migrate_period)
    ]
