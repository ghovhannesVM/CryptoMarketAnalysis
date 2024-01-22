import data_collector
import data_merger
from common_utils import command_line_args_handler

"""
Main script for data processing.

This script initializes and starts two data processing components: data_collector and data_merger.

"""
if __name__ == '__main__':
    # Access command line arguments
    args = command_line_args_handler.get_args()

    days = args.days
    tickers = args.tickers

    # Validate tickers size
    command_line_args_handler.validate_tickers_size(tickers)

    # Start the data collector
    data_collector.start(days, tickers)

    # Start the data merger
    data_merger.start()
