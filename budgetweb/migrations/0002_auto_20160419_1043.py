# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-19 08:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompteComptable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ccid', models.CharField(max_length=100)),
                ('ccparent', models.CharField(max_length=100)),
                ('ccname', models.CharField(max_length=100)),
                ('cclabel', models.CharField(max_length=100)),
                ('cctype', models.CharField(max_length=100)),
                ('ccinput', models.CharField(max_length=100)),
                ('cctypectrl', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='refdfi',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='refsifac',
            field=models.CharField(default='', max_length=100),
        ),
    ]
