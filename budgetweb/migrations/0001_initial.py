# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-18 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdresseBudgetaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myid', models.CharField(max_length=100)),
                ('parent', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('compta', models.CharField(max_length=100)),
                ('budget', models.CharField(max_length=100)),
                ('lolf', models.CharField(max_length=100)),
                ('a', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Authorisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('object', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CentreFinancier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('dependsof', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CompteBudgetaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DomaineFonctionnel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MasseMouvementees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myid', models.CharField(max_length=100)),
                ('parent', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('rd', models.CharField(max_length=100)),
                ('input', models.CharField(max_length=100)),
                ('typecontrole', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PlanFinancement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myid', models.CharField(max_length=100)),
                ('parent', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('budget', models.CharField(max_length=100)),
                ('nomades', models.CharField(max_length=100)),
            ],
        ),
    ]
