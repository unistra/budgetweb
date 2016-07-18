# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0011_auto_20160718_1007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='depense',
            old_name='montantAE',
            new_name='montant_ae',
        ),
        migrations.RenameField(
            model_name='depense',
            old_name='montantCP',
            new_name='montant_cp',
        ),
        migrations.RenameField(
            model_name='depense',
            old_name='montantDC',
            new_name='montant_dc',
        ),
        migrations.RenameField(
            model_name='recette',
            old_name='montantAR',
            new_name='montant_ar',
        ),
        migrations.RenameField(
            model_name='recette',
            old_name='montantDC',
            new_name='montant_dc',
        ),
        migrations.RenameField(
            model_name='recette',
            old_name='montantRE',
            new_name='montant_re',
        ),
    ]
