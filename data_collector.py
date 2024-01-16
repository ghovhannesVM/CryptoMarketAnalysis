import requests
import csv
import os

PRICES_FOLDER_NAME = 'prices'
PRICES_FILE_NAME = 'price'
CANDLE_FOLDER_NAME = 'candles'
CANDLE_FILE_NAME = 'candle'


def do_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return None


def write_csv(data, ticker, is_price):
    file_name = f"{ticker}_{PRICES_FILE_NAME if is_price else CANDLE_FILE_NAME}.csv"
    csv_file_path = os.path.join(PRICES_FOLDER_NAME if is_price else CANDLE_FOLDER_NAME, file_name)
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def get_price_data(ticker, coin):
    price_api_url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=365&interval=daily&precision=2'
    data = do_request(price_api_url)
    if data is not None:
        prices_and_timestamps = data.get('prices')  # Extracting prices from json
        csv_columns = ['timestamp', 'price']
        prices_and_timestamps.insert(0, csv_columns)   # Adding timestamp and price as column names for the CSV file
        write_csv(prices_and_timestamps, ticker, True)


def get_candle_data(ticker):
    candle_api_url = f'https://api-pub.bitfinex.com/v2/candles/trade%3A1D%3At{ticker.upper()}USD/hist?limit=365'
    data = do_request(candle_api_url)
    if data is not None:
        csv_columns = ['timestamp', 'open', 'close', 'high', 'low', 'volume']
        data.insert(0, csv_columns)
        write_csv(data, ticker, False)


if __name__ == '__main__':
    # creating folders for csv files
    os.makedirs(PRICES_FOLDER_NAME, exist_ok=True)
    os.makedirs(CANDLE_FOLDER_NAME, exist_ok=True)

    coins = {'btc': 'bitcoin', 'eth': 'ethereum', 'sol': 'solana', 'xrp': 'ripple', 'ada': 'cardano'}
    for ticker, coin in coins.items():
        get_price_data(ticker, coin)
        get_candle_data(ticker)