# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0014_auto_20160718_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depense',
            name='lienpiecejointe',
            field=models.CharField(validators=[django.core.validators.URLValidator()], blank=True, verbose_name='Lien vers un fichier', null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='recette',
            name='lienpiecejointe',
            field=models.CharField(validators=[django.core.validators.URLValidator()], blank=True, verbose_name='Lien vers un fichier', null=True, max_length=255),
        ),
    ]
