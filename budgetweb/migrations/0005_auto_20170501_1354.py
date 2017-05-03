# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0004_virement'),
    ]

    operations = [
        migrations.AddField(
            model_name='depense',
            name='virement',
            field=models.ForeignKey(verbose_name="Renvoie vers le virement                                  correspondant s'il existe", to='budgetweb.Virement', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='recette',
            name='virement',
            field=models.ForeignKey(verbose_name="Renvoie vers le virement                                  correspondant s'il existe", to='budgetweb.Virement', null=True, blank=True),
        ),
    ]
