from datetime import date

from ecb import EcbServer

import unittest
import os


class EcbServerTest(unittest.TestCase):
    def test_parse_history_ecb_response(self):
        ecb = EcbServer()
        test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'eurofxref-hist.xml')
        with open(test_file, 'r') as file:
            ecb_response = file.read()
            history_rates = ecb.parse_ecb_response(ecb_response)
            self.assertEqual(5405, len(history_rates))
            self.assertEqual(date(1999, 1, 4), history_rates[-1].date)
            self.assertEqual(27, len(history_rates[-1].rates))
            self.assertEqual(date(2020, 2, 12), history_rates[0].date)
            self.assertEqual(32, len(history_rates[0].rates))

    def test_parse_daily_ecb_response(self):
        ecb = EcbServer()
        test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'eurofxref-daily.xml')
        with open(test_file, 'r') as file:
            ecb_response = file.read()
            history_rates = ecb.parse_ecb_response(ecb_response)
            self.assertEqual(1, len(history_rates))
            self.assertEqual(date(2020, 2, 12), history_rates[0].date)
            self.assertEqual(32, len(history_rates[0].rates))
