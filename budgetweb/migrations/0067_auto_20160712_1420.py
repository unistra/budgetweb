# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0066_auto_20160711_0959'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='structure',
            options={'ordering': ['code']},
        ),
        migrations.RemoveField(
            model_name='structure',
            name='bloq',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='ccassoc',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='cpassoc',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='dfmc',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='fdr',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='modifdate',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='modifpar',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='myid',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='name',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='niv',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='ordre',
        ),
        migrations.RemoveField(
            model_name='structure',
            name='parentid',
        ),
        migrations.AddField(
            model_name='structure',
            name='code',
            field=models.CharField(unique=True, max_length=100, verbose_name='Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='structure',
            name='is_active',
            field=models.BooleanField(default=True, max_length=100, verbose_name='Actif'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='label',
            field=models.CharField(max_length=100, verbose_name='Libellé'),
        ),
    ]
