# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0023_auto_20160610_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompteBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20)),
                ('label', models.CharField(max_length=100, default='', blank=True)),
                ('description', models.CharField(max_length=100, default='', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='naturecomptable',
            name='ccbd',
            field=models.ForeignKey(default='', verbose_name='Compte budgétaire', to='budgetweb.CompteBudget', blank=True),
        ),
    ]
