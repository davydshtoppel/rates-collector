from datetime import date

from cbr import CbrServer

import unittest
import os


class CbrServerTest(unittest.TestCase):
    def test_parse_cbr_response(self):
        cbr = CbrServer()
        test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'examples', 'cbr-daily.xml')
        with open(test_file, 'r') as file:
            cbr_response = file.read()
            daily_rates = cbr.parse_cbr_response(cbr_response)
            self.assertEqual(date(2020, 2, 22), daily_rates.date)
            self.assertEqual(34, len(daily_rates.rates))

    def test_daily_rate(self):
        cbr = CbrServer()
        daily_rates = cbr.daily_rates(date(1999, 1, 4))
        self.assertEqual(date(1999, 1, 1), daily_rates.date)
        self.assertEqual(26, len(daily_rates.rates))
