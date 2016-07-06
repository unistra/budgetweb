# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0064_auto_20160706_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recettefull',
            name='cptdeplev1',
            field=models.ForeignKey(to='budgetweb.NatureComptable', related_name='recettes', verbose_name='Nature comptable'),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='domfonc',
            field=models.ForeignKey(verbose_name='Domaine fonctionnel', to='budgetweb.DomaineFonctionnel'),
        ),
        migrations.AlterField(
            model_name='recettefull',
            name='plfi',
            field=models.ForeignKey(verbose_name='Programme de financement', to='budgetweb.PlanFinancement'),
        ),
    ]
