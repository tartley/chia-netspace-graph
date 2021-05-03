import unittest

import json_to_tsv


WEEK = json_to_tsv.SECS_PER_WEEK


class JsonToTsvTests(unittest.TestCase):

    def test_chunk_into_weeks(self):
        ZERO = json_to_tsv.MAINNET_LAUNCH
        rows = [
            json_to_tsv.Datum(ZERO + 0 * WEEK + 0),
            json_to_tsv.Datum(ZERO + 0 * WEEK + 1),
            json_to_tsv.Datum(ZERO + 1 * WEEK + 0),
            json_to_tsv.Datum(ZERO + 1 * WEEK + 2),
            json_to_tsv.Datum(ZERO + 3 * WEEK + 0),
        ]
        actual = json_to_tsv.chunk_into_weeks(rows, json_to_tsv.MAINNET_LAUNCH)
        self.assertEqual(
            [
                [
                    json_to_tsv.Datum(ZERO + 0 * WEEK + 0),
                    json_to_tsv.Datum(ZERO + 0 * WEEK + 1),
                ], [
                    json_to_tsv.Datum(ZERO + 1 * WEEK + 0),
                    json_to_tsv.Datum(ZERO + 1 * WEEK + 2),
                ],
                [],
                [
                    json_to_tsv.Datum(ZERO + 3 * WEEK + 0),
                ],
            ],
            actual
        )

    def test_weekly_growth_returns_(self):
        ZERO = json_to_tsv.MAINNET_LAUNCH
        rows = [
            #                 ts            raw smooth
            json_to_tsv.Datum(ZERO + 0 * WEEK + 0, 98, 100),
            json_to_tsv.Datum(ZERO + 0 * WEEK + 1, 97, 110),
            json_to_tsv.Datum(ZERO + 1 * WEEK + 0, 96, 123), # smooth += 23
            json_to_tsv.Datum(ZERO + 1 * WEEK + 1, 95, 130),
            json_to_tsv.Datum(ZERO + 2 * WEEK + 0, 94, 168), # smooth += 45
        ]
        actual = json_to_tsv.calc_growth(rows, json_to_tsv.MAINNET_LAUNCH)
        self.assertEqual(
            [
                json_to_tsv.Datum(ZERO + 0 * WEEK + 0, '_', '_', 23, 23.0),
                json_to_tsv.Datum(ZERO + 0 * WEEK + 0, 98, 100),
                json_to_tsv.Datum(ZERO + 0 * WEEK + 1, 97, 110),
                json_to_tsv.Datum(ZERO + 1 * WEEK + 0, '_', '_', 23, 23.0),
                json_to_tsv.Datum(ZERO + 1 * WEEK + 0, '_', '_', 45, 36.58536585365854),
                json_to_tsv.Datum(ZERO + 1 * WEEK + 0, 96, 123),
                json_to_tsv.Datum(ZERO + 1 * WEEK + 1, 95, 130),
                json_to_tsv.Datum(ZERO + 2 * WEEK + 0, '_', '_', 45, 36.58536585365854),
                json_to_tsv.Datum(ZERO + 2 * WEEK + 0, 94, 168),
            ],
            actual
        )

    def test_window(self):
        rows = [0, 1, 2, 3, 4, 5]
        self.assertEqual(json_to_tsv.window(rows, -1, 2), [])
        self.assertEqual(json_to_tsv.window(rows, 0, 2), [0])
        self.assertEqual(json_to_tsv.window(rows, 1, 2), [0, 1, 2])
        self.assertEqual(json_to_tsv.window(rows, 2, 2), [0, 1, 2, 3, 4])
        self.assertEqual(json_to_tsv.window(rows, 3, 2), [1, 2, 3, 4, 5])
        self.assertEqual(json_to_tsv.window(rows, 4, 2), [3, 4, 5])
        self.assertEqual(json_to_tsv.window(rows, 5, 2), [5])
        self.assertEqual(json_to_tsv.window(rows, 6, 2), [])

