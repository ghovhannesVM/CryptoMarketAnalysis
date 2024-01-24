import unittest
import os
import pandas as pd
from unittest.mock import patch
from src.data_utils.data_merger import calculate_return, merge_files, start
import shutil


class TestDataMerger(unittest.TestCase):

    __FOLDER_NAME = 'test_data'

    def setUp(self):
        os.makedirs(self.__FOLDER_NAME, exist_ok=True)

    def tearDown(self):
        for root, dirs, files in os.walk(self.__FOLDER_NAME, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            shutil.rmtree(self.__FOLDER_NAME)

    def create_mocked_data(self, filename, columns, data):
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(os.path.join(self.__FOLDER_NAME, filename), index=False)
        return os.path.join(self.__FOLDER_NAME, filename)

    @patch('src.data_utils.data_merger.calculate_return')
    def test_calculate_return(self, mock_calculate_return):
        columns = ['timestamp', 'open', 'close', 'high', 'low', 'volume']
        data = [[1, 10, 15, 14, 8, 100], [2, 15, 18, 20, 12, 150]]
        input_file = self.create_mocked_data('test_candle.csv', columns, data)

        df = pd.read_csv(input_file)
        df = calculate_return(df)

        expected_values = [0.5, 0.2]
        pd.testing.assert_series_equal(df['return'], pd.Series(expected_values, name='return'))

    @patch('src.data_utils.data_merger.calculate_return')
    @patch('src.data_utils.data_merger.clean_and_validate')
    @patch('src.data_utils.data_merger.pd.read_csv')
    def test_merge_files(self, mock_read_csv, mock_clean_and_validate, mock_calculate_return):
        columns_candle = ['timestamp', 'open', 'close', 'high', 'low', 'volume']
        data_candle = [[1, 10, 12, 14, 8, 100], [2, 15, 18, 20, 12, 150]]
        input_candle = self.create_mocked_data('test_candle.csv', columns_candle, data_candle)

        columns_price = ['timestamp', 'price']
        data_price = [[1, 20], [2, 25]]
        input_price = self.create_mocked_data('test_price.csv', columns_price, data_price)

        # Mock the return values for pd.read_csv and calculate_return
        mock_read_csv.return_value = pd.DataFrame({'timestamp': [1, 2], 'open': [10, 15], 'close': [12, 18]})
        mock_calculate_return.return_value = pd.DataFrame({'timestamp': [1, 2], 'return': [0.2, 0.3]})

        merge_files(input_candle, input_price)

        mock_read_csv.assert_any_call(input_candle)
        mock_read_csv.assert_any_call(input_price)
        mock_calculate_return.assert_called_once_with(mock_read_csv.return_value)

    @patch('src.data_utils.data_merger.get_folder_contents')
    @patch('src.data_utils.data_merger.remove_folders')
    @patch('src.data_utils.data_merger.merge_files')
    def test_start(self, mock_merge_files, mock_remove_folders, mock_get_folder_contents):
        mock_get_folder_contents.side_effect = [
            ['candle1.csv', 'candle2.csv'],
            ['price1.csv', 'price2.csv']
        ]

        start()

        mock_merge_files.assert_called_with('candle2.csv', 'price2.csv')
        mock_remove_folders.assert_called_with('data/candles', 'data/prices')


if __name__ == '__main__':
    unittest.main()

