from unittest.mock import patch
from io import StringIO
from currency_rates import get_currency_rate

import unittest
import datetime

class CurrencyRateTestCase(unittest.TestCase):
    def test_get_currency_rate_successful(self):
        code = 'USD'
        date = '2022-10-08'
        expected_output = 'USD (Доллар США): 61,2475\n'

        with patch('sys.stdout', new=StringIO()) as fake_output:
            get_currency_rate(code, date)
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_get_currency_rate_invalid_code(self):
        code = 'RANDOM_VALUTE'
        date = '2022-10-08'
        expected_output = 'Валюта с кодом RANDOM_VALUTE не найдена\n'

        with patch('sys.stdout', new=StringIO()) as fake_output:
            get_currency_rate(code, date)
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_get_currency_rate_invalid_date(self):
        code = 'USD'
        date = '2022/10/08'
        expected_output = 'Введите корректную дату!\n'

        with patch('sys.stdout', new=StringIO()) as fake_output:
            get_currency_rate(code, date)
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_get_currency_rate_future_date(self):
        code = 'USD'
        future_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        expected_output = 'Введите дату до сегодняшнего дня!\n'

        with patch('sys.stdout', new=StringIO()) as fake_output:
            get_currency_rate(code, future_date)
            self.assertEqual(fake_output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()