# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0047_auto_20160624_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='planfinancement',
            name='cfassoclink',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Lien direct vers le CF', to='budgetweb.Structure'),
        ),
    ]
