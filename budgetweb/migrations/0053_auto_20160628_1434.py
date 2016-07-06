# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0052_auto_20160628_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='ccassoc',
            field=models.CharField(max_length=100, default='', null=True, blank=True, verbose_name='CC associé'),
        ),
        migrations.AddField(
            model_name='structure',
            name='cpassoc',
            field=models.CharField(max_length=100, default='', null=True, blank=True, verbose_name='CP associé'),
        ),
        migrations.AlterField(
            model_name='depensefull',
            name='modifiele',
            field=models.DateTimeField(auto_now=True, verbose_name='Date de modification'),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='modifiepar',
            field=models.CharField(max_length=100, null=True, blank=True, verbose_name='Modification par'),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='modifiele',
            field=models.DateTimeField(auto_now=True, verbose_name='Date de modification'),
        ),
    ]
