# -*- coding: UTF-8 -*-
"""
Created on 13.12.21
Unit test for dataset module.

:author:     Martin Dočekal
"""
import os
import unittest

from mag.dataset import JsonlDataset

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

MAG_FULL_RECORD_FIXTURES_PATH = os.path.join(SCRIPT_PATH, "fixtures/mag_full_record.jsonl")


class TestJsonlDataset(unittest.TestCase):

    def setUp(self) -> None:
        self.dataset = JsonlDataset(MAG_FULL_RECORD_FIXTURES_PATH)

    def test_len(self):
        self.assertEqual(7, len(self.dataset))

    def test_read_without_opening(self):
        with self.assertRaises(RuntimeError):
            _ = self.dataset[2036354709]

    def test_not_existing_id(self):
        with self.dataset:
            with self.assertRaises(KeyError):
                _ = self.dataset[999]

    def test_reading(self):
        gts = [
            {"PaperId": 2036354709, "OriginalTitle": "Process for the production of rigid PVC foils", "Year": 1989,
             "Authors": ["Lakos Zoltán"], "References": [5], "Fields": ["IT", "Literature"], "Doi": None,
             "Journal": None},
            {"PaperId": 287156172, "OriginalTitle": "Sufism and Religious Practices in Modern Lifestyle", "Year": 2020,
             "Authors": ["Lakos Zoltán"], "References": [5], "Fields": ["IT", "Literature"], "Doi": None,
             "Journal": None},
            {"PaperId": 51244720,
             "OriginalTitle": "Önkéntes mentőszervezetek létrehozásának specifikumai egy járás tekintetében",
             "Year": 2013,
             "Authors": ["Lakos Zoltán"], "References": [5], "Fields": ["IT", "Literature"], "Doi": None,
             "Journal": None},
            {"PaperId": 2145309562,
             "OriginalTitle": "The impact of different organizational forms of road public transport on distance covered and atmospheric pollution",
             "Year": 2004, "Authors": ["Lakos Zoltán"], "References": [5], "Fields": ["IT", "Literature"], "Doi": None,
             "Journal": None},
            {"PaperId": 4302047,
             "OriginalTitle": "A repülésre veszélyes mezo-skálájú meteorológiai jelenségek modellezésének aspektusai: Numerikus prognosztikai megközelítés",
             "Year": 2009, "Authors": ["Bottyán Zsolt"], "References": [5], "Fields": ["IT", "Literature"], "Doi": None,
             "Journal": None},
            {"PaperId": 760496,
             "OriginalTitle": "Framtidas omsorgsbilde - slik det ser ut på tegnebrettet. Omsorgsplanlegging i norske kommuner. Status i 2009 - utfordringer mot 2015",
             "Year": 2009, "Authors": ["Disch, Per Gunnar", "Vetvik, Einar"], "References": [5],
             "Fields": ["IT", "Literature"], "Doi": None, "Journal": None},
            {"PaperId": 2257060365, "OriginalTitle": "Helikopter gázturbinás hajtóművek hatásfok növelésének problémái",
             "Year": 2011, "Authors": ["Varga Béla"], "References": [5], "Fields": ["IT", "Literature"],
             "Doi": "10.3233/978-1-58603-957-8-354", "Journal": "Graphs and Combinatorics"},
        ]

        with self.dataset:
            for gt in gts:
                self.assertEqual(gt, self.dataset[gt["PaperId"]])


if __name__ == '__main__':
    unittest.main()
