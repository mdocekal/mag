# -*- coding: UTF-8 -*-
""""
Created on 02.12.21

:author:     Martin Dočekal
"""
import os
import shutil
import unittest
from pathlib import Path

from mag.mag import MAG

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
TMP_PATH = os.path.join(SCRIPT_PATH, "tmp")

MAG_FIXTURE_PATH = os.path.join(SCRIPT_PATH, "fixtures/mag")
MAG_TMP_PATH = os.path.join(SCRIPT_PATH, "tmp/mag")

LOG_TMP_PATH = os.path.join(SCRIPT_PATH, "tmp/log.txt")

MAG_PAPERS_NOT_IN_ORDER_FIXTURE_PATH = os.path.join(SCRIPT_PATH, "fixtures/mag_papers_not_in_order")
MAG_PAPERS_NOT_IN_ORDER_TMP_PATH = os.path.join(SCRIPT_PATH, "tmp/mag_papers_not_in_order")

MAG_PAPER_AUTHOR_AFFILIATIONS_NOT_IN_ORDER_FIXTURE_PATH = \
    os.path.join(SCRIPT_PATH, "fixtures/mag_paper_author_affiliations_not_in_order")
MAG_PAPER_AUTHOR_AFFILIATIONS_NOT_IN_ORDER_TMP_PATH = \
    os.path.join(SCRIPT_PATH, "tmp/mag_paper_author_affiliations_not_in_order")


class TestMagGenFullRecords(unittest.TestCase):
    def setUp(self) -> None:
        self.clear_tmp()

        shutil.copytree(MAG_FIXTURE_PATH, MAG_TMP_PATH)

        self.mag = MAG(MAG_TMP_PATH).__enter__()

    def tearDown(self) -> None:
        self.mag.__exit__(None, None, None)
        self.clear_tmp()

    @staticmethod
    def clear_tmp():
        for f in Path(TMP_PATH).glob('*'):
            if not str(f).endswith("placeholder"):
                if f.is_dir():
                    shutil.rmtree(str(f))
                else:
                    f.unlink()

    def test_update(self):

        res = list(self.mag.gen_full_records())

        self.assertEqual([
            {
                "PaperId": 2789336,
                "OriginalTitle": "Önkéntes mentőszervezetek létrehozásának specifikumai egy járás tekintetében",
                "Year": 2013,
                "Authors": ["Lakos Zoltán"],
                "References": [5],
                "Fields": ["IT"]
            },
            {
                "PaperId": 4302047,
                "OriginalTitle": "A repülésre veszélyes mezo-skálájú meteorológiai jelenségek modellezésének "
                                 "aspektusai: Numerikus prognosztikai megközelítés",
                "Year": 2009,
                "Authors": ["Bottyán Zsolt"],
                "References": [6, 7],
                "Fields": ["Biology"]
            }
        ], res)


if __name__ == '__main__':
    unittest.main()
