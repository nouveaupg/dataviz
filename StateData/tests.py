# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import AppealReceiptsData
from django.conf import settings
from django.test import TestCase
import csv
import os

# Create your tests here.


class ModelTestCase(TestCase):
    def setUp(self):
        AppealReceiptsData.objects.create(state_name="Alabama", year=2006, total_appeal_receipts=290)

    def test_get_object(self):
        record = AppealReceiptsData.objects.get(state_name="Alabama", year=2006)
        self.assertEqual(record.total_appeal_receipts, 290)


class DataImportTestCase(TestCase):
    def setUp(self):
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
                    year = years[x-1]
                    total_appeals = int(row[x].replace(",", ""))
                    AppealReceiptsData.objects.create(state_name=state_name,
                                                      year=year,
                                                      total_appeal_receipts=total_appeals)

    # test values somewhat randomly throughout the data to make sure the csv import was successful

    def test_Arizona_2006(self):
        record = AppealReceiptsData.objects.get(state_name="Arizona", year=2006)
        self.assertEqual(record.total_appeal_receipts, 191)

    def test_DC_2014(self):
        record = AppealReceiptsData.objects.get(state_name="District of Columbia", year=2014)
        self.assertEqual(record.total_appeal_receipts, 498)

    def test_Guam_2009(self):
        record = AppealReceiptsData.objects.get(state_name="Guam", year=2009)
        self.assertEqual(record.total_appeal_receipts, 0)

    def test_Texas_2013(self):
        record = AppealReceiptsData.objects.get(state_name="Texas", year=2013)
        self.assertEqual(record.total_appeal_receipts, 19010)

    def test_Unspecified_2011(self):
        record = AppealReceiptsData.objects.get(state_name="Unspecified", year=2011)
        self.assertEqual(record.total_appeal_receipts, 24)

    # aggregation (interesting how these tests run as fast as the above!)

    def test_distinct_years(self):
        years = []
        all_objects = AppealReceiptsData.objects.all()
        for each in all_objects:
            if each.year not in years:
                years.append(each.year)
        self.assertGreater(len(years), 0)
        print(str(years))

    def test_distinct_states(self):
        state_names = []
        all_objects = AppealReceiptsData.objects.all()
        for each in all_objects:
            if each.state_name not in state_names:
                state_names.append(each.state_name)
        self.assertGreater(len(state_names), 0)
        print(str(state_names))
