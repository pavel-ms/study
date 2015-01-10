# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('external_id', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('cover', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('descr', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
