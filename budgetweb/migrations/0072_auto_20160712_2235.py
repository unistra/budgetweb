# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0071_auto_20160712_2158'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='planfinancement',
            options={'ordering': ['label']},
        ),
        migrations.RenameField(
            model_name='planfinancement',
            old_name='fleche',
            new_name='is_fleche',
        ),
        migrations.RenameField(
            model_name='planfinancement',
            old_name='pluriannuel',
            new_name='is_pluriannuel',
        ),
        migrations.RenameField(
            model_name='planfinancement',
            old_name='name',
            new_name='label',
        ),
        migrations.RenameField(
            model_name='planfinancement',
            old_name='cfassoclink',
            new_name='structure',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='ccassoc',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='cfassoc',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='cpassoc',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='creele',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='creepar',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='modifiele',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='modifiepar',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='myid',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='societe',
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='centrecoutderive',
            field=models.CharField(default='', max_length=100, verbose_name='Centre de coût associé'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='centreprofitderive',
            field=models.CharField(default='', max_length=100, verbose_name='Centre de profit associé'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='code',
            field=models.CharField(default='NA', max_length=100, verbose_name='Code du PFI'),
        ),
    ]
