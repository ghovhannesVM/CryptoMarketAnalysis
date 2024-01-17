import pandas as pd
import os

CANDLE_DIRECTORY = os.path.join('candles')
PRICE_DIRECTORY = os.path.join('prices')
MERGED_DIRECTORY_NAME = 'merged'


def calculate_return(df):
    df['return'] = (df['close'] - df['open']) / df['open']
    return df


def validate(df):
    assert not df.isna().any().any(), 'DataFrame contains NaN values'

    is_numeric = pd.to_numeric(df.stack(), errors='coerce').notna().all()
    assert is_numeric


def merge_files(file1, file2):
    df_candle = pd.read_csv(file1)
    df_price = pd.read_csv(file2)
    df_candle = calculate_return(df_candle)

    merged_data = pd.merge(df_candle, df_price, on='timestamp', how='inner')
    validate(merged_data)

    filename = f'{os.path.basename(file1)[:3]}.csv'
    output_path = os.path.join(MERGED_DIRECTORY_NAME, filename)
    merged_data.to_csv(output_path, index=False)


if __name__ == '__main__':
    candles = [os.path.join(CANDLE_DIRECTORY, file) for file in os.listdir(CANDLE_DIRECTORY)]
    prices = [os.path.join(PRICE_DIRECTORY, file) for file in os.listdir(PRICE_DIRECTORY)]
    os.makedirs(MERGED_DIRECTORY_NAME, exist_ok=True)

    for candle, price in zip(candles, prices):
        merge_files(candle, price)
