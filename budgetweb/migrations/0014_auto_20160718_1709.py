# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetweb', '0013_auto_20160718_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='StructureAuthorizations',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('structures', models.ManyToManyField(to='budgetweb.Structure', related_name='authorized_structures')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'structure authorization',
                'verbose_name_plural': 'structures authorizations',
            },
        ),
        migrations.DeleteModel(
            name='Authorisation',
        ),
    ]
