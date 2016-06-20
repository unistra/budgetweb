# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetweb', '0029_auto_20160613_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComptaNature',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(max_length=100, verbose_name='Code de la nature comptable')),
                ('label', models.CharField(max_length=100, verbose_name='Libellé', default='')),
            ],
        ),
        migrations.AlterField(
            model_name='naturecomptable',
            name='naturec_dep',
            field=models.ForeignKey(to='budgetweb.ComptaNature', verbose_name='Nature comptable', blank=True, default=''),
        ),
        migrations.DeleteModel(
            name='NatureC',
        ),
    ]
