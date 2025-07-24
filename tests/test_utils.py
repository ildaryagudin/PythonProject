import unittest
from unittest.mock import patch, MagicMock
from src.utils import load_transactions
import pandas as pd
import json
import os

class TestLoadTransactions(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 200}
        ]

    @patch("main.open")
    def test_load_from_json(self, mock_open):
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = json.dumps(self.test_data)
        mock_open.return_value = mock_file
        result = load_transactions("mocked.json", "json")
        self.assertEqual(result, self.test_data)

    @patch("pandas.read_csv")
    def test_load_from_csv(self, mock_read_csv):
        mock_df = pd.DataFrame(self.test_data)
        mock_read_csv.return_value = mock_df
        result = load_transactions("mocked.csv", "csv")
        self.assertEqual(result, self.test_data)

    @patch("pandas.read_excel")
    def test_load_from_excel(self, mock_read_excel):
        mock_df = pd.DataFrame(self.test_data)
        mock_read_excel.return_value = mock_df
        result = load_transactions("mocked.xlsx", "xlsx")
        self.assertEqual(result, self.test_data)

    @patch("main.open", side_effect=FileNotFoundError())
    def test_nonexistent_file(self, _):
        result = load_transactions("nonexistent.json", "json")
        self.assertEqual(result, [])

    @patch("main.open")
    def test_invalid_json_format(self, mock_open):
        mock_file = MagicMock()
        mock_file.__enter__.return_value.read.return_value = "{invalid json}"
        mock_open.return_value = mock_file
        result = load_transactions("invalid.json", "json")
        self.assertEqual(result, [])

    def test_automatic_detection(self):
        for extension in ["json", "csv", "xlsx"]:
            path = f"autodetect.{extension}"
            result = load_transactions(path)
            self.assertIsInstance(result, list)

    def test_unsupported_filetype(self):
        result = load_transactions("unsupported.filetype", "unknown")
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()