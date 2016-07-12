# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0067_auto_20160712_1420'),
    ]

    operations = [
        migrations.RenameField(
            model_name='domainefonctionnel',
            old_name='dfcode',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='domainefonctionnel',
            old_name='dflabel',
            new_name='label',
        ),
        migrations.RemoveField(
            model_name='domainefonctionnel',
            name='dfdesc',
        ),
        migrations.RemoveField(
            model_name='domainefonctionnel',
            name='dfgrpcumul',
        ),
        migrations.RemoveField(
            model_name='domainefonctionnel',
            name='dfgrpfonc',
        ),
        migrations.RemoveField(
            model_name='domainefonctionnel',
            name='dfrmq',
        ),
        migrations.AddField(
            model_name='domainefonctionnel',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Actif'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Actif'),
        ),
    ]
