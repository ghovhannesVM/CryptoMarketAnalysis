import argparse
from .constants import MAX_DAYS, SUPPORTED_CURRENCIES


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', dest='days', type=validate_days, help='Data up to number of days ago', required=True)
    parser.add_argument('--tickers', dest='tickers', type=validate_tickers, nargs='+',
                        help='List of crypto tickers separated by spaces', required=True)
    return parser.parse_args()


def validate_days(number_of_days):
    if int(number_of_days) > MAX_DAYS:
        raise argparse.ArgumentTypeError("The maximum supported number of days is 1461 (4 years).")
    return number_of_days


def validate_tickers(provided_ticker):
    if SUPPORTED_CURRENCIES.get(provided_ticker, None) is None:
        raise argparse.ArgumentTypeError(f"{provided_ticker} is not supported ticker.")
    return provided_ticker
