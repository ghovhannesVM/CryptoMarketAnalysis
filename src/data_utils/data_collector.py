import requests
import os
from src.common_utils.file_handler import create_folders, write_csv
from src.common_utils.constants import DATA_FOLDER_NAME, CANDLE_FOLDER_NAME, CANDLE_FILE_NAME, PRICES_FOLDER_NAME, PRICES_FILE_NAME, SUPPORTED_CURRENCIES


def do_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return None


def get_filename(ticker, is_price):
    file_name = f"{ticker.lower()}_{PRICES_FILE_NAME if is_price else CANDLE_FILE_NAME}.csv"
    csv_file_path = os.path.join(PRICES_FOLDER_NAME if is_price else CANDLE_FOLDER_NAME, file_name)
    return csv_file_path


def get_price_data(days, ticker, coin):
    price_api_url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}&interval=daily&precision=4'
    data = do_request(price_api_url)
    if data is not None:
        prices_and_timestamps = data.get('prices')  # Extracting prices from json
        csv_columns = ['timestamp', 'price']
        prices_and_timestamps.insert(0, csv_columns)   # Adding timestamp and price as column names for the CSV file
        csv_file_path = get_filename(ticker, True)
        write_csv(prices_and_timestamps, csv_file_path)


def get_candle_data(days, ticker):
    candle_api_url = f'https://api-pub.bitfinex.com/v2/candles/trade%3A1D%3At{ticker}USD/hist?limit={days}'
    data = do_request(candle_api_url)
    if data is not None:
        csv_columns = ['timestamp', 'open', 'close', 'high', 'low', 'volume']
        data.insert(0, csv_columns)
        csv_file_path = get_filename(ticker, False)
        write_csv(data, csv_file_path)


def start(days, tickers):
    create_folders(DATA_FOLDER_NAME, PRICES_FOLDER_NAME, CANDLE_FOLDER_NAME)
    for ticker in tickers:
        get_price_data(days, ticker, SUPPORTED_CURRENCIES[ticker])
        get_candle_data(days, ticker)
