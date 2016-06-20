# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0015_auto_20160519_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planfinancement',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='cleregul',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='creedate',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='dem',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='divirecette',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='domainefonc',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='dordre',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='idabrege',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='label',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='modifdate',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='modifpar',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='nomades',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='refdfi',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='refsifac',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='responsable',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='status',
        ),
        migrations.RemoveField(
            model_name='planfinancement',
            name='type',
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='cfassoc',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='creele',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 30, 14, 28, 30, 370571, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='fleche',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='modifiele',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 30, 14, 28, 37, 490717, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='modifiepar',
            field=models.CharField(blank=True, null=True, max_length=100),
        ),
        migrations.AddField(
            model_name='planfinancement',
            name='pluriannuel',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='planfinancement',
            name='creepar',
            field=models.CharField(blank=True, null=True, max_length=100),
        ),
    ]
