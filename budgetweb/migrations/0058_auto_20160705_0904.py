# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0057_auto_20160705_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recettefull',
            name='domfonc',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Domaine fonctionnel', to='budgetweb.DomaineFonctionnel'),
        ),
    ]
