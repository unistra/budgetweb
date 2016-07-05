# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0056_auto_20160705_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depensefull',
            name='domfonc',
            field=models.ForeignKey(verbose_name='Domaine fonctionnel', to='budgetweb.DomaineFonctionnel', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='depensefull',
            name='plfi',
            field=models.ForeignKey(verbose_name='Programme de financement', to='budgetweb.PlanFinancement', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='domfonc',
            field=models.ForeignKey(verbose_name='Domaine focntionnel', to='budgetweb.DomaineFonctionnel', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='plfi',
            field=models.ForeignKey(verbose_name='Programme de financement', to='budgetweb.PlanFinancement', blank=True, null=True),
        ),
    ]
