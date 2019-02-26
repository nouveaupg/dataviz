# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError

from django.db import models
from django.conf import settings
import os
import csv


def load_data_from_csv_file():
    csv_path = os.path.join(settings.BASE_DIR, "static/receipts_by_state_appeals_csv.csv")
    with open(csv_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        years = []
        for row in csv_reader:
            if len(years) == 0:
                # first row
                for x in range(1, len(row)):
                    years.append(int(row[x]))
                continue
            state_name = row[0]
            for x in range(1, len(row)):
                year = years[x - 1]
                total_appeals = int(row[x].replace(",", ""))
                AppealReceiptsData.objects.create(state_name=state_name,
                                                  year=year,
                                                  total_appeal_receipts=total_appeals)


def year_validator(year):
    if year < 1900 or year > 2050:
        raise ValidationError('Year must be between 1900-2050.')

# Create your models here.


class AppealReceiptsData(models.Model):
    state_name = models.CharField(max_length=64)
    year = models.PositiveSmallIntegerField(validators=[year_validator])
    total_appeal_receipts = models.PositiveIntegerField()
