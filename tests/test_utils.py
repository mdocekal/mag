# -*- coding: UTF-8 -*-
""""
Created on 11.11.21
Tests for utils module.

:author:     Martin Dočekal
"""
import os
import unittest

from mag.utils import bin_search

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
TMP_PATH = os.path.join(SCRIPT_PATH, "tmp")


class TestBinSearch(unittest.TestCase):
    def test_not_in(self):
        s = [0, 1, 2, 3.0, 4.0, 10]

        self.assertIsNone(bin_search(s, -3))
        self.assertIsNone(bin_search(s, 5))
        self.assertIsNone(bin_search(s, 11))

    def test_in(self):
        s = [0, 1, 2, 3.0, 4.0, 10]

        for i, x in enumerate(s):
            self.assertEqual(i, bin_search(s, x))


if __name__ == '__main__':
    unittest.main()
