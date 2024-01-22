import argparse
from .constants import MAX_DAYS, MAX_TICKERS_COUNT, SUPPORTED_CURRENCIES


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', dest='days', type=validate_days, help='Data up to number of days ago', required=True)
    parser.add_argument('--tickers', dest='tickers', type=validate_ticker, nargs='+',
                        help='List of crypto tickers separated by spaces', required=True)
    return parser.parse_args()


def validate_days(number_of_days):
    if int(number_of_days) > MAX_DAYS:
        raise argparse.ArgumentTypeError(f"The maximum supported number of days is {MAX_DAYS} days.")
    return number_of_days


def validate_ticker(provided_ticker):
    if SUPPORTED_CURRENCIES.get(provided_ticker, None) is None:
        raise argparse.ArgumentTypeError(f"{provided_ticker} is not supported ticker.")
    return provided_ticker


def validate_tickers_size(tickers):
    if len(tickers) > MAX_TICKERS_COUNT:
        raise argparse.ArgumentTypeError(f"The maximum number of tickers is {MAX_TICKERS_COUNT}.")
