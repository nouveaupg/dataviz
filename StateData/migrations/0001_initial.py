# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import StateData.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppealReceiptsData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state_name', models.CharField(max_length=64)),
                ('year', models.PositiveSmallIntegerField(validators=[StateData.models.year_validator])),
                ('total_appeal_receipts', models.PositiveIntegerField()),
            ],
        ),
    ]
