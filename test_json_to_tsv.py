import unittest

import json_to_tsv

class JsonToTsvTests(unittest.TestCase):

    def test_window(self):
        rows = [0, 1, 2, 3, 4, 5]
        self.assertEqual(json_to_tsv.window(rows, -3, 2), [])
        self.assertEqual(json_to_tsv.window(rows, -2, 2), [0])
        self.assertEqual(json_to_tsv.window(rows, -1, 2), [0, 1])
        self.assertEqual(json_to_tsv.window(rows, 0, 2), [0, 1, 2])
        self.assertEqual(json_to_tsv.window(rows, 1, 2), [0, 1, 2, 3])
        self.assertEqual(json_to_tsv.window(rows, 2, 2), [0, 1, 2, 3, 4])
        self.assertEqual(json_to_tsv.window(rows, 3, 2), [1, 2, 3, 4, 5])
        self.assertEqual(json_to_tsv.window(rows, 4, 2), [2, 3, 4, 5])
        self.assertEqual(json_to_tsv.window(rows, 5, 2), [3, 4, 5])
        self.assertEqual(json_to_tsv.window(rows, 6, 2), [4, 5])
        self.assertEqual(json_to_tsv.window(rows, 7, 2), [5])
        self.assertEqual(json_to_tsv.window(rows, 8, 2), [])

