import os
import unittest
from unittest.mock import patch, MagicMock

from CryptoMarketAnalysis.src.data_collector import do_request

class TestDataCollector(unittest.TestCase):
    def setUp(self):
        self.data_folder = 'test_data'
        os.makedirs(self.data_folder, exist_ok=True)

    def tearDown(self):
        for root, dirs, files in os.walk(self.data_folder, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for directory in dirs:
                os.rmdir(os.path.join(root, directory))

    @patch('requests.get')
    def test_do_request_success(self, mock_requests_get):
        coin = 'bitcoin'
        days = '7'
        url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}&interval=daily&precision=4'
        expected_response = {'data': 'mocked_data'}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        mock_requests_get.return_value = mock_response

        result = do_request(url)

        mock_requests_get.assert_called_once_with(url)
        self.assertEqual(result, expected_response)

    @patch('requests.get')
    def test_do_request_failure(self, mock_requests_get):
        coin = 'bitcoin'
        days = '7'
        url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}&interval=daily&precision=4'

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = 'Not Found'

        mock_requests_get.return_value = mock_response

        result = do_request(url)

        mock_requests_get.assert_called_once_with(url)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

