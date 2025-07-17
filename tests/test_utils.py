import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.utils import load_transactions
from src.external_api import transaction_amount_in_rubles, convert_to_rubles


class TestUtils(unittest.TestCase):
    def test_load_valid_json(self):
        with patch.object(Path, 'open', create=True) as mock_open:
            mock_file = MagicMock()
            mock_file.read.return_value = '[{"id": 1, "amount": 100}]'
            mock_open.return_value.__enter__.return_value = mock_file

            result = load_transactions('test.json')
            self.assertEqual(result, [{'id': 1, 'amount': 100}])

    def test_load_invalid_json(self):
        with patch.object(Path, 'open', create=True) as mock_open:
            mock_file = MagicMock()
            mock_file.read.return_value = '{"invalid": true}'
            mock_open.return_value.__enter__.return_value = mock_file

            result = load_transactions('test.json')
            self.assertEqual(result, [])

    @patch('requests.get')
    def test_convert_usd_to_rubles(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'rates': {'RUB': 75}}
        mock_get.return_value = mock_response

        result = convert_to_rubles(100, 'USD')
        self.assertAlmostEqual(result, 7500)

    def test_transaction_amount_in_rubles(self):
        transaction = {"amount": 100, "currency": "USD"}
        expected_result = 7500  # Предполагается, что курс 1 USD = 75 RUB
        with patch('external_api.convert_to_rubles', return_value=expected_result):
            result = transaction_amount_in_rubles(transaction)
            self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
