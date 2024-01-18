import pandas as pd
import os
from constants import MERGED_DIRECTORY_NAME, CANDLE_FOLDER_NAME, PRICES_FOLDER_NAME


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


def start():
    candles = [os.path.join(CANDLE_FOLDER_NAME, file) for file in sorted(os.listdir(CANDLE_FOLDER_NAME))]
    prices = [os.path.join(PRICES_FOLDER_NAME, file) for file in sorted(os.listdir(PRICES_FOLDER_NAME))]
    os.makedirs(MERGED_DIRECTORY_NAME, exist_ok=True)

    for candle, price in zip(candles, prices):
        merge_files(candle, price)
