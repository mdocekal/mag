# -*- coding: UTF-8 -*-
""""
Created on 03.12.21
Tests for __main__ module.

:author:     Martin Dočekal
"""
import os
import unittest
from pathlib import Path
from shutil import copyfile

from mag.__main__ import stats_count

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
TMP_PATH = os.path.join(SCRIPT_PATH, "tmp")

MAG_FULL_RECORD_FIXTURES_PATH = os.path.join(SCRIPT_PATH, "fixtures/mag_full_record.jsonl")


class TestStatsCount(unittest.TestCase):

    def test_stats_without_filter(self):
        with open(MAG_FULL_RECORD_FIXTURES_PATH, "r") as f:
            stats_res = stats_count(f)
            self.assertEqual(
                {
                    "total_cnt": 7,
                    "passed_filter_cnt": 7,
                    "year_hist": {2020: 1, 2013: 1, 2004: 1, 1989: 1, 2009: 2, 2011: 1},
                    "fields_hist": {"IT": 7, "Literature": 7}
                },
                stats_res
            )

    def test_stats_with_filter(self):
        with open(MAG_FULL_RECORD_FIXTURES_PATH, "r") as f:
            stats_res = stats_count(f, r"(?i).*The.*")
            self.assertEqual(
                {
                    "total_cnt": 7,
                    "passed_filter_cnt": 2,
                    "year_hist": {2004: 1, 1989: 1},
                    "fields_hist": {"IT": 2, "Literature": 2}
                },
                stats_res
            )


if __name__ == '__main__':
    unittest.main()
